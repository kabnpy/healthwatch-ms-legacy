from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, delete

from app.core.config import settings
from app.core.db import engine, init_db
from app.main import app
from app.models import (
    Item,
    User,
    Insurer,
    Product,
    Client,
    Correspondence,
    Invoice,
    InvoiceLineItem,
    Receipt,
    ReceiptAllocation,
    Policy,
    RiskItem,
    RiskNote,
    Claim,
    PolicyDocument,
)
from tests.utils.user import authentication_token_from_email
from tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        SQLModel.metadata.create_all(engine)
        init_db(session)
        yield session
        # Delete records in correct order to avoid foreign key constraint violations
        statement = delete(PolicyDocument)
        session.execute(statement)
        statement = delete(Claim)
        session.execute(statement)
        statement = delete(ReceiptAllocation)
        session.execute(statement)
        statement = delete(InvoiceLineItem)
        session.execute(statement)
        statement = delete(Receipt)
        session.execute(statement)
        statement = delete(Invoice)
        session.execute(statement)
        statement = delete(RiskItem)
        session.execute(statement)
        statement = delete(RiskNote)
        session.execute(statement)
        statement = delete(Policy)
        session.execute(statement)
        statement = delete(Product)
        session.execute(statement)
        statement = delete(Correspondence)
        session.execute(statement)
        statement = delete(Client)
        session.execute(statement)
        statement = delete(Insurer)
        session.execute(statement)
        statement = delete(Item)
        session.execute(statement)
        statement = delete(User)
        session.execute(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )