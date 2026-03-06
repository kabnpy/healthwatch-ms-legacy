import uuid

from sqlmodel import Session, func, select

from app.models import (
    Document,
    DocumentCreate,
    DocumentEntityType,
    DocumentUpdate,
)


def create_document(*, session: Session, document_in: DocumentCreate) -> Document:
    update_data = {}
    if document_in.entity_type == DocumentEntityType.CLIENT:
        update_data["client_id"] = document_in.entity_id
    elif document_in.entity_type == DocumentEntityType.POLICY:
        update_data["policy_id"] = document_in.entity_id
    elif document_in.entity_type == DocumentEntityType.CLAIM:
        update_data["claim_id"] = document_in.entity_id
    elif document_in.entity_type == DocumentEntityType.RISK_NOTE:
        update_data["risk_note_id"] = document_in.entity_id

    db_obj = Document.model_validate(document_in, update=update_data)
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
