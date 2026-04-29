import uuid
from collections.abc import Sequence
from datetime import date, datetime, timedelta
from typing import Any, cast

from sqlalchemy.orm import selectinload
from sqlmodel import Session, col, func, select

from app.models import (
    Insurer,
    InsurerCreate,
    InsurerUpdate,
    Invoice,
    InvoiceBulkCreate,
    InvoiceCreate,
    InvoiceLineItem,
    InvoiceLineItemCreate,
    InvoiceStatus,
    InvoiceUpdate,
    Policy,
    PolicyCreate,
    PolicyStatus,
    PolicyUpdate,
    Product,
    ProductCreate,
    ProductUpdate,
    Receipt,
    ReceiptAllocation,
    ReceiptAllocationCreate,
    ReceiptCreate,
    ReceiptStatus,
    RiskNote,
    RiskNoteCreate,
    RiskNoteStatus,
    RiskNoteUpdate,
)

# ==========================================
# Insurer & Product CRUD
# ==========================================


def create_insurer(*, session: Session, insurer_in: InsurerCreate) -> Insurer:
    db_obj = Insurer.model_validate(insurer_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_insurer_by_name(session: Session, *, name: str) -> Insurer | None:
    statement = (
        select(Insurer).where(Insurer.name == name).where(Insurer.deleted_at == None)
    )
    return session.exec(statement).first()


def get_insurers(session: Session, *, skip: int = 0, limit: int = 100) -> list[Insurer]:
    statement = (
        select(Insurer).where(Insurer.deleted_at == None).offset(skip).limit(limit)
    )
    return list(session.exec(statement).all())


def count_insurers(session: Session) -> int:
    statement = (
        select(func.count()).select_from(Insurer).where(Insurer.deleted_at == None)
    )
    return session.exec(statement).one()


def delete_insurer(session: Session, *, db_insurer: Insurer) -> None:
    db_insurer.deleted_at = datetime.now()
    session.add(db_insurer)
    session.commit()


def update_insurer(
    *, session: Session, db_insurer: Insurer, insurer_in: InsurerUpdate
) -> Insurer:
    insurer_data = insurer_in.model_dump(exclude_unset=True)
    db_insurer.sqlmodel_update(insurer_data)
    session.add(db_insurer)
    session.commit()
    session.refresh(db_insurer)
    return db_insurer


def create_product(*, session: Session, product_in: ProductCreate) -> Product:
    db_obj = Product.model_validate(product_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_product_by_name(session: Session, *, name: str) -> Product | None:
    statement = (
        select(Product).where(Product.name == name).where(Product.deleted_at == None)
    )
    return session.exec(statement).first()


def get_products(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    insurer_id: uuid.UUID | None = None,
) -> list[Product]:
    statement = select(Product).where(Product.deleted_at == None)
    if insurer_id:
        statement = statement.where(Product.insurer_id == insurer_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_products(session: Session, *, insurer_id: uuid.UUID | None = None) -> int:
    statement = select(Product).where(Product.deleted_at == None)
    if insurer_id:
        statement = statement.where(Product.insurer_id == insurer_id)
    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_product(session: Session, *, db_product: Product) -> None:
    db_product.deleted_at = datetime.now()
    session.add(db_product)
    session.commit()


def update_product(
    *, session: Session, db_product: Product, product_in: ProductUpdate
) -> Product:
    product_data = product_in.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


# ==========================================
# Policy & Risk Note CRUD
# ==========================================


def create_policy(*, session: Session, policy_in: PolicyCreate) -> Policy:
    db_obj = Policy.model_validate(policy_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_policy(session: Session, *, id: uuid.UUID) -> Policy | None:
    statement = (
        select(Policy)
        .where(Policy.id == id)
        .where(Policy.deleted_at == None)
        .options(
            selectinload(cast(Any, Policy.product)),
            selectinload(cast(Any, Policy.client)),
            selectinload(cast(Any, Policy.risk_notes))
            .selectinload(cast(Any, RiskNote.invoice_line_items))
            .selectinload(cast(Any, InvoiceLineItem.invoice)),
        )
    )
    return session.exec(statement).first()


def get_policy_by_policy_number(
    session: Session, *, policy_number: str
) -> Policy | None:
    statement = (
        select(Policy)
        .where(Policy.policy_number == policy_number)
        .where(Policy.deleted_at == None)
    )
    return session.exec(statement).first()


def get_policies_by_client_id(
    session: Session, *, client_id: uuid.UUID
) -> Sequence[Policy]:
    statement = (
        select(Policy)
        .where(Policy.client_id == client_id)
        .where(Policy.deleted_at == None)
        .options(
            selectinload(cast(Any, Policy.product)),
            selectinload(cast(Any, Policy.client)),
            selectinload(cast(Any, Policy.risk_notes))
            .selectinload(cast(Any, RiskNote.invoice_line_items))
            .selectinload(cast(Any, InvoiceLineItem.invoice)),
        )
    )
    return session.exec(statement).all()


def update_policy(
    *, session: Session, db_policy: Policy, policy_in: PolicyUpdate
) -> Policy:
    policy_data = policy_in.model_dump(exclude_unset=True)
    db_policy.sqlmodel_update(policy_data)
    session.add(db_policy)
    session.commit()
    session.refresh(db_policy)
    return db_policy


def _apply_expiry_filter(statement: Any, expiring_within: int) -> Any:
    target_date = date.today() + timedelta(days=expiring_within)
    latest_rn_sub = (
        select(RiskNote.policy_id, func.max(RiskNote.coverage_end).label("max_end"))
        .where(RiskNote.status == RiskNoteStatus.ISSUED)
        .where(RiskNote.deleted_at == None)
        .group_by(col(RiskNote.policy_id))
        .subquery()
    )
    statement = statement.join(
        latest_rn_sub, col(Policy.id) == latest_rn_sub.c.policy_id
    )
    statement = statement.where(latest_rn_sub.c.max_end <= target_date)
    statement = statement.where(latest_rn_sub.c.max_end >= date.today())
    statement = statement.where(
        col(Policy.status).in_([PolicyStatus.ACTIVE, PolicyStatus.RENEWAL_INVITED])
    )
    return statement


def get_policies(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    client_id: uuid.UUID | None = None,
    expiring_within: int | None = None,
) -> list[Policy]:
    statement = (
        select(Policy)
        .where(Policy.deleted_at == None)
        .options(
            selectinload(cast(Any, Policy.product)),
            selectinload(cast(Any, Policy.client)),
            selectinload(cast(Any, Policy.risk_notes))
            .selectinload(cast(Any, RiskNote.invoice_line_items))
            .selectinload(cast(Any, InvoiceLineItem.invoice)),
        )
    )
    if expiring_within is not None:
        statement = _apply_expiry_filter(statement, expiring_within)

    if client_id:
        statement = statement.where(Policy.client_id == client_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_policies(
    session: Session,
    *,
    client_id: uuid.UUID | None = None,
    expiring_within: int | None = None,
) -> int:
    statement = select(Policy).where(Policy.deleted_at == None)
    if expiring_within is not None:
        statement = _apply_expiry_filter(statement, expiring_within)

    if client_id:
        statement = statement.where(Policy.client_id == client_id)
    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_policy(session: Session, *, db_policy: Policy) -> None:
    db_policy.deleted_at = datetime.now()
    session.add(db_policy)
    session.commit()


def create_risk_note(*, session: Session, risk_note_in: RiskNoteCreate) -> RiskNote:
    db_obj = RiskNote.model_validate(risk_note_in)
    if not db_obj.risk_note_number:
        from app.services.policy import generate_risk_note_number

        db_obj.risk_note_number = generate_risk_note_number()
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_risk_note(
    *, session: Session, db_risk_note: RiskNote, risk_note_in: RiskNoteUpdate
) -> RiskNote:
    risk_note_data = risk_note_in.model_dump(exclude_unset=True)
    db_risk_note.sqlmodel_update(risk_note_data)
    session.add(db_risk_note)
    session.commit()
    session.refresh(db_risk_note)
    return db_risk_note


def get_risk_notes(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    policy_id: uuid.UUID | None = None,
    client_id: uuid.UUID | None = None,
    uninvoiced_only: bool = False,
) -> list[RiskNote]:
    statement = (
        select(RiskNote)
        .where(RiskNote.deleted_at == None)
        .options(
            selectinload(cast(Any, RiskNote.invoice_line_items)).selectinload(
                cast(Any, InvoiceLineItem.invoice)
            )
        )
    )
    if policy_id:
        statement = statement.where(RiskNote.policy_id == policy_id)
    if client_id:
        statement = statement.join(Policy).where(Policy.client_id == client_id)
    if uninvoiced_only:
        statement = statement.where(~cast(Any, RiskNote.invoice_line_items).any())
        statement = statement.where(RiskNote.status != RiskNoteStatus.DRAFT)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_risk_notes(
    session: Session,
    *,
    policy_id: uuid.UUID | None = None,
    client_id: uuid.UUID | None = None,
    uninvoiced_only: bool = False,
) -> int:
    statement = select(RiskNote).where(RiskNote.deleted_at == None)
    if policy_id:
        statement = statement.where(RiskNote.policy_id == policy_id)
    if client_id:
        statement = statement.join(Policy).where(Policy.client_id == client_id)
    if uninvoiced_only:
        statement = statement.where(~cast(Any, RiskNote.invoice_line_items).any())
        statement = statement.where(RiskNote.status != RiskNoteStatus.DRAFT)
    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_risk_note(session: Session, *, db_risk_note: RiskNote) -> None:
    db_risk_note.deleted_at = datetime.now()
    session.add(db_risk_note)
    session.commit()


# ==========================================
# Financial CRUD
# ==========================================


def create_invoice(*, session: Session, invoice_in: InvoiceCreate) -> Invoice:
    db_obj = Invoice.model_validate(invoice_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_invoice(session: Session, *, id: uuid.UUID) -> Invoice | None:
    statement = (
        select(Invoice)
        .where(Invoice.id == id)
        .where(Invoice.deleted_at == None)
        .options(
            selectinload(cast(Any, Invoice.allocations)),
            selectinload(cast(Any, Invoice.line_items)),
        )
    )
    return session.exec(statement).first()


def get_invoices(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    client_id: uuid.UUID | None = None,
) -> list[Invoice]:
    statement = (
        select(Invoice)
        .where(Invoice.deleted_at == None)
        .options(
            selectinload(cast(Any, Invoice.allocations)),
            selectinload(cast(Any, Invoice.line_items)),
        )
    )
    if client_id:
        statement = statement.where(Invoice.client_id == client_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def update_invoice(
    *, session: Session, db_invoice: Invoice, invoice_in: InvoiceUpdate
) -> Invoice:
    invoice_data = invoice_in.model_dump(exclude_unset=True)
    db_invoice.sqlmodel_update(invoice_data)
    session.add(db_invoice)
    session.commit()
    session.refresh(db_invoice)
    return db_invoice


def create_invoice_bulk(*, session: Session, bulk_in: InvoiceBulkCreate) -> Invoice:
    risk_notes = session.exec(
        select(RiskNote).where(col(RiskNote.id).in_(bulk_in.risk_note_ids))
    ).all()
    total_amount = sum(rn.total_amount for rn in risk_notes)
    invoice_in = InvoiceCreate(
        invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
        client_id=bulk_in.client_id,
        date_issued=bulk_in.date_issued,
        total_amount=total_amount,
        balance_due=total_amount,
        notes=bulk_in.notes,
        status=InvoiceStatus.UNPAID,
    )
    invoice = create_invoice(session=session, invoice_in=invoice_in)
    for rn in risk_notes:
        line_item_in = InvoiceLineItemCreate(
            invoice_id=invoice.id,
            risk_note_id=rn.id,
            amount=rn.total_amount,
            description=f"{rn.transaction_type} - RN {rn.risk_note_number}",
        )
        create_invoice_line_item(session=session, line_item_in=line_item_in)
    session.commit()
    session.refresh(invoice)
    return invoice


def create_invoice_line_item(
    *, session: Session, line_item_in: InvoiceLineItemCreate
) -> InvoiceLineItem:
    db_obj = InvoiceLineItem.model_validate(line_item_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def create_receipt(*, session: Session, receipt_in: ReceiptCreate) -> Receipt:
    db_obj = Receipt.model_validate(receipt_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_receipt(session: Session, *, id: uuid.UUID) -> Receipt | None:
    statement = (
        select(Receipt)
        .where(Receipt.id == id)
        .where(Receipt.deleted_at == None)
        .options(selectinload(cast(Any, Receipt.allocations)))
    )
    return session.exec(statement).first()


def get_receipts(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    client_id: uuid.UUID | None = None,
) -> list[Receipt]:
    statement = (
        select(Receipt)
        .where(Receipt.deleted_at == None)
        .options(selectinload(cast(Any, Receipt.allocations)))
    )
    if client_id:
        statement = statement.where(Receipt.client_id == client_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def void_receipt(*, session: Session, db_receipt: Receipt) -> Receipt:
    db_receipt.status = ReceiptStatus.VOIDED
    session.add(db_receipt)
    session.commit()
    session.refresh(db_receipt)
    return db_receipt


def create_receipt_allocation(
    *, session: Session, allocation_in: ReceiptAllocationCreate
) -> ReceiptAllocation:
    db_obj = ReceiptAllocation.model_validate(allocation_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
