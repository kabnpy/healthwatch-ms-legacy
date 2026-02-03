import uuid
from collections.abc import Sequence
from datetime import date
from typing import Any, cast

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.models.insurance.financial import Invoice, InvoiceLineItem
from app.models.insurance.policy import (
    Claim,
    ClaimCreate,
    ClaimEvent,
    ClaimEventCreate,
    ClaimUpdate,
    Document,
    DocumentCreate,
    DocumentUpdate,
    Policy,
    PolicyCreate,
    PolicyUpdate,
    RiskItem,
    RiskItemCreate,
    RiskItemUpdate,
    RiskNote,
    RiskNoteCreate,
    RiskNoteUpdate,
)


def create_policy(*, session: Session, policy_in: PolicyCreate) -> Policy:
    db_obj = Policy.model_validate(policy_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    # Automatically create the first Risk Note for the new policy
    from datetime import date, timedelta

    first_risk_note_in = RiskNoteCreate(
        policy_id=db_obj.id,
        transaction_type="New Business",
        status="Draft",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=365),
        net_premium=0.0,
        taxes={},
        commission_amount=0.0,
        total_amount=0.0,
        items_snapshot={},
        special_clauses=[],
    )
    create_risk_note(session=session, risk_note_in=first_risk_note_in)

    return db_obj


def get_policy(session: Session, *, id: uuid.UUID) -> Policy | None:
    statement = (
        select(Policy)
        .where(Policy.id == id)
        .options(
            selectinload(cast(Any, Policy.product)),
            selectinload(cast(Any, Policy.items)),
        )
    )
    return session.exec(statement).first()


def get_policy_by_policy_number(
    session: Session, *, policy_number: str
) -> Policy | None:
    statement = select(Policy).where(Policy.policy_number == policy_number)
    return session.exec(statement).first()


def get_policies_by_client_id(
    session: Session, *, client_id: uuid.UUID
) -> Sequence[Policy]:
    statement = (
        select(Policy)
        .where(Policy.client_id == client_id)
        .options(
            selectinload(cast(Any, Policy.product)),
            selectinload(cast(Any, Policy.items)),
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


def create_risk_item(*, session: Session, risk_item_in: RiskItemCreate) -> RiskItem:
    db_obj = RiskItem.model_validate(risk_item_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_risk_item_by_identifier(
    _session: Session, *, _identifier: str
) -> RiskItem | None:
    # In temporal items, identifier might be in risk_details
    # For now, we search by description or similar if needed,
    # but the old identifier column is gone.
    return None


def update_risk_item(
    *, session: Session, db_risk_item: RiskItem, risk_item_in: RiskItemUpdate
) -> RiskItem:
    risk_item_data = risk_item_in.model_dump(exclude_unset=True)
    db_risk_item.sqlmodel_update(risk_item_data)
    session.add(db_risk_item)
    session.commit()
    session.refresh(db_risk_item)
    return db_risk_item


def create_risk_note(*, session: Session, risk_note_in: RiskNoteCreate) -> RiskNote:
    # 1. Create the Risk Note
    db_obj = RiskNote.model_validate(risk_note_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    # 2. Handle Invoicing Logic
    policy = session.get(Policy, db_obj.policy_id)
    if not policy:
        return db_obj

    amount = db_obj.total_amount

    # Check for an existing Unpaid invoice for this client
    statement = select(Invoice).where(
        Invoice.client_id == policy.client_id, Invoice.status == "Unpaid"
    )
    invoice = session.exec(statement).first()

    if not invoice:
        # Create a new invoice
        invoice = Invoice(
            invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
            client_id=policy.client_id,
            date_issued=date.today(),
            total_amount=0.0,
            balance_due=0.0,
            status="Unpaid",
        )
        session.add(invoice)
        session.commit()
        session.refresh(invoice)

    # Create Line Item linking Risk Note to Invoice
    line_item = InvoiceLineItem(
        invoice_id=invoice.id,
        risk_note_id=db_obj.id,
        amount=amount,
        description=f"{db_obj.transaction_type} - {policy.policy_number}",
    )
    session.add(line_item)

    # Update Invoice Totals
    invoice.total_amount += amount
    invoice.balance_due += amount
    session.add(invoice)

    # Update RiskNote with Invoice Number
    db_obj.invoice_number = invoice.invoice_number
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


def create_claim(*, session: Session, claim_in: ClaimCreate) -> Claim:
    db_obj = Claim.model_validate(claim_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_claim(*, session: Session, db_claim: Claim, claim_in: ClaimUpdate) -> Claim:
    claim_data = claim_in.model_dump(exclude_unset=True)
    db_claim.sqlmodel_update(claim_data)
    session.add(db_claim)
    session.commit()
    session.refresh(db_claim)
    return db_claim


def get_policies(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    client_id: uuid.UUID | None = None,
) -> list[Policy]:
    statement = select(Policy).options(
        selectinload(cast(Any, Policy.product)), selectinload(cast(Any, Policy.items))
    )
    if client_id:
        statement = statement.where(Policy.client_id == client_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_policies(session: Session, *, client_id: uuid.UUID | None = None) -> int:
    from sqlmodel import func

    statement = select(Policy)
    if client_id:
        statement = statement.where(Policy.client_id == client_id)
    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_policy(session: Session, *, db_policy: Policy) -> None:
    session.delete(db_policy)
    session.commit()


def get_claims(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    policy_id: uuid.UUID | None = None,
    client_id: uuid.UUID | None = None,
) -> list[Claim]:
    statement = select(Claim)
    if policy_id:
        statement = statement.where(Claim.policy_id == policy_id)
    if client_id:
        statement = statement.join(Policy).where(Policy.client_id == client_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_claims(
    session: Session,
    *,
    policy_id: uuid.UUID | None = None,
    client_id: uuid.UUID | None = None,
) -> int:
    from sqlmodel import func

    statement = select(Claim)
    if policy_id:
        statement = statement.where(Claim.policy_id == policy_id)
    if client_id:
        statement = statement.join(Policy).where(Policy.client_id == client_id)
    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_claim(session: Session, *, db_claim: Claim) -> None:
    session.delete(db_claim)
    session.commit()


def get_risk_items(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    policy_id: uuid.UUID | None = None,
) -> list[RiskItem]:
    statement = select(RiskItem)
    if policy_id:
        statement = statement.where(RiskItem.policy_id == policy_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_risk_items(session: Session, *, policy_id: uuid.UUID | None = None) -> int:
    from sqlmodel import func

    statement = select(RiskItem)
    if policy_id:
        statement = statement.where(RiskItem.policy_id == policy_id)
    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_risk_item(session: Session, *, db_risk_item: RiskItem) -> None:
    session.delete(db_risk_item)
    session.commit()


def get_risk_notes(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    policy_id: uuid.UUID | None = None,
) -> list[RiskNote]:
    statement = select(RiskNote)
    if policy_id:
        statement = statement.where(RiskNote.policy_id == policy_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_risk_notes(session: Session, *, policy_id: uuid.UUID | None = None) -> int:
    from sqlmodel import func

    statement = select(RiskNote)
    if policy_id:
        statement = statement.where(RiskNote.policy_id == policy_id)
    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_risk_note(session: Session, *, db_risk_note: RiskNote) -> None:
    session.delete(db_risk_note)
    session.commit()


def create_claim_event(
    *, session: Session, claim_event_in: ClaimEventCreate
) -> ClaimEvent:
    db_obj = ClaimEvent.model_validate(claim_event_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def create_document(*, session: Session, document_in: DocumentCreate) -> Document:
    db_obj = Document.model_validate(document_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_document(
    *,
    session: Session,
    db_document: Document,
    document_in: DocumentUpdate,
) -> Document:
    document_data = document_in.model_dump(exclude_unset=True)
    db_document.sqlmodel_update(document_data)
    session.add(db_document)
    session.commit()
    session.refresh(db_document)
    return db_document


def get_documents(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    entity_id: uuid.UUID | None = None,
    entity_type: str | None = None,
) -> list[Document]:
    statement = select(Document)
    if entity_id:
        statement = statement.where(Document.entity_id == entity_id)
    if entity_type:
        statement = statement.where(Document.entity_type == entity_type)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_documents(
    session: Session,
    *,
    entity_id: uuid.UUID | None = None,
    entity_type: str | None = None,
) -> int:
    from sqlmodel import func

    statement = select(Document)
    if entity_id:
        statement = statement.where(Document.entity_id == entity_id)
    if entity_type:
        statement = statement.where(Document.entity_type == entity_type)
    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_document(session: Session, *, db_document: Document) -> None:
    session.delete(db_document)
    session.commit()
