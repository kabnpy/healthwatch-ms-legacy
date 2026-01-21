import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.crud.insurance.catalog import (
    count_insurers,
    create_insurer as crud_create_insurer,
    delete_insurer as crud_delete_insurer,
    get_insurer_by_name,
    get_insurers,
)
from app.crud.insurance.catalog import (
    update_insurer as crud_update_insurer,
)
from app.models import (
    Insurer,
    InsurerCreate,
    InsurerPublic,
    InsurersPublic,
    InsurerUpdate,
    Message,
)

router = APIRouter()


@router.get("/", response_model=InsurersPublic)
def read_insurers(
    session: SessionDep, _current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve insurers.
    """
    count = count_insurers(session=session)
    insurers = get_insurers(session=session, skip=skip, limit=limit)
    return InsurersPublic(data=insurers, count=count)


@router.get("/{id}", response_model=InsurerPublic)
def read_insurer(session: SessionDep, _current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get insurer by ID.
    """
    insurer = session.get(Insurer, id)
    if not insurer:
        raise HTTPException(status_code=404, detail="Insurer not found")
    return insurer


@router.post("/", response_model=InsurerPublic)
def create_insurer(
    *, session: SessionDep, _current_user: CurrentUser, insurer_in: InsurerCreate
) -> Any:
    """
    Create new insurer.
    """
    existing_insurer = get_insurer_by_name(session=session, name=insurer_in.name)
    if existing_insurer:
        raise HTTPException(
            status_code=400,
            detail="The insurer with this name already exists in the system.",
        )

    insurer = crud_create_insurer(session=session, insurer_in=insurer_in)
    return insurer


@router.put("/{id}", response_model=InsurerPublic)
def update_insurer(
    *,
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
    insurer_in: InsurerUpdate,
) -> Any:
    """
    Update an insurer.
    """
    insurer = session.get(Insurer, id)
    if not insurer:
        raise HTTPException(status_code=404, detail="Insurer not found")

    insurer = crud_update_insurer(
        session=session, db_insurer=insurer, insurer_in=insurer_in
    )
    return insurer


@router.delete("/{id}", response_model=Message)
def delete_insurer(
    session: SessionDep, _current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Delete an insurer.
    """
    insurer = session.get(Insurer, id)
    if not insurer:
        raise HTTPException(status_code=404, detail="Insurer not found")
    crud_delete_insurer(session=session, db_insurer=insurer)
    return Message(message="Insurer deleted successfully")
