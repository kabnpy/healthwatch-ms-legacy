import uuid
from typing import Any, cast

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.models.insurance.catalog import Product
from app.models.insurance.financial import (
    Invoice,
    InvoiceBulkCreate,
    InvoiceCreate,
    InvoiceLineItem,
    InvoiceUpdate,
    Receipt,
    ReceiptAllocation,
    ReceiptAllocationCreate,
    ReceiptCreate,
)
from app.models.insurance.policy import Policy, RiskNote

# ==========================================
# Invoice CRUD
# ==========================================


def create_invoice(*, session: Session, invoice_in: InvoiceCreate) -> Invoice:
    db_obj = Invoice.model_validate(invoice_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def create_invoice_bulk(*, session: Session, bulk_in: InvoiceBulkCreate) -> Invoice:
    # 1. Create the Invoice
    invoice = Invoice(
        invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
        client_id=bulk_in.client_id,
        date_issued=bulk_in.date_issued,
        notes=bulk_in.notes,
        total_amount=0.0,
        balance_due=0.0,
        status="Unpaid",
    )
    session.add(invoice)
    session.commit()
    session.refresh(invoice)

    total_amount = 0.0

    # 2. Link Risk Notes via Line Items
    for rn_id in bulk_in.risk_note_ids:
        rn = session.get(RiskNote, rn_id)
        if rn:
            policy = session.get(Policy, rn.policy_id)
            policy_num = policy.policy_number if policy else "Unknown"

            line_item = InvoiceLineItem(
                invoice_id=invoice.id,
                risk_note_id=rn.id,
                amount=rn.total_amount,
                description=f"{rn.transaction_type} - {policy_num}",
            )
            session.add(line_item)
            total_amount += rn.total_amount

            # Update Risk Note with Invoice Number
            rn.invoice_number = invoice.invoice_number
            session.add(rn)

    # 3. Update Invoice Totals
    invoice.total_amount = total_amount
    invoice.balance_due = total_amount
    session.add(invoice)

    session.commit()
    session.refresh(invoice)
    return invoice


def get_invoice(session: Session, *, id: uuid.UUID) -> Invoice | None:
    statement = (
        select(Invoice)
        .where(Invoice.id == id)
        .options(
            selectinload(cast(Any, Invoice.allocations)),
            selectinload(cast(Any, Invoice.line_items))
            .joinedload(cast(Any, InvoiceLineItem.risk_note))
            .joinedload(cast(Any, RiskNote.policy))
            .joinedload(cast(Any, Policy.product))
            .joinedload(cast(Any, Product.insurer)),
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
    statement = select(Invoice).options(
        selectinload(cast(Any, Invoice.allocations)),
        selectinload(cast(Any, Invoice.line_items))
        .joinedload(cast(Any, InvoiceLineItem.risk_note))
        .joinedload(cast(Any, RiskNote.policy))
        .joinedload(cast(Any, Policy.product))
        .joinedload(cast(Any, Product.insurer)),
    )
    if client_id:
        statement = statement.where(Invoice.client_id == client_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def update_invoice(
    *, session: Session, db_invoice: Invoice, invoice_in: InvoiceUpdate
) -> Invoice:
    update_data = invoice_in.model_dump(exclude_unset=True)
    db_invoice.sqlmodel_update(update_data)
    session.add(db_invoice)
    session.commit()
    session.refresh(db_invoice)
    return db_invoice


# ==========================================
# Receipt CRUD
# ==========================================


def create_receipt(*, session: Session, receipt_in: ReceiptCreate) -> Receipt:
    db_obj = Receipt.model_validate(receipt_in)
    db_obj.unallocated_amount = db_obj.amount
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_receipt(session: Session, *, id: uuid.UUID) -> Receipt | None:
    statement = (
        select(Receipt)
        .where(Receipt.id == id)
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
    statement = select(Receipt).options(selectinload(cast(Any, Receipt.allocations)))
    if client_id:
        statement = statement.where(Receipt.client_id == client_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def void_receipt(*, session: Session, db_receipt: Receipt) -> Receipt:
    # 1. Reverse all allocations
    for allocation in db_receipt.allocations:
        invoice = session.get(Invoice, allocation.invoice_id)
        if invoice:
            invoice.balance_due += allocation.amount_allocated
            # Update status back
            if invoice.balance_due >= invoice.total_amount:
                invoice.status = "Unpaid"
            else:
                invoice.status = "Partial"
            session.add(invoice)
        session.delete(allocation)

    # 2. Mark receipt as voided
    db_receipt.status = "Voided"
    db_receipt.unallocated_amount = 0
    session.add(db_receipt)
    session.commit()
    session.refresh(db_receipt)
    return db_receipt


# ==========================================
# Allocation CRUD
# ==========================================


def create_receipt_allocation(
    *, session: Session, allocation_in: ReceiptAllocationCreate
) -> ReceiptAllocation:
    # 1. Create the allocation
    db_obj = ReceiptAllocation.model_validate(allocation_in)
    session.add(db_obj)

    # 2. Update the Invoice balance
    invoice = session.get(Invoice, db_obj.invoice_id)
    if invoice:
        invoice.balance_due -= db_obj.amount_allocated
        # Auto-update status
        if invoice.balance_due <= 0:
            invoice.status = "Paid"
        elif invoice.balance_due < invoice.total_amount:
            invoice.status = "Partial"
        session.add(invoice)

    # 3. Update the Receipt (Payment) unallocated amount
    receipt = session.get(Receipt, db_obj.receipt_id)
    if receipt:
        receipt.unallocated_amount -= db_obj.amount_allocated
        session.add(receipt)

    session.commit()
    session.refresh(db_obj)
    return db_obj
