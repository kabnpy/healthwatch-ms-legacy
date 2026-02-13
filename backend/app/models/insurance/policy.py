import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Optional

from pydantic import computed_field
from sqlalchemy import JSON, Numeric
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

    # Cover Details (Merged from RiskItem)
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None
    total_premium: Decimal = Field(
        default=Decimal("0.0"), sa_type=Numeric(precision=15, scale=2)
    )
    premium_breakdown: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)
    risk_details: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(SQLModel):
    policy_number: str | None = None
    client_id: uuid.UUID | None = None
    product_id: uuid.UUID | None = None
    status: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None
    total_premium: Decimal | None = None
    premium_breakdown: dict[str, Any] | None = None
    risk_details: dict[str, Any] | None = None


class PolicyPublic(PolicyBase):
    id: uuid.UUID
    product: ProductPublic | None = None

    @computed_field  # type: ignore
    @property
    def display_name(self) -> str:
        def recursive_search(obj: Any, targets: list[str]) -> str | None:
            if not isinstance(obj, dict):
                return None
            # 1. Immediate match
            for k, v in obj.items():
                if any(t.lower() == str(k).lower().strip() for t in targets):
                    if isinstance(v, str) and v and "<<" not in v:
                        return v.strip()
            # 2. Recurse
            for v in obj.values():
                res = recursive_search(v, targets)
                if res:
                    return res
            return None

        if self.product:
            base_name = self.product.class_of_insurance or self.product.name

            # Refinement for Motor Private: Add Reg No if available
            if "motor private" in base_name.lower():
                reg_no = recursive_search(
                    self.risk_details, ["reg_no", "Reg No", "Reg. No", "Registration"]
                )
                if reg_no:
                    return f"{base_name} - {reg_no}"

            if self.description:
                trimmed_desc = self.description.strip()
                trimmed_base = base_name.strip()
                if trimmed_desc.lower() != trimmed_base.lower() and trimmed_desc:
                    return f"{base_name} - {trimmed_desc}"

            return base_name
        return self.policy_number


class Policy(PolicyBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    client: "Client" = Relationship(back_populates="policies")
    product: Optional["Product"] = Relationship(back_populates="policies")

    risk_notes: list["RiskNote"] = Relationship(back_populates="policy")
    claims: list["Claim"] = Relationship(back_populates="policy")


class PoliciesPublic(SQLModel):
    data: list[PolicyPublic]
    count: int


# ==========================================
# Risk Note Models
# ==========================================


class RiskNoteBase(SQLModel):
    policy_id: uuid.UUID = Field(foreign_key="policy.id")
    risk_note_number: str | None = Field(default=None, unique=True, index=True)
    transaction_type: str  # "New Business", "Renewal", "Endorsement", "Cancellation"
    status: str = Field(default="Draft")  # "Draft", "Active", "Cancelled"
    previous_risk_note_id: uuid.UUID | None = Field(
        default=None, foreign_key="risknote.id"
    )
    invoice_number: str | None = None
    created_by_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")
    payment_status: str = Field(default="Unpaid")

    start_date: date
    end_date: date

    # Invoice Totals
    net_premium: Decimal = Field(sa_type=Numeric(precision=15, scale=2))
    taxes: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)
    commission_amount: Decimal = Field(sa_type=Numeric(precision=15, scale=2))
    total_amount: Decimal = Field(sa_type=Numeric(precision=15, scale=2))

    # SNAPSHOTS:
    # A frozen state of the policy at this moment in time
    policy_snapshot: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)

    # Policy level clauses added to this note
    special_clauses: list[str] = Field(default_factory=list, sa_type=JSON)


class RiskNoteCreate(RiskNoteBase):
    pass


class RiskNoteUpdate(SQLModel):
    transaction_type: str | None = None
    risk_note_number: str | None = None
    status: str | None = None
    previous_risk_note_id: uuid.UUID | None = None
    invoice_number: str | None = None
    payment_status: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    net_premium: Decimal | None = None
    taxes: dict[str, Any] | None = None
    commission_amount: Decimal | None = None
    total_amount: Decimal | None = None
    policy_snapshot: dict[str, Any] | None = None
    special_clauses: list[str] | None = None


class RiskNotePublic(RiskNoteBase):
    id: uuid.UUID
    policy: Optional["PolicyPublic"] = None


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

    date_of_loss: date
    date_reported: date = Field(default_factory=date.today)
    description: str
    status: str = "Reported"
    reserve_amount: Decimal = Field(
        default=Decimal("0.0"), sa_type=Numeric(precision=15, scale=2)
    )


class ClaimCreate(ClaimBase):
    pass


class ClaimUpdate(SQLModel):
    claim_number: str | None = None
    policy_id: uuid.UUID | None = None
    date_of_loss: date | None = None
    date_reported: date | None = None
    description: str | None = None
    status: str | None = None
    reserve_amount: Decimal | None = None


class ClaimPublic(ClaimBase):
    id: uuid.UUID


class Claim(ClaimBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    policy: "Policy" = Relationship(back_populates="claims")
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
    doc_metadata: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)
    uploaded_at: datetime = Field(default_factory=datetime.now)


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(SQLModel):
    entity_type: str | None = None
    entity_id: uuid.UUID | None = None
    document_type: str | None = None
    file_path: str | None = None
    mime_type: str | None = None
    doc_metadata: dict[str, Any] | None = None


class DocumentPublic(DocumentBase):
    id: uuid.UUID


class Document(DocumentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class DocumentsPublic(SQLModel):
    data: list[DocumentPublic]
    count: int
