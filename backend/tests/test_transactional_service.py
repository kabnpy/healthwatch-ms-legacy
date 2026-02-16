import uuid
from datetime import date, timedelta
from decimal import Decimal
from sqlmodel import Session, select
from app.models import Policy, RiskNote, PolicyStatus, RiskNoteStatus, PolicyCreate, TransactionType
from app.services.policy import policy_service
from tests.utils.utils import random_lower_string
from tests.utils.client import create_random_client
from tests.utils.insurance import create_random_product

def test_atomic_policy_creation(db: Session) -> None:
    # 1. Setup
    client = create_random_client(db)
    product = create_random_product(db)
    policy_number = random_lower_string()
    
    policy_in = PolicyCreate(
        policy_number=policy_number,
        client_id=client.id,
        product_id=product.id,
    )
    
    # Mocking fields that should go to RiskNote
    risk_details = {"VEHICLE DETAILS": {"Value Kshs.": 5000000, "Reg. No": "KCM 123", "Make": "Toyota", "Year": 2020}}
    start_date = date.today()
    end_date = start_date + timedelta(days=365)
    
    # Execute (Service should be refactored to handle this)
    policy = policy_service.create_policy(
        session=db, 
        policy_in=policy_in,
        risk_details=risk_details,
        coverage_start=start_date,
        coverage_end=end_date
    )
    
    # Verify
    db.refresh(policy)
    assert policy.policy_number == policy_number
    assert len(policy.risk_notes) == 1
    rn = policy.risk_notes[0]
    assert rn.transaction_type == TransactionType.NEW_BUSINESS
    assert rn.policy_snapshot["risk_details"] == risk_details
    assert rn.coverage_start == start_date
    assert rn.coverage_end == end_date
    assert policy.current_risk_details == risk_details

def test_endorsement_creation(db: Session) -> None:
    # 1. Setup a policy with one RiskNote
    client = create_random_client(db)
    product = create_random_product(db)
    policy_in = PolicyCreate(
        policy_number=random_lower_string(),
        client_id=client.id,
        product_id=product.id,
    )
    start_date = date.today()
    end_date = start_date + timedelta(days=365)
    risk_details = {"VEHICLE DETAILS": {"Value Kshs.": 5000000, "Reg. No": "KCM 123", "Make": "Toyota", "Year": 2020}}
    
    policy = policy_service.create_policy(
        session=db, 
        policy_in=policy_in,
        risk_details=risk_details,
        coverage_start=start_date,
        coverage_end=end_date
    )
    
    # 2. Create Endorsement
    new_risk_details = {"VEHICLE DETAILS": {"Value Kshs.": 6000000, "Reg. No": "KCM 123", "Make": "Toyota", "Year": 2020}}
    endorsement_rn = policy_service.create_endorsement(
        session=db,
        policy_id=policy.id,
        updated_risk_details=new_risk_details,
        change_description="Increased vehicle value"
    )
    
    # 3. Verify
    db.refresh(policy)
    assert len(policy.risk_notes) == 2
    
    # Sort locally to verify logic
    sorted_notes = sorted(policy.risk_notes, key=lambda x: (x.effective_date, x.created_at), reverse=True)
    assert sorted_notes[0].id == endorsement_rn.id
    
    assert policy.current_risk_note.id == endorsement_rn.id
    assert policy.current_risk_details == new_risk_details
    assert endorsement_rn.transaction_type == TransactionType.ENDORSEMENT
    assert endorsement_rn.policy_snapshot["changes"]["description"] == "Increased vehicle value"
