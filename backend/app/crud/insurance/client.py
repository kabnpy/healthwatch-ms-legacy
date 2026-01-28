import uuid

from sqlmodel import Session, select

from app.models.insurance.client import (
    Client,
    ClientCreate,
    ClientUpdate,
    Correspondence,
    CorrespondenceCreate,
    CorrespondenceUpdate,
)


def create_client(*, session: Session, client_in: ClientCreate) -> Client:
    db_obj = Client.model_validate(client_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_client_by_kra_pin(session: Session, *, kra_pin: str) -> Client | None:
    statement = select(Client).where(Client.kra_pin == kra_pin)
    return session.exec(statement).first()


def get_client_by_email(session: Session, *, email: str) -> Client | None:
    statement = select(Client).where(Client.email == email)
    return session.exec(statement).first()


def update_client(
    *, session: Session, db_client: Client, client_in: ClientUpdate
) -> Client:
    client_data = client_in.model_dump(exclude_unset=True)
    db_client.sqlmodel_update(client_data)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client


def create_correspondence(
    *, session: Session, correspondence_in: CorrespondenceCreate
) -> Correspondence:
    db_obj = Correspondence.model_validate(correspondence_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_correspondence(
    *,
    session: Session,
    db_correspondence: Correspondence,
    correspondence_in: CorrespondenceUpdate,
) -> Correspondence:
    correspondence_data = correspondence_in.model_dump(exclude_unset=True)
    db_correspondence.sqlmodel_update(correspondence_data)
    session.add(db_correspondence)
    session.commit()
    session.refresh(db_correspondence)
    return db_correspondence


def get_clients(session: Session, *, skip: int = 0, limit: int = 100) -> list[Client]:
    statement = select(Client).offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_clients(session: Session) -> int:
    from sqlmodel import func

    statement = select(func.count()).select_from(Client)
    return session.exec(statement).one()


def delete_client(session: Session, *, db_client: Client) -> None:
    session.delete(db_client)
    session.commit()


def get_correspondences(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    client_id: uuid.UUID | None = None,
) -> list[Correspondence]:
    statement = select(Correspondence)
    if client_id:
        statement = statement.where(Correspondence.client_id == client_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_correspondences(
    session: Session, *, client_id: uuid.UUID | None = None
) -> int:
    from sqlmodel import func

    statement = select(Correspondence)
    if client_id:
        statement = statement.where(Correspondence.client_id == client_id)
    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_correspondence(
    session: Session, *, db_correspondence: Correspondence
) -> None:
    session.delete(db_correspondence)
    session.commit()
