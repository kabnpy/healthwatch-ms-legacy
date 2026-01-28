import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils.client import create_random_client
from tests.utils.utils import random_email, random_lower_string


def test_create_client(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "name": random_lower_string(),
        "kra_pin": random_lower_string(),
        "email": random_email(),
        "phone": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/clients/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["kra_pin"] == data["kra_pin"]
    assert "id" in content


def test_read_client(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    db_client = create_random_client(db)
    response = client.get(
        f"{settings.API_V1_STR}/clients/{db_client.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == db_client.name
    assert content["id"] == str(db_client.id)


def test_read_client_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/clients/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Client not found"


def test_read_clients(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_client(db)
    create_random_client(db)
    response = client.get(
        f"{settings.API_V1_STR}/clients/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_client(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    db_client = create_random_client(db)
    data = {"name": "Updated Name", "phone": "0000000000"}
    response = client.put(
        f"{settings.API_V1_STR}/clients/{db_client.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["phone"] == data["phone"]
    assert content["id"] == str(db_client.id)


def test_delete_client(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    db_client = create_random_client(db)
    response = client.delete(
        f"{settings.API_V1_STR}/clients/{db_client.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Client deleted successfully"
