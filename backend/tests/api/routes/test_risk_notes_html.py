import uuid
from datetime import date
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models import (
    Client,
    Insurer,
    Policy,
    Product,
    RiskNote,
    TransactionType,
)
from tests.utils.utils import random_email


def test_read_risk_note_html(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # 1. Setup Data
    insurer = Insurer(name=f"Test Insurer {uuid.uuid4()}")
    db.add(insurer)
    db.commit()

    product = Product(
        name="Test Product", insurer_id=insurer.id, class_of_insurance="Motor Private"
    )
    db.add(product)
    db.commit()

    client_obj = Client(
        name="Test Client",
        kra_pin=f"A{uuid.uuid4().hex[:8]}",
        email=random_email(),
        phone="123",
    )
    db.add(client_obj)
    db.commit()

    policy = Policy(
        policy_number=f"POL-{uuid.uuid4()}",
        client_id=client_obj.id,
        product_id=product.id,
    )
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
        cover_snapshot={"VEHICLE": {"Reg No": "KAA 123A"}},
    )
    db.add(rn)
    db.commit()
    db.refresh(rn)

    # 2. Test HTML retrieval
    response = client.get(
        f"{settings.API_V1_STR}/risk-notes/{rn.id}/html",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "KAA 123A" in response.text
    assert "RISK NOTE" in response.text
