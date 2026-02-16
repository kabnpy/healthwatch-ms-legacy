import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Optional

from pydantic import ConfigDict, computed_field
from sqlalchemy import JSON, Column, Numeric
from sqlmodel import Field, Relationship, SQLModel

from .catalog import ProductPublic
from .enums import (
    ClaimEventType,
    ClaimStatus,
    DocumentEntityType,
    DocumentType,
    PolicyStatus,
    RiskNoteStatus,
    TransactionType,
)
from .mixins import AuditMixin

if TYPE_CHECKING:
    from .catalog import Product
    from .client import Client
    from .financial import InvoiceLineItem, ReceiptAllocation

# ==========================================
# Policy Models
# ==========================================


class PolicyBase(AuditMixin, SQLModel):
    model_config = ConfigDict(validate_assignment=True)
    policy_number: str = Field(unique=True, index=True)
    client_id: uuid.UUID = Field(foreign_key="client.id", index=True)
    product_id: uuid.UUID | None = Field(default=None, foreign_key="product.id", index=True)
    status: PolicyStatus = Field(default=PolicyStatus.ACTIVE)
    inception_date: date | None = Field(default_factory=date.today)


class PolicyCreate(PolicyBase):
    pass


class PolicyCreateExtended(PolicyCreate):
    """Extended model for atomic creation via Service layer"""
    risk_details: dict[str, Any] = Field(default_factory=dict)
    coverage_start: date = Field(default_factory=date.today)
    coverage_end: date


class EndorsementCreate(SQLModel):
    """Model for creating an endorsement"""
    updated_risk_details: dict[str, Any]
    change_description: str


class PolicyUpdate(SQLModel):
    policy_number: str | None = None
    client_id: uuid.UUID | None = None
    product_id: uuid.UUID | None = None
    status: PolicyStatus | None = None
    inception_date: date | None = None


class Policy(PolicyBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    client: "Client" = Relationship(back_populates="policies")
    product: Optional["Product"] = Relationship(back_populates="policies")

    risk_notes: list["RiskNote"] = Relationship(
        back_populates="policy",
        sa_relationship_kwargs={
            "order_by": "RiskNote.effective_date.desc(), RiskNote.created_at.desc()",
            "lazy": "selectin"
        }
    )
    claims: list["Claim"] = Relationship(back_populates="policy")

    @property
    def current_risk_note(self) -> Optional["RiskNote"]:
        """Get most recent risk note (current state)"""
        # Sorted by effective_date DESC in relationship
        active_notes = [
            rn for rn in self.risk_notes
            if rn.status in [RiskNoteStatus.ISSUED, RiskNoteStatus.ACTIVE]
        ]
        return active_notes[0] if active_notes else None

    @property
    def current_risk_details(self) -> dict[str, Any]:
        """Get current coverage details from latest risk note"""
        rn = self.current_risk_note
        return rn.policy_snapshot.get("risk_details", {}) if rn else {}

    @property
    def current_premium(self) -> Decimal:
        """Get current total premium from latest risk note"""
        rn = self.current_risk_note
        return rn.total_amount if rn else Decimal("0")

    @property
    def current_term_start(self) -> date | None:
        """Get current coverage period start"""
        rn = self.current_risk_note
        return rn.coverage_start if rn else None

    @property
    def current_term_end(self) -> date | None:
        """Get current coverage period end"""
        rn = self.current_risk_note
        return rn.coverage_end if rn else None


class PolicyPublic(PolicyBase):
    id: uuid.UUID
    product: ProductPublic | None = None

    @computed_field  # type: ignore
    @property
    def current_risk_details(self) -> dict[str, Any]:
        """Get current coverage details from latest risk note"""
        if not hasattr(self, "risk_notes") or not self.risk_notes:
            return {}
        active_notes = [
            rn for rn in self.risk_notes
            if rn.status in [RiskNoteStatus.ISSUED, RiskNoteStatus.ACTIVE]
        ]
        if not active_notes:
            return {}
        return active_notes[0].policy_snapshot.get("risk_details", {})

    @computed_field  # type: ignore
    @property
    def total_premium(self) -> Decimal:
        """Get current total premium from latest risk note"""
        if not hasattr(self, "risk_notes") or not self.risk_notes:
            return Decimal("0")
        active_notes = [
            rn for rn in self.risk_notes
            if rn.status in [RiskNoteStatus.ISSUED, RiskNoteStatus.ACTIVE]
        ]
        return active_notes[0].total_amount if active_notes else Decimal("0")

    @computed_field  # type: ignore
    @property
    def start_date(self) -> date | None:
        """Backward compatibility for start_date"""
        if not hasattr(self, "risk_notes") or not self.risk_notes:
            return None
        active_notes = [
            rn for rn in self.risk_notes
            if rn.status in [RiskNoteStatus.ISSUED, RiskNoteStatus.ACTIVE]
        ]
        return active_notes[0].coverage_start if active_notes else None

    @computed_field  # type: ignore
    @property
    def end_date(self) -> date | None:
        """Backward compatibility for end_date"""
        if not hasattr(self, "risk_notes") or not self.risk_notes:
            return None
        active_notes = [
            rn for rn in self.risk_notes
            if rn.status in [RiskNoteStatus.ISSUED, RiskNoteStatus.ACTIVE]
        ]
        return active_notes[0].coverage_end if active_notes else None

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
            # Note: In PolicyPublic, we use current_risk_details (computed)
            risk_details = self.current_risk_details
            if "motor private" in base_name.lower():
                reg_no = recursive_search(
                    risk_details, ["reg_no", "Reg No", "Reg. No", "Registration"]
                )
                if reg_no:
                    return f"{base_name} - {reg_no}"

            return base_name
        return self.policy_number


class PoliciesPublic(SQLModel):
    data: list[PolicyPublic]
    count: int


# ==========================================
# Risk Note Models
# ==========================================


class RiskNoteBase(AuditMixin, SQLModel):
    policy_id: uuid.UUID = Field(foreign_key="policy.id", index=True)
    risk_note_number: str | None = Field(default=None, unique=True, index=True)
    transaction_type: TransactionType
    status: RiskNoteStatus = Field(default=RiskNoteStatus.DRAFT)
    previous_risk_note_id: uuid.UUID | None = Field(
        default=None, foreign_key="risknote.id", index=True
    )
    invoice_number: str | None = None
    created_by_id: uuid.UUID | None = Field(default=None, foreign_key="user.id", index=True)
    payment_status: str = Field(default="Unpaid")

    effective_date: date = Field(default_factory=date.today, index=True)
    coverage_start: date
    coverage_end: date

    # Invoice Totals
    net_premium: Decimal = Field(sa_type=Numeric(precision=15, scale=2))
    commission_amount: Decimal = Field(sa_type=Numeric(precision=15, scale=2))
    total_amount: Decimal = Field(sa_type=Numeric(precision=15, scale=2))


class RiskNoteCreate(RiskNoteBase):
    taxes: dict[str, Any] = Field(default_factory=dict)
    policy_snapshot: dict[str, Any] = Field(default_factory=dict)
    special_clauses: list[str] = Field(default_factory=list)


class RiskNoteUpdate(SQLModel):
    transaction_type: TransactionType | None = None
    risk_note_number: str | None = None
    status: RiskNoteStatus | None = None
    previous_risk_note_id: uuid.UUID | None = None
    invoice_number: str | None = None
    payment_status: str | None = None
    effective_date: date | None = None
    coverage_start: date | None = None
    coverage_end: date | None = None
    net_premium: Decimal | None = None
    taxes: dict[str, Any] | None = None
    commission_amount: Decimal | None = None
    total_amount: Decimal | None = None
    policy_snapshot: dict[str, Any] | None = None
    special_clauses: list[str] | None = None


class RiskNotePublic(RiskNoteBase):
    id: uuid.UUID
    policy: PolicyPublic | None = None
    taxes: dict[str, Any] = Field(default_factory=dict)
    policy_snapshot: dict[str, Any] = Field(default_factory=dict)
    special_clauses: list[str] = Field(default_factory=list)


class RiskNote(RiskNoteBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    policy: Policy = Relationship(back_populates="risk_notes")
    invoice_line_items: list["InvoiceLineItem"] = Relationship(back_populates="risk_note")
    allocations: list["ReceiptAllocation"] = Relationship(back_populates="risk_note")

    taxes: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    policy_snapshot: dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON)
    )
    special_clauses: list[str] = Field(default_factory=list, sa_column=Column(JSON))


class RiskNotesPublic(SQLModel):
    data: list[RiskNotePublic]
    count: int


# ==========================================
# Claim Models
# ==========================================


class ClaimBase(AuditMixin, SQLModel):
    claim_number: str = Field(unique=True, index=True)
    policy_id: uuid.UUID = Field(foreign_key="policy.id", index=True)
    date_of_loss: date
    date_reported: date = Field(default_factory=date.today)
    description: str
    status: ClaimStatus = Field(default=ClaimStatus.REPORTED)
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
    status: ClaimStatus | None = None
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
    claim_id: uuid.UUID = Field(foreign_key="claim.id", index=True)
    event_type: ClaimEventType
    description: str
    created_by_id: uuid.UUID | None = Field(default=None, foreign_key="user.id", index=True)
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
# Polymorphic Document Model (Single Table)
# ==========================================


class DocumentBase(SQLModel):
    model_config = ConfigDict(validate_assignment=True)
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
