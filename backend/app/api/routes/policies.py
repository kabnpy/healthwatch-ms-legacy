import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.crud.insurance.policy import (
    count_policies,
    create_policy as crud_create_policy,
    delete_policy as crud_delete_policy,
    get_policies,
    get_policy_by_policy_number,
)
from app.crud.insurance.policy import (
    update_policy as crud_update_policy,
)
from app.models import (
    Message,
    PoliciesPublic,
    Policy,
    PolicyCreate,
    PolicyPublic,
    PolicyUpdate,
    RiskItemsPublic,
    RiskNotesPublic,
)

router = APIRouter()


@router.get("/", response_model=PoliciesPublic)
def read_policies(
    session: SessionDep,
    _current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    client_id: uuid.UUID | None = None,
) -> Any:
    """
    Retrieve policies.
    """
    count = count_policies(session=session, client_id=client_id)
    policies = get_policies(
        session=session, skip=skip, limit=limit, client_id=client_id
    )
    return PoliciesPublic(data=policies, count=count)


@router.get("/{id}", response_model=PolicyPublic)
def read_policy(session: SessionDep, _current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get policy by ID.
    """
    policy = session.get(Policy, id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


@router.post("/", response_model=PolicyPublic)
def create_policy(
    *, session: SessionDep, _current_user: CurrentUser, policy_in: PolicyCreate
) -> Any:
    """
    Create new policy.
    """
    existing_policy = get_policy_by_policy_number(
        session=session, policy_number=policy_in.policy_number
    )
    if existing_policy:
        raise HTTPException(
            status_code=400,
            detail="The policy with this number already exists in the system.",
        )

    policy = crud_create_policy(session=session, policy_in=policy_in)
    return policy


@router.put("/{id}", response_model=PolicyPublic)
def update_policy(
    *,
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
    policy_in: PolicyUpdate,
) -> Any:
    """
    Update a policy.
    """
    policy = session.get(Policy, id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    policy = crud_update_policy(session=session, db_policy=policy, policy_in=policy_in)
    return policy


@router.delete("/{id}", response_model=Message)
def delete_policy(
    session: SessionDep, _current_user: CurrentUser, id: uuid.UUID
) -> Any:
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
    from app.crud.insurance.policy import count_risk_notes, get_risk_notes

    count = count_risk_notes(session=session, policy_id=id)
    risk_notes = get_risk_notes(session=session, policy_id=id)
    return RiskNotesPublic(data=risk_notes, count=count)


@router.get("/{id}/risk-items", response_model=RiskItemsPublic)
def read_policy_risk_items(
    session: SessionDep, _current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Get risk items for a policy.
    """
    from app.crud.insurance.policy import count_risk_items, get_risk_items

    count = count_risk_items(session=session, policy_id=id)
    risk_items = get_risk_items(session=session, policy_id=id)
    return RiskItemsPublic(data=risk_items, count=count)
