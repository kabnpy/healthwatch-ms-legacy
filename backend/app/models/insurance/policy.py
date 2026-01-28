import uuid
from datetime import date
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .catalog import Product
    from .client import Client
    from .financial import InvoiceLineItem, ReceiptAllocation

# ==========================================
# Policy Models
# ==========================================


class PolicyBase(SQLModel):
    policy_number: str = Field(unique=True, index=True)
    client_id: uuid.UUID = Field(foreign_key="client.id")
    product_id: uuid.UUID | None = Field(default=None, foreign_key="product.id")
    status: str = "Active"


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(SQLModel):
    policy_number: str | None = None
    client_id: uuid.UUID | None = None
    product_id: uuid.UUID | None = None
    status: str | None = None


class PolicyPublic(PolicyBase):
    id: uuid.UUID


class Policy(PolicyBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    client: "Client" = Relationship(back_populates="policies")
    product: Optional["Product"] = Relationship(back_populates="policies")

    risk_notes: list["RiskNote"] = Relationship(back_populates="policy")
    items: list["RiskItem"] = Relationship(back_populates="policy")
    claims: list["Claim"] = Relationship(back_populates="policy")
    documents: list["PolicyDocument"] = Relationship(back_populates="policy")


class PoliciesPublic(SQLModel):
    data: list[PolicyPublic]
    count: int


# ==========================================
# Risk Item Models
# ==========================================


class RiskItemBase(SQLModel):
    policy_id: uuid.UUID = Field(foreign_key="policy.id")
    identifier: str
    description: str
    sum_insured: float

    # The JSON Magic (Engine No, Chassis, Occupation, DOB)
    details: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)

    # Specific Limits (Windscreen: 50k, Medical: 100k)
    benefits: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)


class RiskItemCreate(RiskItemBase):
    pass


class RiskItemUpdate(SQLModel):
    policy_id: uuid.UUID | None = None
    identifier: str | None = None
    description: str | None = None
    sum_insured: float | None = None
    details: dict[str, Any] | None = None
    benefits: dict[str, Any] | None = None


class RiskItemPublic(RiskItemBase):
    id: uuid.UUID


class RiskItem(RiskItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    policy: "Policy" = Relationship(back_populates="items")
    claims: list["Claim"] = Relationship(back_populates="risk_item")
    documents: list["PolicyDocument"] = Relationship(back_populates="risk_item")


class RiskItemsPublic(SQLModel):
    data: list[RiskItemPublic]
    count: int


# ==========================================
# Risk Note Models
# ==========================================


class RiskNoteBase(SQLModel):
    risk_note_number: str = Field(unique=True)
    policy_id: uuid.UUID = Field(foreign_key="policy.id")

    transaction_type: str  # "New Business", "Renewal", "Endorsement"
    start_date: date
    end_date: date

    # Financials
    premium_breakdown: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)
    benefits_snapshot: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)
    risk_item_snapshot: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)

    commission_amount: float

    special_clauses: list[str] = Field(default_factory=list, sa_type=JSON)


class RiskNoteCreate(RiskNoteBase):
    pass


class RiskNoteUpdate(SQLModel):
    risk_note_number: str | None = None
    transaction_type: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    premium_breakdown: dict[str, Any] | None = None
    benefits_snapshot: dict[str, Any] | None = None
    risk_item_snapshot: dict[str, Any] | None = None
    commission_amount: float | None = None
    special_clauses: list[str] | None = None


class RiskNotePublic(RiskNoteBase):
    id: uuid.UUID


class RiskNote(RiskNoteBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    policy: "Policy" = Relationship(back_populates="risk_notes")
    invoice_line_items: list["InvoiceLineItem"] = Relationship(back_populates="risk_note")
    allocations: list["ReceiptAllocation"] = Relationship(back_populates="risk_note")
    documents: list["PolicyDocument"] = Relationship(back_populates="risk_note")


class RiskNotesPublic(SQLModel):
    data: list[RiskNotePublic]
    count: int


# ==========================================
# Claim Models
# ==========================================


class ClaimBase(SQLModel):
    claim_number: str = Field(unique=True)
    policy_id: uuid.UUID = Field(foreign_key="policy.id")
    risk_item_id: uuid.UUID | None = Field(default=None, foreign_key="riskitem.id")

    date_of_loss: date
    description: str
    status: str = "Open"
    reserve_amount: float = 0.0


class ClaimCreate(ClaimBase):
    pass


class ClaimUpdate(SQLModel):
    claim_number: str | None = None
    policy_id: uuid.UUID | None = None
    risk_item_id: uuid.UUID | None = None
    date_of_loss: date | None = None
    description: str | None = None
    status: str | None = None
    reserve_amount: float | None = None


class ClaimPublic(ClaimBase):
    id: uuid.UUID


class Claim(ClaimBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    policy: "Policy" = Relationship(back_populates="claims")
    risk_item: Optional["RiskItem"] = Relationship(back_populates="claims")
    documents: list["PolicyDocument"] = Relationship(back_populates="claim")


class ClaimsPublic(SQLModel):
    data: list[ClaimPublic]
    count: int


# ==========================================
# Policy Document Models
# ==========================================


class PolicyDocumentBase(SQLModel):
    document_type: str
    file_path: str
    expiry_date: date | None = None

    policy_id: uuid.UUID | None = Field(default=None, foreign_key="policy.id")
    risk_item_id: uuid.UUID | None = Field(default=None, foreign_key="riskitem.id")
    risk_note_id: uuid.UUID | None = Field(default=None, foreign_key="risknote.id")
    claim_id: uuid.UUID | None = Field(default=None, foreign_key="claim.id")


class PolicyDocumentCreate(PolicyDocumentBase):
    pass


class PolicyDocumentUpdate(SQLModel):
    document_type: str | None = None
    file_path: str | None = None
    expiry_date: date | None = None
    policy_id: uuid.UUID | None = None
    risk_item_id: uuid.UUID | None = None
    risk_note_id: uuid.UUID | None = None
    claim_id: uuid.UUID | None = None


class PolicyDocumentPublic(PolicyDocumentBase):
    id: uuid.UUID


class PolicyDocument(PolicyDocumentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    policy: Optional["Policy"] = Relationship(back_populates="documents")
    risk_item: Optional["RiskItem"] = Relationship(back_populates="documents")
    risk_note: Optional["RiskNote"] = Relationship(back_populates="documents")
    claim: Optional["Claim"] = Relationship(back_populates="documents")


class PolicyDocumentsPublic(SQLModel):
    data: list[PolicyDocumentPublic]
    count: int
