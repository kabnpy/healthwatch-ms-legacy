import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser, SessionDep
from app.crud.insurance.policy import (
    count_risk_notes,
    create_risk_note as crud_create_risk_note,
    delete_risk_note as crud_delete_risk_note,
    get_risk_notes,
    update_risk_note as crud_update_risk_note,
)
from app.models import (
    Message,
    RiskNote,
    RiskNoteCreate,
    RiskNotePublic,
    RiskNoteUpdate,
    RiskNotesPublic,
)

router = APIRouter()


@router.get("/", response_model=RiskNotesPublic)
def read_risk_notes(
    session: SessionDep,
    _current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    policy_id: uuid.UUID | None = None,
) -> Any:
    """
    Retrieve risk notes.
    """
    count = count_risk_notes(session=session, policy_id=policy_id)
    risk_notes = get_risk_notes(session=session, skip=skip, limit=limit, policy_id=policy_id)
    return RiskNotesPublic(data=risk_notes, count=count)


@router.get("/{id}", response_model=RiskNotePublic)
def read_risk_note(session: SessionDep, _current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get risk note by ID.
    """
    risk_note = session.get(RiskNote, id)
    if not risk_note:
        raise HTTPException(status_code=404, detail="Risk note not found")
    return risk_note


@router.post("/", response_model=RiskNotePublic)
def create_risk_note(
    *, session: SessionDep, _current_user: CurrentUser, risk_note_in: RiskNoteCreate
) -> Any:
    """
    Create new risk note.
    """
    risk_note = crud_create_risk_note(session=session, risk_note_in=risk_note_in)
    return risk_note


@router.put("/{id}", response_model=RiskNotePublic)
def update_risk_note(
    *,
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
    risk_note_in: RiskNoteUpdate,
) -> Any:
    """
    Update a risk note.
    """
    risk_note = session.get(RiskNote, id)
    if not risk_note:
        raise HTTPException(status_code=404, detail="Risk note not found")

    risk_note = crud_update_risk_note(
        session=session, db_risk_note=risk_note, risk_note_in=risk_note_in
    )
    return risk_note


@router.delete("/{id}", response_model=Message)
def delete_risk_note(
    session: SessionDep, _current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Delete a risk note.
    """
    risk_note = session.get(RiskNote, id)
    if not risk_note:
        raise HTTPException(status_code=404, detail="Risk note not found")
    crud_delete_risk_note(session=session, db_risk_note=risk_note)
    return Message(message="Risk note deleted successfully")
