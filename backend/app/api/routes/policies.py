import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Response

from app.api.deps import CurrentUser, SessionDep, StaffUser
from app.api.utils import prepare_policy_public
from app.crud import (
    count_policies,
    get_policies,
    get_policy,
    get_policy_by_policy_number,
)
from app.crud import (
    delete_policy as crud_delete_policy,
)
from app.crud import (
    update_policy as crud_update_policy,
)
from app.models import (
    Message,
    PoliciesPublic,
    Policy,
    PolicyCreateExtended,
    PolicyPublic,
    PolicyUpdate,
    Product,
    RiskNotesPublic,
    RiskNoteStatus,
)
from app.schemas import QuoteRequest, QuoteResponse
from app.services.document_service import (
    generate_renewal_invitation_html,
    generate_renewal_invitation_pdf,
)
from app.services.policy import policy_service
from app.services.product import product_service
from app.services.rating import RatingService

router = APIRouter()


@router.get("/", response_model=PoliciesPublic)
def read_policies(
    session: SessionDep,
    _current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    client_id: uuid.UUID | None = None,
    expiring_within: int | None = None,
) -> Any:
    """
    Retrieve policies.
    """
    count = count_policies(
        session=session, client_id=client_id, expiring_within=expiring_within
    )
    policies = get_policies(
        session=session,
        skip=skip,
        limit=limit,
        client_id=client_id,
        expiring_within=expiring_within,
    )
    return PoliciesPublic(
        data=[prepare_policy_public(p) for p in policies], count=count
    )


@router.get("/{id}", response_model=PolicyPublic)
def read_policy(session: SessionDep, _current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get policy by ID.
    """
    policy = get_policy(session=session, id=id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return prepare_policy_public(policy)


@router.post("/quote", response_model=QuoteResponse)
def get_policy_quote(
    *,
    session: SessionDep,
    _current_user: CurrentUser,
    quote_in: QuoteRequest,
) -> Any:
    """
    Get a non-persistent premium quote breakdown.
    """
    product = session.get(Product, quote_in.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        validated_risk = product_service.validate_risk_details(
            product, quote_in.risk_details
        )
        breakdown = RatingService.calculate_breakdown(product, validated_risk)
        return QuoteResponse(breakdown=breakdown)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=PolicyPublic)
def create_policy(
    *, session: SessionDep, current_user: StaffUser, policy_in: PolicyCreateExtended
) -> Any:
    """
    Create new policy with initial risk note.
    """
    existing_policy = get_policy_by_policy_number(
        session=session, policy_number=policy_in.policy_number
    )
    if existing_policy:
        raise HTTPException(
            status_code=400,
            detail="The policy with this number already exists in the system.",
        )

    policy = policy_service.create_policy(
        session=session,
        policy_in=policy_in,
        cover_snapshot=policy_in.risk_details,
        coverage_start=policy_in.coverage_start,
        coverage_end=policy_in.coverage_end,
        current_user_id=current_user.id,
    )
    session.commit()
    session.refresh(policy)
    return prepare_policy_public(policy)


@router.put("/{id}", response_model=PolicyPublic)
def update_policy(
    *,
    session: SessionDep,
    _current_user: StaffUser,
    id: uuid.UUID,
    policy_in: PolicyUpdate,
) -> Any:
    """
    Update a policy container.
    """
    policy = session.get(Policy, id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    policy = crud_update_policy(session=session, db_policy=policy, policy_in=policy_in)
    return prepare_policy_public(policy)


@router.delete("/{id}", response_model=Message)
def delete_policy(session: SessionDep, _current_user: StaffUser, id: uuid.UUID) -> Any:
    """
    Delete a policy.
    """
    policy = session.get(Policy, id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    crud_delete_policy(session=session, db_policy=policy)
    return Message(message="Policy deleted successfully")


@router.get("/{id}/risk-notes", response_model=RiskNotesPublic)
def read_policy_risk_notes(
    session: SessionDep, _current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Get risk notes for a policy.
    """
    from app.crud import count_risk_notes, get_risk_notes

    count = count_risk_notes(session=session, policy_id=id)
    risk_notes = get_risk_notes(session=session, policy_id=id)
    return RiskNotesPublic(data=risk_notes, count=count)


@router.get("/{id}/renewal-invitation/pdf")
def read_policy_renewal_invitation_pdf(
    session: SessionDep, _current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Generate and return Renewal Invitation as PDF.
    """
    policy = session.get(Policy, id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    # Find the renewal invited risk note
    renewal_rn = next(
        (rn for rn in policy.risk_notes if rn.status == RiskNoteStatus.RENEWAL_INVITED),
        None,
    )
    if not renewal_rn:
        raise HTTPException(
            status_code=400,
            detail="No 'Renewal Invited' risk note found for this policy.",
        )

    pdf_bytes = generate_renewal_invitation_pdf(
        risk_note=renewal_rn, client=policy.client, policy=policy
    )

    filename = f"Renewal_Invitation_{policy.policy_number}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/{id}/renewal-invitation/html")
def read_policy_renewal_invitation_html(
    session: SessionDep, _current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Generate and return Renewal Invitation as HTML.
    """
    policy = session.get(Policy, id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    # Find the renewal invited risk note
    renewal_rn = next(
        (rn for rn in policy.risk_notes if rn.status == RiskNoteStatus.RENEWAL_INVITED),
        None,
    )
    if not renewal_rn:
        raise HTTPException(
            status_code=400,
            detail="No 'Renewal Invited' risk note found for this policy.",
        )

    html_content = generate_renewal_invitation_html(
        risk_note=renewal_rn, client=policy.client, policy=policy
    )

    return Response(content=html_content, media_type="text/html")


@router.post("/{id}/send-renewal-invitation", response_model=Message)
def send_policy_renewal_invitation(
    session: SessionDep, _current_user: StaffUser, id: uuid.UUID
) -> Any:
    """
    Manually trigger a renewal invitation email.
    """
    policy = get_policy(session=session, id=id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    from app.services.renewal import renewal_service

    try:
        renewal_service.send_renewal_invitation(session, policy=policy)
        session.commit()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return Message(message="Renewal invitation sent successfully")


@router.post("/{id}/send-renewal-reminder", response_model=Message)
def send_policy_renewal_reminder(
    session: SessionDep, _current_user: StaffUser, id: uuid.UUID
) -> Any:
    """
    Manually trigger a renewal reminder email.
    """
    policy = get_policy(session=session, id=id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    from app.services.renewal import renewal_service

    renewal_service.send_renewal_reminder(session, policy=policy)
    session.commit()

    return Message(message="Renewal reminder sent successfully")
