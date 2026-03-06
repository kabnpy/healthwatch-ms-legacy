import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import ConfigDict
from sqlalchemy import JSON
from sqlmodel import Column, Field, SQLModel


class DocumentEntityType(str, Enum):
    CLIENT = "Client"
    POLICY = "Policy"
    CLAIM = "Claim"
    USER = "User"
    RISK_NOTE = "RiskNote"


class DocumentType(str, Enum):
    LOGBOOK = "Logbook"
    ID = "ID"
    VALUATION = "Valuation"
    POLICE_ABSTRACT = "PoliceAbstract"
    RECEIPT = "Receipt"
    OTHER = "Other"


class DocumentBase(SQLModel):
    model_config = ConfigDict(validate_assignment=True)  # type: ignore
    document_type: DocumentType
    file_path: str
    mime_type: str | None = None
    uploaded_at: datetime = Field(default_factory=datetime.now)


class DocumentCreate(DocumentBase):
    entity_type: DocumentEntityType
    entity_id: uuid.UUID
    doc_metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentUpdate(SQLModel):
    document_type: DocumentType | None = None
    file_path: str | None = None
    mime_type: str | None = None
    doc_metadata: dict[str, Any] | None = None


class DocumentPublic(DocumentBase):
    id: uuid.UUID
    entity_type: DocumentEntityType
    entity_id: uuid.UUID
    doc_metadata: dict[str, Any] = Field(default_factory=dict)


class Document(DocumentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    entity_type: DocumentEntityType
    entity_id: uuid.UUID
    doc_metadata: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class DocumentsPublic(SQLModel):
    data: list[DocumentPublic]
    count: int


# ==========================================
# Late Binding / Rebuild
# ==========================================

DocumentPublic.model_rebuild()
DocumentsPublic.model_rebuild()
