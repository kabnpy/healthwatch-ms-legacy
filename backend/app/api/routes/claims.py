import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.crud.insurance.policy import (
    create_claim as crud_create_claim,
)
from app.crud.insurance.policy import (
    update_claim as crud_update_claim,
)
from app.models import (
    Claim,
    ClaimCreate,
    ClaimPublic,
    ClaimsPublic,
    ClaimUpdate,
    Message,
)

router = APIRouter()


@router.get("/", response_model=ClaimsPublic)
def read_claims(
    session: SessionDep, _current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve claims.
    """
    count_statement = select(func.count()).select_from(Claim)
    count = session.exec(count_statement).one()
    statement = select(Claim).offset(skip).limit(limit)
    claims = session.exec(statement).all()
    return ClaimsPublic(data=claims, count=count)


@router.get("/{id}", response_model=ClaimPublic)
def read_claim(session: SessionDep, _current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get claim by ID.
    """
    claim = session.get(Claim, id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim


@router.post("/", response_model=ClaimPublic)
def create_claim(
    *, session: SessionDep, _current_user: CurrentUser, claim_in: ClaimCreate
) -> Any:
    """
    Create new claim.
    """
    claim = crud_create_claim(session=session, claim_in=claim_in)
    return claim


@router.put("/{id}", response_model=ClaimPublic)
def update_claim(
    *,
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
    claim_in: ClaimUpdate,
) -> Any:
    """
    Update a claim.
    """
    claim = session.get(Claim, id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    claim = crud_update_claim(session=session, db_claim=claim, claim_in=claim_in)
    return claim


@router.delete("/{id}", response_model=Message)
def delete_claim(session: SessionDep, _current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Delete a claim.
    """
    claim = session.get(Claim, id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    session.delete(claim)
    session.commit()
    return Message(message="Claim deleted successfully")
