import uuid
from datetime import date
from decimal import Decimal
import pytest
from sqlmodel import Session
from app.models import Policy, RiskNote, PolicyStatus, RiskNoteStatus, TransactionType, Client, Product, Insurer, PolicyCreate
from app.services.policy import policy_service

def test_create_policy_atomic_snapshot(db: Session) -> None:
    """
    Test that PolicyService.create_policy creates an atomic snapshot in the first RiskNote.
    """
    insurer = Insurer(name="Service Insurer")
    db.add(insurer)
    db.commit()
    
    product = Product(
        name="Service Product",
        class_of_insurance="Motor Private",
        insurer_id=insurer.id,
        pricing_rules={"tiers": []}
    )
    db.add(product)
    db.commit()

    client = Client(
        name="Service Client",
        kra_pin="S111111111Z",
        phone="0711111111"
    )
    db.add(client)
    db.commit()

    cover_data = {
        "vehicle": {
            "registration_number": "KBA 001",
            "make": "Toyota",
            "sum_insured": 1000000
        },
        "extensions": {"pvt": True},
        "terms": {
            "benefits_and_limits": "Included",
            "excesses": "Standard",
            "special_clauses": "None"
        }
    }

    policy_in = PolicyCreate(
        policy_number="POL-SRV-001",
        client_id=client.id,
        product_id=product.id,
        status=PolicyStatus.ACTIVE,
        inception_date=date.today()
    )

    policy = policy_service.create_policy(
        session=db,
        policy_in=policy_in,
        cover_snapshot=cover_data,
        coverage_start=date.today(),
        coverage_end=date.today()
    )
    db.commit()
    db.refresh(policy)

    assert len(policy.risk_notes) == 1
    snapshot = policy.risk_notes[0].cover_snapshot
    assert snapshot["vehicle"]["registration_number"] == "KBA 001"
    assert snapshot["vehicle"]["sum_insured"] in [1000000, "1000000", Decimal("1000000")]
    assert snapshot["extensions"]["pvt"] is True
    assert snapshot["terms"]["benefits_and_limits"] == "Included"
    
    assert policy.risk_notes[0].transaction_type == TransactionType.NEW_BUSINESS
