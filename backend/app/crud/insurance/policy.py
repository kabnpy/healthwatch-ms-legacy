import uuid
from collections.abc import Sequence
from datetime import date
from decimal import Decimal
from typing import Any, cast

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

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
    from datetime import timedelta

    first_risk_note_in = RiskNoteCreate(
        policy_id=db_obj.id,
        transaction_type="New Business",
        status="Draft",
        start_date=db_obj.start_date or date.today(),
        end_date=db_obj.end_date or (date.today() + timedelta(days=365)),
        net_premium=db_obj.total_premium,  # Default to policy total for draft
        taxes={},
        commission_amount=Decimal("0.0"),
        total_amount=db_obj.total_premium,
        policy_snapshot=jsonable_encoder(db_obj),
        special_clauses=[],
    )
    create_risk_note(session=session, risk_note_in=first_risk_note_in)

    return db_obj


def get_policy(session: Session, *, id: uuid.UUID) -> Policy | None:
    statement = (
        select(Policy)
        .where(Policy.id == id)
        .where(Policy.deleted_at == None)
        .options(
            selectinload(cast(Any, Policy.product)),
        )
    )
    return session.exec(statement).first()


def get_policy_by_policy_number(
    session: Session, *, policy_number: str
) -> Policy | None:
    statement = select(Policy).where(Policy.policy_number == policy_number).where(Policy.deleted_at == None)
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


def create_risk_note(*, session: Session, risk_note_in: RiskNoteCreate) -> RiskNote:
    # 1. Create the Risk Note
    db_obj = RiskNote.model_validate(risk_note_in)

    # Generate unique risk_note_number if not provided
    if not db_obj.risk_note_number:
        db_obj.risk_note_number = f"RSK-{uuid.uuid4().hex[:8].upper()}"

    # Ensure policy_snapshot is populated if not provided
    if not db_obj.policy_snapshot:
        policy = session.get(Policy, db_obj.policy_id)
        if policy:
            db_obj.policy_snapshot = jsonable_encoder(policy)

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
    statement = select(Policy).where(Policy.deleted_at == None).options(selectinload(cast(Any, Policy.product)))
    if client_id:
        statement = statement.where(Policy.client_id == client_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_policies(session: Session, *, client_id: uuid.UUID | None = None) -> int:
    from sqlmodel import func

    statement = select(Policy).where(Policy.deleted_at == None)
    if client_id:
        statement = statement.where(Policy.client_id == client_id)
    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_policy(session: Session, *, db_policy: Policy) -> None:
    db_policy.deleted_at = datetime.now()
    session.add(db_policy)
    session.commit()


def get_claims(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    policy_id: uuid.UUID | None = None,
    client_id: uuid.UUID | None = None,
) -> list[Claim]:
    statement = select(Claim).where(Claim.deleted_at == None)
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

    statement = select(Claim).where(Claim.deleted_at == None)
    if policy_id:
        statement = statement.where(Claim.policy_id == policy_id)
    if client_id:
        statement = statement.join(Policy).where(Policy.client_id == client_id)
    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_claim(session: Session, *, db_claim: Claim) -> None:
    db_claim.deleted_at = datetime.now()
    session.add(db_claim)
    session.commit()


def get_risk_notes(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    policy_id: uuid.UUID | None = None,
    client_id: uuid.UUID | None = None,
    uninvoiced_only: bool = False,
) -> list[RiskNote]:
    statement = select(RiskNote).where(RiskNote.deleted_at == None)
    if policy_id:
        statement = statement.where(RiskNote.policy_id == policy_id)
    if client_id:
        statement = statement.join(Policy).where(Policy.client_id == client_id)
    if uninvoiced_only:
        # A risk note is uninvoiced if it has no invoice_line_items
        # Or more simply, if invoice_number is null (though line items are more robust)
        statement = statement.where(RiskNote.invoice_number is None)
        # Filters out drafts as well since we want to invoice finalized notes
        statement = statement.where(RiskNote.status != "Draft")

    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_risk_notes(
    session: Session,
    *,
    policy_id: uuid.UUID | None = None,
    client_id: uuid.UUID | None = None,
    uninvoiced_only: bool = False,
) -> int:
    from sqlmodel import func

    statement = select(RiskNote).where(RiskNote.deleted_at == None)
    if policy_id:
        statement = statement.where(RiskNote.policy_id == policy_id)
    if client_id:
        statement = statement.join(Policy).where(Policy.client_id == client_id)
    if uninvoiced_only:
        statement = statement.where(RiskNote.invoice_number is None)
        statement = statement.where(RiskNote.status != "Draft")

    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_risk_note(session: Session, *, db_risk_note: RiskNote) -> None:
    db_risk_note.deleted_at = datetime.now()
    session.add(db_risk_note)
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
