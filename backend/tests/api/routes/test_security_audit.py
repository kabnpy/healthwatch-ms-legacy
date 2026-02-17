import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app
from app.models import UserRole
from tests.utils.auth import MockAuth, get_mock_user
from app.core.config import settings

@pytest.fixture
def mock_auth():
    auth = MockAuth(app)
    yield auth
    auth.reset()

def test_read_clients_with_mock_user(
    client: TestClient, mock_auth: MockAuth, db: Session
) -> None:
    # Setup mock user
    mock_user = get_mock_user(role=UserRole.VIEWER)
    mock_auth.mock_user(mock_user)
    
    # Try to read clients
    response = client.get(f"{settings.API_V1_STR}/clients/")
    
    # Should work because read_clients only requires CurrentUser
    assert response.status_code == 200

def test_create_client_with_unauthorized_role(
    client: TestClient, mock_auth: MockAuth, db: Session
) -> None:
    # Setup mock user with Viewer role (not Staff)
    mock_user = get_mock_user(role=UserRole.VIEWER)
    mock_auth.mock_user(mock_user)
    
    data = {
        "full_name": "Test Client",
        "email": "test@client.com",
        "phone": "123456",
        "kra_pin": "A123456789Z"
    }
    
    # Try to create client
    response = client.post(f"{settings.API_V1_STR}/clients/", json=data)
    
    # Should fail with 403 because create_client requires StaffUser
    assert response.status_code == 403

def test_document_endpoints_missing_auth(
    client: TestClient, db: Session
) -> None:
    """
    Audit: Check if document endpoints are properly protected.
    """
    # Try to read documents without token
    response = client.get(f"{settings.API_V1_STR}/documents/")
    
    assert response.status_code == 401

def test_download_document_missing_auth(
    client: TestClient, db: Session
) -> None:
    """
    Audit: Check if download endpoint is protected.
    """
    import uuid
    dummy_id = uuid.uuid4()
    response = client.get(f"{settings.API_V1_STR}/documents/{dummy_id}/download")
    
    assert response.status_code == 401
