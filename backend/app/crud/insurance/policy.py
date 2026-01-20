import uuid
from collections.abc import Sequence

from sqlmodel import Session, select

from app.models.insurance.policy import (
    Claim,
    ClaimCreate,
    ClaimUpdate,
    Policy,
    PolicyCreate,
    PolicyDocument,
    PolicyDocumentCreate,
    PolicyDocumentUpdate,
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
    return db_obj


def get_policy_by_policy_number(session: Session, *, policy_number: str) -> Policy | None:
    statement = select(Policy).where(Policy.policy_number == policy_number)
    return session.exec(statement).first()


def get_policies_by_client_id(
    session: Session, *, client_id: uuid.UUID
) -> Sequence[Policy]:
    statement = select(Policy).where(Policy.client_id == client_id)
    return session.exec(statement).all()


def update_policy(*, session: Session, db_policy: Policy, policy_in: PolicyUpdate) -> Policy:
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


def get_risk_item_by_identifier(session: Session, *, identifier: str) -> RiskItem | None:
    statement = select(RiskItem).where(RiskItem.identifier == identifier)
    return session.exec(statement).first()


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
    db_obj = RiskNote.model_validate(risk_note_in)
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


def create_policy_document(
    *, session: Session, policy_document_in: PolicyDocumentCreate
) -> PolicyDocument:
    db_obj = PolicyDocument.model_validate(policy_document_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_policy_document(
    *,
    session: Session,
    db_policy_document: PolicyDocument,
    policy_document_in: PolicyDocumentUpdate,
) -> PolicyDocument:
    policy_document_data = policy_document_in.model_dump(exclude_unset=True)
    db_policy_document.sqlmodel_update(policy_document_data)
    session.add(db_policy_document)
    session.commit()
    session.refresh(db_policy_document)
    return db_policy_document