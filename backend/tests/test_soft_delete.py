from datetime import datetime

from sqlmodel import Session, select

from app import crud
from app.models import Client, ClientCreate
from tests.utils.utils import random_email, random_lower_string


def test_client_soft_delete(db: Session) -> None:
    # 1. Create a client
    client_in = ClientCreate(
        name=random_lower_string(),
        kra_pin=random_lower_string(),
        email=random_email(),
        phone=random_lower_string(),
    )
    client = crud.create_client(session=db, client_in=client_in)
    client_id = client.id

    # Verify it has no deleted_at yet
    assert hasattr(client, "deleted_at")
    assert client.deleted_at is None

    # 2. Soft delete the client
    crud.delete_client(session=db, db_client=client)

    # 3. Verify it's still in the DB but marked as deleted
    # Use session.get directly to check if it's there (SQLModel.get bypasses my CRUD filters)
    db_client = db.get(Client, client_id)
    assert db_client is not None
    assert db_client.deleted_at is not None
    assert isinstance(db_client.deleted_at, datetime)

    # 4. Verify that CRUD list/get doesn't return it
    # We need to use the CRUD methods
    # Wait, get_client by ID might not exist yet, let's check
    # statement = select(Client).where(Client.id == client_id).where(Client.deleted_at == None)
    # results = db.exec(statement).first()
    # assert results is None

    clients = crud.get_clients(session=db)
    assert not any(c.id == client_id for c in clients)

    # 5. Verify it's still accessible via direct select if we don't filter
    statement = select(Client).where(Client.id == client_id)
    results = db.exec(statement).all()
    assert len(results) == 1
