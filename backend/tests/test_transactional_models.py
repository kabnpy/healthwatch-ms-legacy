import uuid
from datetime import date, timedelta
from decimal import Decimal
from sqlmodel import Session
from app.models import Policy, RiskNote, PolicyStatus, RiskNoteStatus
from tests.utils.utils import random_lower_string
from tests.utils.client import create_random_client
from tests.utils.insurance import create_random_product

def test_policy_computed_properties(db: Session) -> None:
    # 1. Setup base entities
    client = create_random_client(db)
    product = create_random_product(db)
    
    # 2. Create Policy container
    policy = Policy(
        policy_number=random_lower_string(),
        client_id=client.id,
        product_id=product.id,
        status=PolicyStatus.ACTIVE,
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    
    # 3. Create historical RiskNote
    old_date = date.today() - timedelta(days=365)
    rn_old = RiskNote(
        risk_note_number=random_lower_string(),
        policy_id=policy.id,
        transaction_type="New Business",
        status=RiskNoteStatus.ISSUED,
        effective_date=old_date,
        coverage_start=old_date,
        coverage_end=old_date + timedelta(days=364),
        policy_snapshot={
            "risk_details": {"vehicle": {"value": 1000000}}
        },
        net_premium=Decimal("10000.00"),
        commission_amount=Decimal("1000.00"),
        total_amount=Decimal("10500.00"),
    )
    db.add(rn_old)
    
    # 4. Create latest RiskNote
    new_date = date.today()
    rn_new = RiskNote(
        risk_note_number=random_lower_string(),
        policy_id=policy.id,
        transaction_type="Endorsement",
        status=RiskNoteStatus.ISSUED,
        effective_date=new_date,
        coverage_start=old_date,
        coverage_end=old_date + timedelta(days=364),
        policy_snapshot={
            "risk_details": {"vehicle": {"value": 1200000}}
        },
        net_premium=Decimal("2000.00"),
        commission_amount=Decimal("200.00"),
        total_amount=Decimal("2100.00"),
    )
    db.add(rn_new)
    db.commit()
    db.refresh(policy)
    
    # 5. Verify computed properties
    assert policy.current_risk_note.id == rn_new.id
    assert policy.current_risk_details["vehicle"]["value"] == 1200000
    assert policy.current_premium == Decimal("2100.00")
    assert policy.current_term_start == old_date

def test_policy_has_no_duplicated_data(db: Session) -> None:
    # This test verifies that we've removed the old columns
    client = create_random_client(db)
    policy = Policy(
        policy_number=random_lower_string(),
        client_id=client.id,
        status=PolicyStatus.ACTIVE,
    )
    
    # These should raise AttributeError if columns are removed
    try:
        val = getattr(policy, "risk_details")
        assert False, "Policy should not have risk_details attribute"
    except AttributeError:
        pass
        
    try:
        val = getattr(policy, "total_premium")
        assert False, "Policy should not have total_premium attribute"
    except AttributeError:
        pass
