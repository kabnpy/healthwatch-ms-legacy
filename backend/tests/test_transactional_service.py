from datetime import date, timedelta

from sqlmodel import Session

from app.models import PolicyCreate, TransactionType
from app.services.policy import policy_service
from tests.utils.client import create_random_client
from tests.utils.insurance import create_random_product
from tests.utils.utils import random_lower_string


def test_atomic_policy_creation(db: Session) -> None:
    # 1. Setup
    client = create_random_client(db)
    product = create_random_product(db, class_of_insurance="Motor Private")
    policy_number = random_lower_string()

    policy_in = PolicyCreate(
        policy_number=policy_number,
        client_id=client.id,
        product_id=product.id,
    )

    # Singular Semantic Input
    risk_details = {"sum_insured": 5000000, "registration_number": "KCM 123", "make": "Toyota", "year_of_manufacture": 2020}
    start_date = date.today()
    end_date = start_date + timedelta(days=365)

    # Execute
    policy = policy_service.create_policy(
        session=db,
        policy_in=policy_in,
        cover_snapshot=risk_details,
        coverage_start=start_date,
        coverage_end=end_date
    )

    # Verify
    db.refresh(policy)
    assert policy.policy_number == policy_number
    assert len(policy.risk_notes) == 1
    rn = policy.risk_notes[0]
    assert rn.transaction_type == TransactionType.NEW_BUSINESS
    
    # Verify authoritative state on RiskNote snapshot
    assert float(rn.cover_snapshot["vehicle"]["sum_insured"]) == 5000000.0
    assert rn.cover_snapshot["vehicle"]["registration_number"] == "KCM 123"
    
    # Verify RiskNote financials
    assert rn.financial_breakdown["type"] == "motor"
    assert "net_premium" in rn.financial_breakdown
    assert "taxes" in rn.financial_breakdown
    assert "total_amount" in rn.financial_breakdown
    assert "commission_amount" in rn.financial_breakdown
    assert "benefits" in rn.financial_breakdown
    
    # Verify exact math for 5M Motor Private
    # 5M Tier: 3.25% (inclusive of max), min 0
    # 5,000,000 * 0.0325 = 162,500
    assert float(rn.net_premium) == 162500.0
    assert float(rn.financial_breakdown["net_premium"]) == 162500.0
    assert rn.coverage_start == start_date
    assert rn.coverage_end == end_date

def test_endorsement_creation(db: Session) -> None:
    # 1. Setup a policy with one RiskNote
    client = create_random_client(db)
    product = create_random_product(db, class_of_insurance="Motor Private")
    policy_in = PolicyCreate(
        policy_number=random_lower_string(),
        client_id=client.id,
        product_id=product.id,
    )
    start_date = date.today()
    end_date = start_date + timedelta(days=365)
    risk_details = {"sum_insured": 5000000, "registration_number": "KCM 123", "make": "Toyota", "year_of_manufacture": 2020}

    policy = policy_service.create_policy(
        session=db,
        policy_in=policy_in,
        cover_snapshot=risk_details,
        coverage_start=start_date,
        coverage_end=end_date
    )

    # 2. Create Endorsement
    new_risk_details = {"sum_insured": 6000000, "registration_number": "KCM 123", "make": "Toyota", "year_of_manufacture": 2020}
    endorsement_rn = policy_service.create_endorsement(
        session=db,
        policy_id=policy.id,
        updated_cover_snapshot=new_risk_details,
        change_description="Increased vehicle value"
    )

    # 3. Verify
    db.refresh(policy)
    assert len(policy.risk_notes) == 2

    # Verify updated state on RiskNote
    assert float(endorsement_rn.cover_snapshot["vehicle"]["sum_insured"]) == 6000000.0
    
    assert endorsement_rn.transaction_type == TransactionType.ENDORSEMENT

    # Delta logic verification
    assert "new_state" in endorsement_rn.financial_breakdown
    assert "delta" in endorsement_rn.financial_breakdown
    
    # Verify summary fields match deltas
    delta = endorsement_rn.financial_breakdown["delta"]
    assert float(endorsement_rn.net_premium) == float(delta["net_premium"])
    assert float(endorsement_rn.total_amount) == float(delta["total_amount"])
    assert float(endorsement_rn.commission_amount) == float(delta["commission_amount"])
