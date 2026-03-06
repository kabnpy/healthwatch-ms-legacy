from datetime import date, timedelta
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import (
    PolicyStatus,
    RiskNote,
    RiskNoteCreate,
    RiskNoteStatus,
    TransactionType,
)
from app.services.renewal import renewal_service
from tests.utils.insurance import create_random_policy


def test_new_policy_statuses_exist():
    # These should exist once implemented
    assert PolicyStatus.RENEWAL_INVITED == "Renewal Invited"
    assert PolicyStatus.RENEWAL_CONFIRMED == "Renewal Confirmed"
    assert PolicyStatus.LAPSED == "Lapsed"

def test_new_risknote_statuses_exist():
    # Maybe we want them here too for the draft notes
    assert RiskNoteStatus.RENEWAL_INVITED == "Renewal Invited"
    assert RiskNoteStatus.RENEWAL_CONFIRMED == "Renewal Confirmed"

def test_get_policies_expiring_exactly_in_days(db: Session):
    # 1. Setup policies
    # Expiring in 30 days
    p30 = create_random_policy(db)
    rn30 = p30.risk_notes[0]
    rn30.coverage_end = date.today() + timedelta(days=30)
    db.add(rn30)

    # Expiring in 7 days
    p7 = create_random_policy(db)
    rn7 = p7.risk_notes[0]
    rn7.coverage_end = date.today() + timedelta(days=7)
    db.add(rn7)

    # Expiring in 31 days (should not be caught)
    p31 = create_random_policy(db)
    rn31 = p31.risk_notes[0]
    rn31.coverage_end = date.today() + timedelta(days=31)
    db.add(rn31)

    db.commit()

    # 2. Test queries
    results_30 = renewal_service.get_policies_expiring_exactly_in(db, days=30)
    assert len(results_30) == 1
    assert results_30[0].id == p30.id

    results_7 = renewal_service.get_policies_expiring_exactly_in(db, days=7)
    assert len(results_7) == 1
    assert results_7[0].id == p7.id

def test_get_policies_expiring_within_days(db: Session):
    # Setup policies (re-using or adding more)
    p15 = create_random_policy(db)
    rn15 = p15.risk_notes[0]
    rn15.coverage_end = date.today() + timedelta(days=15)
    db.add(rn15)
    db.commit()

    # Within 30 days should catch p30, p7, p15 but not p31
    results_within_30 = renewal_service.get_policies_expiring_within(db, days=30)
    # Note: earlier tests might have left data if db is not cleaned,
    # but fixtures usually handle it. Assuming clean db.
    assert len(results_within_30) >= 3

@patch("app.services.renewal.send_email")
def test_send_renewal_invitation(mock_send_email, db: Session):
    policy = create_random_policy(db)
    # Ensure client has email
    policy.client.email = "client@example.com"
    db.add(policy.client)

    # Create the required RENEWAL_INVITED note for the gate
    rn_invite = RiskNote.model_validate(
        RiskNoteCreate(
            policy_id=policy.id,
            transaction_type=TransactionType.RENEWAL,
            status=RiskNoteStatus.RENEWAL_INVITED,
            coverage_start=date.today(),
            coverage_end=date.today() + timedelta(days=365),
            net_premium=100.0,
            commission_amount=10.0,
            total_amount=110.0,
        )
    )
    rn_invite.risk_note_number = "RN-INVITE-TEST"
    db.add(rn_invite)
    db.commit()
    db.refresh(policy)

    renewal_service.send_renewal_invitation(db, policy=policy)

    assert mock_send_email.called
    kwargs = mock_send_email.call_args[1]
    assert kwargs["email_to"] == "client@example.com"
    assert "Renewal Invitation" in kwargs["subject"]
    assert policy.policy_number in kwargs["html_content"]

@patch("app.services.renewal.send_email")
def test_send_renewal_reminder(mock_send_email, db: Session):
    policy = create_random_policy(db)
    policy.client.email = "client@example.com"
    db.add(policy.client)
    db.commit()

    renewal_service.send_renewal_reminder(db, policy=policy)

    assert mock_send_email.called
    assert "Renewal Reminder" in mock_send_email.call_args[1]["subject"]

@patch("app.services.renewal.send_email")
def test_run_daily_renewal_checks(mock_send_email, db: Session):
    # 1. Setup policies
    # Expiring in 30 days
    p30 = create_random_policy(db)
    rn30 = p30.risk_notes[0]
    rn30.coverage_end = date.today() + timedelta(days=30)
    db.add(rn30)

    # Create the required RENEWAL_INVITED note for p30
    rn_invite = RiskNote.model_validate(
        RiskNoteCreate(
            policy_id=p30.id,
            transaction_type=TransactionType.RENEWAL,
            status=RiskNoteStatus.RENEWAL_INVITED,
            coverage_start=rn30.coverage_end,
            coverage_end=rn30.coverage_end + timedelta(days=365),
            net_premium=100.0,
            commission_amount=10.0,
            total_amount=110.0,
        )
    )
    rn_invite.risk_note_number = "RN-INVITE-P30"
    db.add(rn_invite)

    # Expiring in 7 days
    p7 = create_random_policy(db)
    rn7 = p7.risk_notes[0]
    rn7.coverage_end = date.today() + timedelta(days=7)
    db.add(rn7)

    db.commit()
    db.refresh(p30)

    # 2. Run checks
    renewal_service.run_daily_renewal_checks(db)

    # 3. Verify
    # Extract all HTML contents from mock calls
    sent_htmls = [call.kwargs["html_content"] for call in mock_send_email.call_args_list]

    # Verify our specific policies were notified
    assert any(p30.policy_number in html for html in sent_htmls)
    assert any(p7.policy_number in html for html in sent_htmls)

    # Verify status transition
    db.refresh(p30)
    assert p30.status == PolicyStatus.RENEWAL_INVITED

def test_read_policies_expiring_soon(client: "TestClient", superuser_token_headers: dict, db: Session):
    # 1. Setup policies
    p_soon = create_random_policy(db)
    rn = p_soon.risk_notes[0]
    rn.coverage_end = date.today() + timedelta(days=10)
    db.add(rn)

    p_far = create_random_policy(db)
    rn_far = p_far.risk_notes[0]
    rn_far.coverage_end = date.today() + timedelta(days=40)
    db.add(rn_far)

    db.commit()

    # 2. Call API
    from app.core.config import settings
    response = client.get(
        f"{settings.API_V1_STR}/policies/?expiring_within=30",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # 3. Verify
    policy_ids = [p["id"] for p in data["data"]]
    assert str(p_soon.id) in policy_ids
    assert str(p_far.id) not in policy_ids
