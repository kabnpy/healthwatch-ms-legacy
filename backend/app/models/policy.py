import uuid
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, cast

from pydantic import ConfigDict
from sqlalchemy import JSON, Column, Numeric
from sqlmodel import Field, Relationship, SQLModel

from .audit import AuditMixin
from .client import ClientPublic

if TYPE_CHECKING:
    from .claim import Claim
    from .client import Client



class PolicyStatus(str, Enum):
    ACTIVE = "Active"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"
    LAPSED = "Lapsed"
    RENEWAL_INVITED = "Renewal Invited"
    RENEWAL_CONFIRMED = "Renewal Confirmed"


class TransactionType(str, Enum):
    NEW_BUSINESS = "New Business"
    RENEWAL = "Renewal"
    CANCELLATION = "Cancellation"


class RiskNoteStatus(str, Enum):
    DRAFT = "Draft"
    ISSUED = "Issued"
    REPLACED = "Replaced"
    CANCELLED = "Cancelled"
    ACTIVE = "Issued"
    RENEWAL_INVITED = "Renewal Invited"
    RENEWAL_CONFIRMED = "Renewal Confirmed"


class InvoiceStatus(str, Enum):
    UNPAID = "Unpaid"
    PARTIAL = "Partial"
    PAID = "Paid"
    CANCELLED = "Cancelled"


class ReceiptStatus(str, Enum):
    ACTIVE = "Active"
    VOIDED = "Voided"


class PricingStrategy(str, Enum):
    PERCENTAGE = "Percentage"
    FIXED_TIERED = "FixedTiered"
    MANUAL = "Manual"


# ==========================================
# Insurer & Product Models
# ==========================================


class InsurerBase(AuditMixin, SQLModel):
    model_config = ConfigDict(validate_assignment=True)  # type: ignore
    name: str = Field(unique=True, index=True)
    email: str | None = None
    phone: str | None = None


class InsurerCreate(InsurerBase):
    pass


class InsurerUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class InsurerPublic(InsurerBase):
    id: uuid.UUID


class Insurer(InsurerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    products: list["Product"] = Relationship(back_populates="insurer")


class InsurersPublic(SQLModel):
    data: list[InsurerPublic]
    count: int


class ProductBase(AuditMixin, SQLModel):
    insurer_id: uuid.UUID = Field(foreign_key="insurer.id", index=True)
    name: str
    class_of_insurance: str
    product_details: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)
    pricing_strategy: PricingStrategy = Field(default=PricingStrategy.PERCENTAGE)
    pricing_rules: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)
    default_commission_rate: float = 10.0
    default_benefits_and_limits: str | None = None
    default_excesses: str | None = None
    default_special_clauses: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    insurer_id: uuid.UUID | None = None
    name: str | None = None
    class_of_insurance: str | None = None
    product_details: dict[str, Any] | None = None
    pricing_strategy: PricingStrategy | None = None
    pricing_rules: dict[str, Any] | None = None
    default_commission_rate: float | None = None


class ProductPublic(ProductBase):
    id: uuid.UUID
    insurer: Optional["InsurerPublic"] = None


class Product(ProductBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    insurer: "Insurer" = Relationship(back_populates="products")
    policies: list["Policy"] = Relationship(back_populates="product")

    def validate_risk_details(self, risk_details: dict[str, Any]) -> dict[str, Any]:
        if "motor private" in self.class_of_insurance.lower():
            from app.schemas import MotorPrivateRiskDetails
            validated = MotorPrivateRiskDetails(**risk_details)
            return validated.model_dump(mode="python")
        return risk_details

    def calculate_premium(self, risk_details: dict[str, Any]) -> Decimal:
        from app.services.rating import RatingService
        breakdown = RatingService.calculate_breakdown(self, risk_details)
        return breakdown.net_premium


class ProductsPublic(SQLModel):
    data: list[ProductPublic]
    count: int


# ==========================================
# Policy Models
# ==========================================


class PolicyBase(AuditMixin, SQLModel):
    model_config = ConfigDict(validate_assignment=True)  # type: ignore
    policy_number: str = Field(unique=True, index=True)
    client_id: uuid.UUID = Field(foreign_key="client.id", index=True)
    product_id: uuid.UUID | None = Field(
        default=None, foreign_key="product.id", index=True
    )
    status: PolicyStatus = Field(default=PolicyStatus.ACTIVE)
    inception_date: date = Field(default_factory=date.today)


class PolicyCreate(PolicyBase):
    pass


class PolicyCreateExtended(PolicyCreate):
    coverage_start: date = Field(default_factory=date.today)
    coverage_end: date
    risk_details: dict[str, Any] = Field(default_factory=dict)


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
            "lazy": "selectin",
        },
    )
    claims: list["Claim"] = Relationship(back_populates="policy")


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
    created_by_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", index=True
    )
    effective_date: date = Field(default_factory=date.today, index=True)
    coverage_start: date
    coverage_end: date
    net_premium: Decimal = Field(sa_column=Column(Numeric(precision=15, scale=2)))
    commission_amount: Decimal = Field(sa_column=Column(Numeric(precision=15, scale=2)))
    total_amount: Decimal = Field(sa_column=Column(Numeric(precision=15, scale=2)))
    cover_snapshot: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)


class RiskNoteCreate(RiskNoteBase):
    financial_breakdown: dict[str, Any] = Field(default_factory=dict)
    special_clauses: list[str] = Field(default_factory=list)


class RiskNoteUpdate(SQLModel):
    transaction_type: TransactionType | None = None
    risk_note_number: str | None = None
    status: RiskNoteStatus | None = None
    previous_risk_note_id: uuid.UUID | None = None
    effective_date: date | None = None
    coverage_start: date | None = None
    coverage_end: date | None = None
    net_premium: Decimal | None = None
    financial_breakdown: dict[str, Any] | None = None
    commission_amount: Decimal | None = None
    total_amount: Decimal | None = None
    special_clauses: list[str] | None = None
    cover_snapshot: dict[str, Any] | None = None


class RiskNote(RiskNoteBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    policy: Policy = Relationship(back_populates="risk_notes")
    invoice_line_items: list["InvoiceLineItem"] = Relationship(
        back_populates="risk_note"
    )
    allocations: list["ReceiptAllocation"] = Relationship(back_populates="risk_note")
    financial_breakdown: dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON)
    )
    special_clauses_raw: list[str] = Field(
        default_factory=list, sa_column=Column("special_clauses", JSON)
    )

    @property
    def special_clauses(self) -> list[str]:
        snapshot_terms = self.cover_snapshot.get("terms", {})
        if isinstance(snapshot_terms, dict):
            snapshot_clauses = snapshot_terms.get("special_clauses")
            if snapshot_clauses:
                if isinstance(snapshot_clauses, str):
                    return [snapshot_clauses]
                return cast(list[str], snapshot_clauses)
        return self.special_clauses_raw

    @special_clauses.setter
    def special_clauses(self, value: list[str]) -> None:
        self.special_clauses_raw = value

    @property
    def invoice_number(self) -> str | None:
        if self.invoice_line_items and self.invoice_line_items[0].invoice:
            return self.invoice_line_items[0].invoice.invoice_number
        return None


class RiskNotePublic(RiskNoteBase):
    id: uuid.UUID
    policy: Optional["PolicyPublic"] = None
    financial_breakdown: dict[str, Any] = Field(default_factory=dict)
    special_clauses: list[str] = Field(default_factory=list)
    invoice_number: str | None = None
    invoice_line_items: list["InvoiceLineItemDetailedPublic"] = Field(
        default_factory=list
    )


class RiskNotesPublic(SQLModel):
    data: list[RiskNotePublic]
    count: int


# ==========================================
# Financial Models
# ==========================================


class InvoiceBase(AuditMixin, SQLModel):
    model_config = ConfigDict(validate_assignment=True)  # type: ignore
    invoice_number: str = Field(unique=True, index=True)
    client_id: uuid.UUID = Field(foreign_key="client.id", index=True)
    date_issued: date = Field(default_factory=date.today)
    due_date: date | None = None
    status: InvoiceStatus = Field(default=InvoiceStatus.UNPAID)
    total_amount: Decimal = Field(
        default=Decimal("0.0"), sa_column=Column(Numeric(precision=15, scale=2))
    )
    balance_due: Decimal = Field(
        default=Decimal("0.0"), sa_column=Column(Numeric(precision=15, scale=2))
    )
    notes: str | None = None


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceBulkCreate(SQLModel):
    client_id: uuid.UUID
    risk_note_ids: list[uuid.UUID]
    date_issued: date = Field(default_factory=date.today)
    notes: str | None = None


class InvoiceUpdate(SQLModel):
    invoice_number: str | None = None
    due_date: date | None = None
    status: InvoiceStatus | None = None
    total_amount: Decimal | None = None
    balance_due: Decimal | None = None
    notes: str | None = None


class Invoice(InvoiceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    client: "Client" = Relationship(back_populates="invoices")
    line_items: list["InvoiceLineItem"] = Relationship(back_populates="invoice")
    allocations: list["ReceiptAllocation"] = Relationship(back_populates="invoice")


class InvoiceLineItemBase(SQLModel):
    invoice_id: uuid.UUID = Field(foreign_key="invoice.id", index=True)
    risk_note_id: uuid.UUID = Field(foreign_key="risknote.id", index=True)
    amount: Decimal = Field(sa_column=Column(Numeric(precision=15, scale=2)))
    description: str | None = None


class InvoiceLineItemCreate(InvoiceLineItemBase):
    pass


class InvoiceLineItem(InvoiceLineItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    invoice: "Invoice" = Relationship(back_populates="line_items")
    risk_note: "RiskNote" = Relationship(back_populates="invoice_line_items")


class ReceiptBase(AuditMixin, SQLModel):
    receipt_number: str = Field(unique=True, index=True)
    client_id: uuid.UUID = Field(foreign_key="client.id", index=True)
    date_received: date
    amount: Decimal = Field(sa_column=Column(Numeric(precision=15, scale=2)))
    unallocated_amount: Decimal = Field(
        default=Decimal("0.0"), sa_column=Column(Numeric(precision=15, scale=2))
    )
    mode: str
    reference: str
    notes: str | None = None
    status: ReceiptStatus = Field(default=ReceiptStatus.ACTIVE)
    created_by_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", index=True
    )


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptUpdate(SQLModel):
    receipt_number: str | None = None
    date_received: date | None = None
    amount: Decimal | None = None
    unallocated_amount: Decimal | None = None
    mode: str | None = None
    reference: str | None = None
    notes: str | None = None
    status: ReceiptStatus | None = None


class ReceiptAllocationBase(SQLModel):
    receipt_id: uuid.UUID = Field(foreign_key="receipt.id", index=True)
    invoice_id: uuid.UUID = Field(foreign_key="invoice.id", index=True)
    risk_note_id: uuid.UUID | None = Field(
        default=None, foreign_key="risknote.id", index=True
    )
    amount_allocated: Decimal = Field(sa_column=Column(Numeric(precision=15, scale=2)))


class ReceiptAllocationCreate(ReceiptAllocationBase):
    pass


class ReceiptAllocation(ReceiptAllocationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    receipt: "Receipt" = Relationship(back_populates="allocations")
    invoice: "Invoice" = Relationship(back_populates="allocations")
    risk_note: "RiskNote" = Relationship(back_populates="allocations")


class ReceiptAllocationsPublic(SQLModel):
    data: list[ReceiptAllocationBase]
    count: int


class ReceiptPublic(ReceiptBase):
    id: uuid.UUID
    allocations: list[ReceiptAllocationBase] = []


class Receipt(ReceiptBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    client: "Client" = Relationship(back_populates="receipts")
    allocations: list["ReceiptAllocation"] = Relationship(back_populates="receipt")


class ReceiptsPublic(SQLModel):
    data: list[ReceiptPublic]
    count: int


class InvoiceLineItemPublic(InvoiceLineItemBase):
    id: uuid.UUID


class InvoicePublic(InvoiceBase):
    id: uuid.UUID
    line_items: list[InvoiceLineItemPublic] = []
    allocations: list[ReceiptAllocationBase] = []


class InvoiceLineItemDetailedPublic(InvoiceLineItemPublic):
    invoice: InvoicePublic | None = None


class InvoicesPublic(SQLModel):
    data: list[InvoicePublic]
    count: int


class PolicyPublic(PolicyBase):
    id: uuid.UUID
    product: ProductPublic | None = None
    client: Optional["ClientPublic"] = None
    active_note: Optional["RiskNotePublic"] = None


class PoliciesPublic(SQLModel):
    data: list[PolicyPublic]
    count: int


# ==========================================
# Late Binding / Rebuild
# ==========================================

InvoiceLineItemPublic.model_rebuild()
InvoiceLineItemDetailedPublic.model_rebuild()
InvoicePublic.model_rebuild()
InvoicesPublic.model_rebuild()
ReceiptPublic.model_rebuild()
ReceiptsPublic.model_rebuild()
PolicyPublic.model_rebuild()
PoliciesPublic.model_rebuild()
RiskNotePublic.model_rebuild()
RiskNotesPublic.model_rebuild()
