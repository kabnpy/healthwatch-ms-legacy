from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models import User
from tests.utils.utils import get_superuser_token_headers, random_email


def test_read_documents_auth(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # Test with valid token
    response = client.get(f"{settings.API_V1_STR}/documents/", headers=superuser_token_headers)
    assert response.status_code == 200

    # Test without token
    response = client.get(f"{settings.API_V1_STR}/documents/")
    assert response.status_code == 401


def test_download_document_auth(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # 1. Create a dummy document first
    from app.models import Document, DocumentEntityType, DocumentType
    import uuid
    
    doc = Document(
        entity_type=DocumentEntityType.CLIENT,
        entity_id=uuid.uuid4(),
        document_type=DocumentType.ID,
        file_path="tests/test_file.txt",
        mime_type="text/plain"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # 2. Create the physical file
    from pathlib import Path
    from app.core.storage import storage
    abs_path = storage.get_file_path(doc.file_path)
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    abs_path.write_text("test content")

    # 3. Test download with valid token
    response = client.get(
        f"{settings.API_V1_STR}/documents/{doc.id}/download",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.text == "test content"

    # 4. Test download without token (Should be 401)
    response = client.get(f"{settings.API_V1_STR}/documents/{doc.id}/download")
    assert response.status_code == 401
    
def test_read_risk_note_pdf_auth(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # 1. Create a dummy risk note
    from app.models import RiskNote, Policy, Product, Insurer, Client, TransactionType
    import uuid
    from datetime import date
    from decimal import Decimal

    insurer = Insurer(name=f"Test Insurer {uuid.uuid4()}")
    db.add(insurer)
    db.commit()

    product = Product(name="Test Product", insurer_id=insurer.id, class_of_insurance="Motor Private")
    db.add(product)
    db.commit()

    client_obj = Client(name="Test Client", kra_pin=f"A{uuid.uuid4().hex[:8]}", email=random_email(), phone="123")
    db.add(client_obj)
    db.commit()

    policy = Policy(policy_number=f"POL-{uuid.uuid4()}", client_id=client_obj.id, product_id=product.id)
    db.add(policy)
    db.commit()

    rn = RiskNote(
        policy_id=policy.id,
        transaction_type=TransactionType.NEW_BUSINESS,
        coverage_start=date.today(),
        coverage_end=date.today(),
        net_premium=Decimal("100.00"),
        commission_amount=Decimal("10.00"),
        total_amount=Decimal("110.00"),
        cover_snapshot={
            "VEHICLE": {
                "Reg No": "KDH 519E",
                "Make": "Toyota Hilux",
                "Year": 2020
            },
            "sum_insured": 2700000.00
        }
    )
    db.add(rn)
    db.commit()
    db.refresh(rn)

    # 2. Test PDF generation with valid token
    response = client.get(
        f"{settings.API_V1_STR}/risk-notes/{rn.id}/pdf",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

def test_read_risk_note_pdf_missing_data(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # 1. Create a dummy risk note with missing cover_snapshot data
    from app.models import RiskNote, Policy, Product, Insurer, Client, TransactionType
    import uuid
    from datetime import date
    from decimal import Decimal

    insurer = Insurer(name=f"Test Insurer {uuid.uuid4()}")
    db.add(insurer)
    db.commit()

    product = Product(name="Test Product", insurer_id=insurer.id, class_of_insurance="Motor Private")
    db.add(product)
    db.commit()

    client_obj = Client(name="Test Client", kra_pin=f"A{uuid.uuid4().hex[:8]}", email=random_email(), phone="123")
    db.add(client_obj)
    db.commit()

    policy = Policy(policy_number=f"POL-{uuid.uuid4()}", client_id=client_obj.id, product_id=product.id)
    db.add(policy)
    db.commit()

    rn = RiskNote(
        policy_id=policy.id,
        transaction_type=TransactionType.NEW_BUSINESS,
        coverage_start=date.today(),
        coverage_end=date.today(),
        net_premium=Decimal("100.00"),
        commission_amount=Decimal("10.00"),
        total_amount=Decimal("110.00"),
        cover_snapshot={} # Empty snapshot
    )
    db.add(rn)
    db.commit()
    db.refresh(rn)

    # 2. Test PDF generation should NOT fail with 500
    response = client.get(
        f"{settings.API_V1_STR}/risk-notes/{rn.id}/pdf",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
