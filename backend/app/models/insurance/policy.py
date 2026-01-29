import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Any, Optional

from pydantic import computed_field
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel

from .catalog import ProductPublic

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
    created_at: datetime = Field(default_factory=datetime.now)


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(SQLModel):
    policy_number: str | None = None
    client_id: uuid.UUID | None = None
    product_id: uuid.UUID | None = None
    status: str | None = None


class PolicyPublic(PolicyBase):
    id: uuid.UUID
    product: ProductPublic | None = None
    items: list["RiskItemPublic"] = []

    @computed_field
    @property
    def display_name(self) -> str:
        if self.product:
            # Safe access to items list
            if self.items and len(self.items) > 0:
                return (
                    f"{self.product.class_of_insurance} - {self.items[0].description}"
                )
            return f"{self.product.name}"
        return self.policy_number


class Policy(PolicyBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    client: "Client" = Relationship(back_populates="policies")
    product: Optional["Product"] = Relationship(back_populates="policies")

    risk_notes: list["RiskNote"] = Relationship(back_populates="policy")
    items: list["RiskItem"] = Relationship(back_populates="policy")
    claims: list["Claim"] = Relationship(back_populates="policy")


class PoliciesPublic(SQLModel):
    data: list[PolicyPublic]
    count: int


# ==========================================
# Risk Item Models
# ==========================================


class RiskItemBase(SQLModel):
    policy_id: uuid.UUID = Field(foreign_key="policy.id")
    version_number: int = Field(default=1)
    valid_from: date = Field(default_factory=date.today)
    valid_to: date | None = None
    is_active: bool = Field(default=True)

    description: str
    cover_description: str
    total_premium: float = Field(default=0.0)
    premium_breakdown: dict[str, float] = Field(default_factory=dict, sa_type=JSON)
    risk_details: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)


class RiskItemCreate(RiskItemBase):
    pass


class RiskItemUpdate(SQLModel):
    version_number: int | None = None
    valid_from: date | None = None
    valid_to: date | None = None
    is_active: bool | None = None
    description: str | None = None
    cover_description: str | None = None
    total_premium: float | None = None
    premium_breakdown: dict[str, float] | None = None
    risk_details: dict[str, Any] | None = None


class RiskItemPublic(RiskItemBase):
    id: uuid.UUID


class RiskItem(RiskItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    policy: "Policy" = Relationship(back_populates="items")
    claims: list["Claim"] = Relationship(back_populates="risk_item")


class RiskItemsPublic(SQLModel):
    data: list[RiskItemPublic]
    count: int


# ==========================================
# Risk Note Models
# ==========================================


class RiskNoteBase(SQLModel):
    policy_id: uuid.UUID = Field(foreign_key="policy.id")
    transaction_type: str  # "New Business", "Renewal", "Endorsement", "Cancellation"
    previous_risk_note_id: uuid.UUID | None = Field(
        default=None, foreign_key="risknote.id"
    )
    invoice_number: str | None = None
    created_by_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")
    payment_status: str = Field(default="Unpaid")

    start_date: date
    end_date: date

    # Invoice Totals (Aggregated from all items)
    net_premium: float
    taxes: dict[str, float] = Field(default_factory=dict, sa_type=JSON)
    commission_amount: float
    total_amount: float

    # SNAPSHOTS:
    # 1. The items as they were at this moment in time
    # Structure: { "item_uuid": {"description": "...", "premium": 500, "details": {...}} }
    items_snapshot: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)

    # 2. Policy level clauses added to this note
    special_clauses: list[str] = Field(default_factory=list, sa_type=JSON)


class RiskNoteCreate(RiskNoteBase):
    pass


class RiskNoteUpdate(SQLModel):
    transaction_type: str | None = None
    previous_risk_note_id: uuid.UUID | None = None
    invoice_number: str | None = None
    payment_status: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    net_premium: float | None = None
    taxes: dict[str, float] | None = None
    commission_amount: float | None = None
    total_amount: float | None = None
    items_snapshot: dict[str, Any] | None = None
    special_clauses: list[str] | None = None


class RiskNotePublic(RiskNoteBase):
    id: uuid.UUID


class RiskNote(RiskNoteBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    policy: "Policy" = Relationship(back_populates="risk_notes")
    invoice_line_items: list["InvoiceLineItem"] = Relationship(
        back_populates="risk_note"
    )
    allocations: list["ReceiptAllocation"] = Relationship(back_populates="risk_note")


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
    date_reported: date = Field(default_factory=date.today)
    description: str
    status: str = "Reported"
    reserve_amount: float = 0.0


class ClaimCreate(ClaimBase):
    pass


class ClaimUpdate(SQLModel):
    claim_number: str | None = None
    policy_id: uuid.UUID | None = None
    risk_item_id: uuid.UUID | None = None
    date_of_loss: date | None = None
    date_reported: date | None = None
    description: str | None = None
    status: str | None = None
    reserve_amount: float | None = None


class ClaimPublic(ClaimBase):
    id: uuid.UUID


class Claim(ClaimBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    policy: "Policy" = Relationship(back_populates="claims")
    risk_item: Optional["RiskItem"] = Relationship(back_populates="claims")
    events: list["ClaimEvent"] = Relationship(back_populates="claim")


class ClaimsPublic(SQLModel):
    data: list[ClaimPublic]
    count: int


# ==========================================
# Claim Event Models
# ==========================================


class ClaimEventBase(SQLModel):
    claim_id: uuid.UUID = Field(foreign_key="claim.id")
    event_type: str  # "Notification", "Assessment", "Correspondence", "Payment"
    description: str
    created_by_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)


class ClaimEventCreate(ClaimEventBase):
    pass


class ClaimEventPublic(ClaimEventBase):
    id: uuid.UUID


class ClaimEvent(ClaimEventBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    claim: "Claim" = Relationship(back_populates="events")


class ClaimEventsPublic(SQLModel):
    data: list[ClaimEventPublic]
    count: int


# ==========================================
# Polymorphic Document Models
# ==========================================


class DocumentBase(SQLModel):
    entity_type: str  # "Client", "Policy", "Claim", "User", "RiskNote"
    entity_id: uuid.UUID
    document_type: str  # "Logbook", "ID", "Valuation", "PoliceAbstract", "Receipt"
    file_path: str
    mime_type: str | None = None
    uploaded_at: datetime = Field(default_factory=datetime.now)


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(SQLModel):
    entity_type: str | None = None
    entity_id: uuid.UUID | None = None
    document_type: str | None = None
    file_path: str | None = None
    mime_type: str | None = None


class DocumentPublic(DocumentBase):
    id: uuid.UUID


class Document(DocumentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class DocumentsPublic(SQLModel):
    data: list[DocumentPublic]
    count: int
