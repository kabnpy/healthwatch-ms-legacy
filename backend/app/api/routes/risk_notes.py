import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Response

from app.api.deps import CurrentUser, SessionDep, StaffUser
from app.crud import (
    count_risk_notes,
    get_risk_notes,
)
from app.crud import (
    delete_risk_note as crud_delete_risk_note,
)
from app.crud import (
    update_risk_note as crud_update_risk_note,
)
from app.models import (
    Message,
    RiskNote,
    RiskNoteCreate,
    RiskNotePublic,
    RiskNotesPublic,
    RiskNoteUpdate,
)
from app.services.document_service import generate_risknote_pdf
from app.services.policy import policy_service

router = APIRouter()


@router.get("/", response_model=RiskNotesPublic)
def read_risk_notes(
    session: SessionDep,
    _current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    policy_id: uuid.UUID | None = None,
    client_id: uuid.UUID | None = None,
    uninvoiced_only: bool = False,
) -> Any:
    """
    Retrieve risk notes.
    """
    count = count_risk_notes(
        session=session,
        policy_id=policy_id,
        client_id=client_id,
        uninvoiced_only=uninvoiced_only,
    )
    risk_notes = get_risk_notes(
        session=session,
        skip=skip,
        limit=limit,
        policy_id=policy_id,
        client_id=client_id,
        uninvoiced_only=uninvoiced_only,
    )
    return RiskNotesPublic(data=risk_notes, count=count)


@router.get("/{id}", response_model=RiskNotePublic)
def read_risk_note(
    session: SessionDep, _current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Get risk note by ID.
    """
    risk_note = session.get(RiskNote, id)
    if not risk_note:
        raise HTTPException(status_code=404, detail="Risk note not found")
    return risk_note


@router.get("/{id}/pdf")
def read_risk_note_pdf(
    session: SessionDep, _current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Generate and return Risk Note as PDF.
    """
    risk_note = session.get(RiskNote, id)
    if not risk_note:
        raise HTTPException(status_code=404, detail="Risk note not found")

    # Get associated policy and client
    policy = risk_note.policy
    client = policy.client

    # Check if there's an invoice
    invoice = None
    if risk_note.invoice_line_items:
        invoice = risk_note.invoice_line_items[0].invoice

    pdf_bytes = generate_risknote_pdf(
        risk_note=risk_note,
        client=client,
        policy=policy,
        invoice=invoice
    )

    filename = f"RiskNote_{risk_note.risk_note_number or str(id)}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/", response_model=RiskNotePublic)
def create_risk_note(
    *, session: SessionDep, _current_user: StaffUser, risk_note_in: RiskNoteCreate
) -> Any:
    """
    Create new risk note.
    """
    risk_note = policy_service.create_risk_note(
        session=session, risk_note_in=risk_note_in, created_by_id=_current_user.id
    )
    return risk_note


@router.put("/{id}", response_model=RiskNotePublic)
def update_risk_note(
    *,
    session: SessionDep,
    _current_user: StaffUser,
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
    session: SessionDep, _current_user: StaffUser, id: uuid.UUID
) -> Any:
    """
    Delete a risk note.
    """
    risk_note = session.get(RiskNote, id)
    if not risk_note:
        raise HTTPException(status_code=404, detail="Risk note not found")
    crud_delete_risk_note(session=session, db_risk_note=risk_note)
    return Message(message="Risk note deleted successfully")
