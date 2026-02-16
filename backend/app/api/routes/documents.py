import json
import uuid
from pathlib import Path
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.api.deps import SessionDep, StaffUser
from app.core.storage import storage
from app.crud.policy import (
    count_documents,
    create_document,
    delete_document,
    get_documents,
)
from app.models.policy import (
    DocumentCreate,
    DocumentPublic,
    DocumentsPublic,
)

router = APIRouter()


@router.get("/", response_model=DocumentsPublic)
def read_documents(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
    entity_id: uuid.UUID | None = None,
    entity_type: str | None = None,
) -> Any:
    """
    Retrieve documents.
    """
    documents = get_documents(
        session=session,
        skip=skip,
        limit=limit,
        entity_id=entity_id,
        entity_type=entity_type,
    )
    count = count_documents(
        session=session, entity_id=entity_id, entity_type=entity_type
    )
    return DocumentsPublic(data=documents, count=count)


@router.post("/upload", response_model=DocumentPublic)
async def upload_document(
    *,
    session: SessionDep,
    _current_user: StaffUser,
    file: UploadFile = File(...),
    entity_type: str = Form(...),
    entity_id: uuid.UUID = Form(...),
    document_type: str = Form(...),
    metadata_json: str = Form(""),
) -> Any:
    """
    Upload a document.
    """
    try:
        # Save file to storage
        relative_path = storage.save_file(
            file.file,
            filename=file.filename or "unnamed_file",
            folder=entity_type.lower(),
        )

        # Parse metadata
        metadata = {}
        if metadata_json:
            try:
                metadata = json.loads(metadata_json)
            except json.JSONDecodeError:
                pass

        # Create document record
        document_in = DocumentCreate(
            entity_type=entity_type,
            entity_id=entity_id,
            document_type=document_type,
            file_path=relative_path,
            mime_type=file.content_type,
            doc_metadata=metadata,
        )

        return create_document(session=session, document_in=document_in)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to upload document: {str(e)}"
        )


@router.get("/{id}", response_model=DocumentPublic)
def read_document_by_id(
    *,
    session: SessionDep,
    id: uuid.UUID,
) -> Any:
    """
    Get document by ID.
    """
    from app.models.policy import Document

    document = session.get(Document, id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{id}", response_model=DocumentPublic)
def remove_document(
    *,
    session: SessionDep,
    _current_user: StaffUser,
    id: uuid.UUID,
) -> Any:
    """
    Delete a document.
    """
    from app.models.policy import Document

    document = session.get(Document, id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete from storage
    storage.delete_file(document.file_path)

    # Delete from DB
    delete_document(session=session, db_document=document)
    return document


@router.get("/{id}/download")
def download_document(
    *,
    session: SessionDep,
    id: uuid.UUID,
) -> Any:
    """
    Download/View a document.
    """
    from app.models.policy import Document

    document = session.get(Document, id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    absolute_path = storage.get_file_path(document.file_path)
    if not absolute_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Physical file missing from storage: {document.file_path}",
        )

    return FileResponse(
        path=absolute_path,
        media_type=document.mime_type,
        content_disposition_type="inline",
        filename=f"{document.document_type}_{document.id}{Path(document.file_path).suffix}",
    )
