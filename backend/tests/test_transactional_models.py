from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlmodel import Session

from app.models import Policy, PolicyStatus, RiskNote, RiskNoteStatus
from tests.utils.client import create_random_client
from tests.utils.insurance import create_random_product
from tests.utils.utils import random_lower_string


def test_policy_has_no_temporal_state(db: Session) -> None:
    """
    Verify that Policy is a clean identity container without risk_details.
    """
    client = create_random_client(db)
    product = create_random_product(db)

    policy = Policy(
        policy_number=random_lower_string(),
        client_id=client.id,
        product_id=product.id,
        status=PolicyStatus.ACTIVE,
        inception_date=date.today(),
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)

    with pytest.raises(AttributeError):
        _ = policy.risk_details


def test_risknote_chain_and_changelog(db: Session) -> None:
    """
    Verify that RiskNote records the linking and snapshots.
    """
    # 1. Setup base entities
    client = create_random_client(db)
    product = create_random_product(db)

    # 2. Create Policy container
    policy = Policy(
        policy_number=random_lower_string(),
        client_id=client.id,
        product_id=product.id,
        status=PolicyStatus.ACTIVE,
        inception_date=date.today(),
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
        net_premium=Decimal("10000.00"),
        commission_amount=Decimal("1000.00"),
        total_amount=Decimal("10500.00"),
        cover_snapshot={"vehicle": {"value": 1000000}},
    )
    db.add(rn_old)

    # 4. Create latest RiskNote (Renewal)
    new_date = date.today()
    rn_new = RiskNote(
        risk_note_number=random_lower_string(),
        policy_id=policy.id,
        transaction_type="Renewal",
        status=RiskNoteStatus.ISSUED,
        previous_risk_note_id=rn_old.id,
        effective_date=new_date,
        coverage_start=old_date,
        coverage_end=old_date + timedelta(days=364),
        net_premium=Decimal("2000.00"),
        commission_amount=Decimal("200.00"),
        total_amount=Decimal("2100.00"),
        cover_snapshot={"vehicle": {"value": 1200000}},
    )
    db.add(rn_new)

    db.commit()
    db.refresh(rn_new)
    db.refresh(policy)

    # 5. Verify
    assert rn_new.previous_risk_note_id == rn_old.id
    assert rn_new.cover_snapshot["vehicle"]["value"] == 1200000
    assert len(policy.risk_notes) == 2


def test_policy_has_no_duplicated_data(db: Session) -> None:
    """
    Verify that old columns are gone.
    """
    client = create_random_client(db)
    policy = Policy(
        policy_number=random_lower_string(),
        client_id=client.id,
        status=PolicyStatus.ACTIVE,
    )

    # These should NOT be in the __dict__ (representing DB columns)
    assert "risk_details" not in policy.__dict__
    assert "total_premium" not in policy.__dict__
    assert "premium_breakdown" not in policy.__dict__
    assert "start_date" not in policy.__dict__
    assert "end_date" not in policy.__dict__
