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


def update_client(*, session: Session, db_client: Client, client_in: ClientUpdate) -> Client:
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
    *, session: Session, db_correspondence: Correspondence, correspondence_in: CorrespondenceUpdate
) -> Correspondence:
    correspondence_data = correspondence_in.model_dump(exclude_unset=True)
    db_correspondence.sqlmodel_update(correspondence_data)
    session.add(db_correspondence)
    session.commit()
    session.refresh(db_correspondence)
    return db_correspondence