import uuid
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Optional

from pydantic import ConfigDict, EmailStr
from sqlalchemy import JSON, Column, Numeric
from sqlmodel import Field, Relationship, SQLModel

# ==========================================
# Enums
# ==========================================


class PolicyStatus(str, Enum):
    ACTIVE = "Active"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"
    LAPSED = "Lapsed"


class TransactionType(str, Enum):
    NEW_BUSINESS = "New Business"
    RENEWAL = "Renewal"
    ENDORSEMENT = "Endorsement"
    CANCELLATION = "Cancellation"


class RiskNoteStatus(str, Enum):
    DRAFT = "Draft"
    ISSUED = "Issued"
    REPLACED = "Replaced"  # superseded by a newer note on same policy
    CANCELLED = "Cancelled"


class InvoiceStatus(str, Enum):
    UNPAID = "Unpaid"
    PARTIAL = "Partial"
    PAID = "Paid"
    CANCELLED = "Cancelled"


class ReceiptStatus(str, Enum):
    ACTIVE = "Active"
    VOIDED = "Voided"


class ClaimStatus(str, Enum):
    REPORTED = "Reported"
    ASSESSED = "Assessed"
    PAID = "Paid"
    REJECTED = "Rejected"
    CLOSED = "Closed"


class ClaimEventType(str, Enum):
    NOTIFICATION = "Notification"
    ASSESSMENT = "Assessment"
    CORRESPONDENCE = "Correspondence"
    PAYMENT = "Payment"


class DocumentEntityType(str, Enum):
    CLIENT = "Client"
    POLICY = "Policy"
    CLAIM = "Claim"
    RISK_NOTE = "RiskNote"


class DocumentType(str, Enum):
    LOGBOOK = "Logbook"
    ID = "ID"
    KRA_CERTIFICATE = "KraCertificate"
    VALUATION = "Valuation"
    POLICE_ABSTRACT = "PoliceAbstract"
    COVER_NOTE = "CoverNote"
    OTHER = "Other"


class RenewalStatus(str, Enum):
    PENDING = "Pending"  # created by scheduler; awaiting team action
    UNDER_REVIEW = "UnderReview"  # team has insurer notice; comparing to last term
    CLIENT_NOTIFIED = "ClientNotified"  # payment notice sent to client
    COMPLETED = "Completed"  # new RiskNote issued; renewal done
    LAPSED = "Lapsed"  # client didn't pay; policy lapsed


# ==========================================
# Common
# ==========================================


class Message(SQLModel):
    message: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


# ==========================================
# User
# ==========================================


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# ==========================================
# Insurer
# ==========================================


class InsurerBase(SQLModel):
    name: str = Field(unique=True, index=True, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)


class InsurerCreate(InsurerBase):
    pass


class InsurerUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class Insurer(InsurerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    products: list["Product"] = Relationship(back_populates="insurer")


class InsurerPublic(InsurerBase):
    id: uuid.UUID


class InsurersPublic(SQLModel):
    data: list[InsurerPublic]
    count: int


# ==========================================
# Product
#
# A product is an insurer's named offering for a class of insurance.
# It carries no business logic — premium calculation and risk detail
# validation belong in the service layer, not the data model.
# ==========================================


class ProductBase(SQLModel):
    insurer_id: uuid.UUID = Field(foreign_key="insurer.id", index=True)
    name: str = Field(max_length=255)
    class_of_insurance: str = Field(max_length=100)  # "Motor Private", "Fire", etc.
    pricing_strategy: PricingStrategy = Field(default=PricingStrategy.PERCENTAGE)
    # For PERCENTAGE/FIXED_TIERED: {"tiers": [{"max": 1500000, "rate": 5.0, "min": 60000}, ...]}
    # For a flat rate product:      {"rate": 2.5}
    # For MANUAL:                   {} — user supplies premium directly
    pricing_rules: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    insurer_id: uuid.UUID | None = None
    name: str | None = None
    class_of_insurance: str | None = None


class Product(ProductBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    insurer: "Insurer" = Relationship(back_populates="products")
    policies: list["Policy"] = Relationship(back_populates="product")


class ProductPublic(ProductBase):
    id: uuid.UUID
    insurer: InsurerPublic | None = None


class ProductsPublic(SQLModel):
    data: list[ProductPublic]
    count: int


# ==========================================
# Client
# ==========================================


class ClientBase(SQLModel):
    model_config = ConfigDict(validate_assignment=True)  # type: ignore
    client_type: str = Field(default="Individual", max_length=50)
    name: str = Field(index=True, max_length=255)
    kra_pin: str = Field(unique=True, index=True, max_length=50)
    email: str | None = Field(default=None, max_length=255)
    phone: str = Field(max_length=50)
    postal_number: str | None = Field(default=None, max_length=50)
    postal_code: str | None = Field(default=None, max_length=20)
    town: str | None = Field(default=None, max_length=100)
    # Additional named contacts (e.g. fleet manager, accountant).
    # Schema: [{"name": str, "role": str, "phone": str, "email": str}]
    contacts: list[dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))


class ClientCreate(ClientBase):
    pass


class ClientUpdate(SQLModel):
    client_type: str | None = None
    name: str | None = None
    kra_pin: str | None = None
    email: str | None = None
    phone: str | None = None
    postal_number: str | None = None
    postal_code: str | None = None
    town: str | None = None
    contacts: list[dict[str, Any]] | None = None


class Client(ClientBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    policies: list["Policy"] = Relationship(back_populates="client")
    invoices: list["Invoice"] = Relationship(back_populates="client")
    receipts: list["Receipt"] = Relationship(back_populates="client")


class ClientPublic(ClientBase):
    id: uuid.UUID


class ClientsPublic(SQLModel):
    data: list[ClientPublic]
    count: int


# ==========================================
# Policy
#
# A Policy is the long-lived contract. It is the single source of truth
# for WHAT is being insured (risk_details). Coverage period and premium
# are per-term concerns that belong on RiskNote, not here.
#
# risk_details schema is intentionally open (JSON) because it varies by
# class of insurance (motor needs reg/make/value; fire needs location/
# sum insured; medical needs beneficiary count). Validation happens in
# the service layer using class_of_insurance from the related Product.
# ==========================================


class PolicyBase(SQLModel):
    model_config = ConfigDict(validate_assignment=True)  # type: ignore
    policy_number: str = Field(unique=True, index=True, max_length=100)
    client_id: uuid.UUID = Field(foreign_key="client.id", index=True)
    product_id: uuid.UUID = Field(foreign_key="product.id", index=True)
    status: PolicyStatus = Field(default=PolicyStatus.ACTIVE)
    # inception_date = when this policy was first taken out. Never changes.
    inception_date: date = Field(default_factory=date.today)
    # risk_details = authoritative record of what is insured.
    # Endorsements update this in-place; the RiskNote records the diff.
    risk_details: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(SQLModel):
    policy_number: str | None = None
    product_id: uuid.UUID | None = None
    status: PolicyStatus | None = None
    risk_details: dict[str, Any] | None = None


class Policy(PolicyBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    client: "Client" = Relationship(back_populates="policies")
    product: "Product" = Relationship(back_populates="policies")
    risk_notes: list["RiskNote"] = Relationship(back_populates="policy")
    claims: list["Claim"] = Relationship(back_populates="policy")
    renewal_workflows: list["RenewalWorkflow"] = Relationship(back_populates="policy")


class PolicyPublic(PolicyBase):
    id: uuid.UUID
    product: ProductPublic | None = None
    # Deliberately no computed fields here. Callers that need current
    # coverage period or premium should load the active RiskNote explicitly.
    # Hiding relationship traversal inside computed properties caused
    # subtle loading bugs in the previous model.


class PoliciesPublic(SQLModel):
    data: list[PolicyPublic]
    count: int


# ==========================================
# RiskNote
#
# A RiskNote is the document issued per transaction (New Business,
# Renewal, Endorsement, Cancellation). It records the terms for a
# specific coverage period.
#
# Critically: it does NOT store a copy of risk_details. That data lives
# on Policy. For endorsements, change_log records only the diff
# ({"field": {"from": old, "to": new}}), keeping history lean.
#
# The chain of notes for a policy is navigable via previous_risk_note_id,
# forming a linked list: NB → Renewal 1 → Renewal 2.
# ==========================================


class RiskNoteBase(SQLModel):
    policy_id: uuid.UUID = Field(foreign_key="policy.id", index=True)
    risk_note_number: str | None = Field(
        default=None, unique=True, index=True, max_length=100
    )
    transaction_type: TransactionType
    status: RiskNoteStatus = Field(default=RiskNoteStatus.DRAFT)
    # Links to the note this one supersedes. Null for New Business.
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
    total_amount: Decimal = Field(sa_column=Column(Numeric(precision=15, scale=2)))


class RiskNoteCreate(RiskNoteBase):
    # taxes: {"stamp_duty": 40, "phcf": 0.25, ...}
    taxes: dict[str, Any] = Field(default_factory=dict)
    special_clauses: list[str] = Field(default_factory=list)
    # Only populated for Endorsement notes. Records field-level diff.
    # Schema: {"risk_details.vehicle.value": {"from": 1_000_000, "to": 1_200_000}}
    change_log: dict[str, Any] = Field(default_factory=dict)


class RiskNoteUpdate(SQLModel):
    risk_note_number: str | None = None
    status: RiskNoteStatus | None = None
    effective_date: date | None = None
    coverage_start: date | None = None
    coverage_end: date | None = None
    net_premium: Decimal | None = None
    total_amount: Decimal | None = None
    taxes: dict[str, Any] | None = None
    special_clauses: list[str] | None = None
    change_log: dict[str, Any] | None = None


class RiskNote(RiskNoteBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    policy: "Policy" = Relationship(back_populates="risk_notes")
    invoice_line_items: list["InvoiceLineItem"] = Relationship(
        back_populates="risk_note"
    )
    allocations: list["ReceiptAllocation"] = Relationship(back_populates="risk_note")
    taxes: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    special_clauses: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    change_log: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class RiskNotePublic(RiskNoteBase):
    id: uuid.UUID
    taxes: dict[str, Any] = Field(default_factory=dict)
    special_clauses: list[str] = Field(default_factory=list)
    change_log: dict[str, Any] = Field(default_factory=dict)


class RiskNotesPublic(SQLModel):
    data: list[RiskNotePublic]
    count: int


# ==========================================
# Renewal Workflow
#
# Created automatically by a scheduler when a policy's active RiskNote
# has coverage_end within the alert window. Everything after creation
# is human-driven — the system tracks state and handles email dispatch.
#
# The authoritative premium for the new term lives on the RiskNote
# created at completion, NOT here. quoted_premium is a working field
# used during the review/negotiation stage only.
# ==========================================


class RenewalWorkflowBase(SQLModel):
    policy_id: uuid.UUID = Field(foreign_key="policy.id", index=True)
    # The note whose coverage_end triggered this workflow.
    expiring_risk_note_id: uuid.UUID = Field(foreign_key="risknote.id", index=True)
    status: RenewalStatus = Field(default=RenewalStatus.PENDING)
    # Filled in when team receives and reviews the insurer's renewal notice.
    insurer_notice_received_at: datetime | None = None
    insurer_notice_notes: str | None = None  # what changed vs last term
    quoted_premium: Decimal | None = Field(
        default=None, sa_column=Column(Numeric(precision=15, scale=2))
    )
    new_coverage_start: date | None = None
    new_coverage_end: date | None = None
    # Filled when team confirms the review.
    reviewed_by_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", index=True
    )
    reviewed_at: datetime | None = None
    # Filled when the client payment notice email is sent.
    client_notified_at: datetime | None = None
    # Filled when the renewal is complete and a new RiskNote is issued.
    completed_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.now)


class RenewalWorkflowCreate(RenewalWorkflowBase):
    pass


class RenewalWorkflowUpdate(SQLModel):
    status: RenewalStatus | None = None
    insurer_notice_received_at: datetime | None = None
    insurer_notice_notes: str | None = None
    quoted_premium: Decimal | None = None
    new_coverage_start: date | None = None
    new_coverage_end: date | None = None
    reviewed_by_id: uuid.UUID | None = None
    reviewed_at: datetime | None = None
    client_notified_at: datetime | None = None
    completed_at: datetime | None = None


class RenewalWorkflow(RenewalWorkflowBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    policy: "Policy" = Relationship(back_populates="renewal_workflows")


class RenewalWorkflowPublic(RenewalWorkflowBase):
    id: uuid.UUID


class RenewalWorkflowsPublic(SQLModel):
    data: list[RenewalWorkflowPublic]
    count: int


# ==========================================
# Invoice & Line Items
#
# An Invoice is raised against a Client for one or more RiskNotes.
# The line items are the bridge — each line item points at one RiskNote.
# This means the Invoice never needs to store a copy of policy or
# premium data; it's all reachable via the line item → risk note chain.
#
# Payment status is derived from balance_due, not stored as a redundant
# enum on RiskNote. A RiskNote is "paid" when its line item's invoice
# has balance_due == 0.
# ==========================================


class InvoiceBase(SQLModel):
    model_config = ConfigDict(validate_assignment=True)  # type: ignore
    invoice_number: str = Field(unique=True, index=True, max_length=100)
    client_id: uuid.UUID = Field(foreign_key="client.id", index=True)
    date_issued: date = Field(default_factory=date.today)
    due_date: date | None = None
    status: InvoiceStatus = Field(default=InvoiceStatus.UNPAID)
    total_amount: Decimal = Field(
        default=Decimal("0.00"), sa_column=Column(Numeric(precision=15, scale=2))
    )
    balance_due: Decimal = Field(
        default=Decimal("0.00"), sa_column=Column(Numeric(precision=15, scale=2))
    )
    notes: str | None = None


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceBulkCreate(SQLModel):
    """Create a single invoice covering multiple risk notes at once."""

    client_id: uuid.UUID
    risk_note_ids: list[uuid.UUID]
    date_issued: date = Field(default_factory=date.today)
    due_date: date | None = None
    notes: str | None = None


class InvoiceUpdate(SQLModel):
    due_date: date | None = None
    status: InvoiceStatus | None = None
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


class InvoiceLineItemPublic(InvoiceLineItemBase):
    id: uuid.UUID
    risk_note: RiskNotePublic | None = None


class InvoicePublic(InvoiceBase):
    id: uuid.UUID
    line_items: list[InvoiceLineItemPublic] = []
    allocations: list["ReceiptAllocationPublic"] = []


class InvoicesPublic(SQLModel):
    data: list[InvoicePublic]
    count: int


# ==========================================
# Receipt & Allocations
#
# A Receipt records money received from a client. The amount may cover
# multiple invoices, so it is split across them via ReceiptAllocation.
# unallocated_amount = amount - sum(allocations). This is the only place
# that tracks whether money has been applied somewhere.
# ==========================================


class ReceiptBase(SQLModel):
    receipt_number: str = Field(unique=True, index=True, max_length=100)
    client_id: uuid.UUID = Field(foreign_key="client.id", index=True)
    date_received: date
    amount: Decimal = Field(sa_column=Column(Numeric(precision=15, scale=2)))
    unallocated_amount: Decimal = Field(
        default=Decimal("0.00"), sa_column=Column(Numeric(precision=15, scale=2))
    )
    mode: str = Field(max_length=50)  # "MPESA", "Bank Transfer", "Cheque"
    reference: str = Field(max_length=100)  # MPESA code, cheque number, etc.
    notes: str | None = None
    status: ReceiptStatus = Field(default=ReceiptStatus.ACTIVE)
    created_by_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", index=True
    )


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptUpdate(SQLModel):
    date_received: date | None = None
    mode: str | None = None
    reference: str | None = None
    notes: str | None = None
    status: ReceiptStatus | None = None


class Receipt(ReceiptBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    client: "Client" = Relationship(back_populates="receipts")
    allocations: list["ReceiptAllocation"] = Relationship(back_populates="receipt")


class ReceiptPublic(ReceiptBase):
    id: uuid.UUID
    allocations: list["ReceiptAllocationPublic"] = []


class ReceiptsPublic(SQLModel):
    data: list[ReceiptPublic]
    count: int


class ReceiptAllocationBase(SQLModel):
    receipt_id: uuid.UUID = Field(foreign_key="receipt.id", index=True)
    invoice_id: uuid.UUID = Field(foreign_key="invoice.id", index=True)
    # risk_note_id here lets you see exactly which note a payment covers
    # without having to traverse invoice → line_items. Useful for statements.
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
    risk_note: Optional["RiskNote"] = Relationship(back_populates="allocations")


class ReceiptAllocationPublic(ReceiptAllocationBase):
    id: uuid.UUID


# ==========================================
# Claims
# ==========================================


class ClaimBase(SQLModel):
    claim_number: str = Field(unique=True, index=True, max_length=100)
    policy_id: uuid.UUID = Field(foreign_key="policy.id", index=True)
    date_of_loss: date
    date_reported: date = Field(default_factory=date.today)
    description: str
    status: ClaimStatus = Field(default=ClaimStatus.REPORTED)
    reserve_amount: Decimal = Field(
        default=Decimal("0.00"), sa_column=Column(Numeric(precision=15, scale=2))
    )


class ClaimCreate(ClaimBase):
    pass


class ClaimUpdate(SQLModel):
    date_of_loss: date | None = None
    description: str | None = None
    status: ClaimStatus | None = None
    reserve_amount: Decimal | None = None


class Claim(ClaimBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    policy: "Policy" = Relationship(back_populates="claims")
    events: list["ClaimEvent"] = Relationship(back_populates="claim")


class ClaimPublic(ClaimBase):
    id: uuid.UUID


class ClaimsPublic(SQLModel):
    data: list[ClaimPublic]
    count: int


class ClaimEventBase(SQLModel):
    claim_id: uuid.UUID = Field(foreign_key="claim.id", index=True)
    event_type: ClaimEventType
    description: str
    created_by_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", index=True
    )
    created_at: datetime = Field(default_factory=datetime.now)


class ClaimEventCreate(ClaimEventBase):
    pass


class ClaimEvent(ClaimEventBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    claim: "Claim" = Relationship(back_populates="events")


class ClaimEventPublic(ClaimEventBase):
    id: uuid.UUID


class ClaimEventsPublic(SQLModel):
    data: list[ClaimEventPublic]
    count: int


# ==========================================
# Documents
#
# Generic attachment store. entity_type + entity_id form a polymorphic
# reference — one table covers documents for clients, policies, claims,
# and risk notes without needing four separate document tables.
# ==========================================


class DocumentBase(SQLModel):
    document_type: DocumentType
    entity_type: DocumentEntityType
    entity_id: uuid.UUID = Field(index=True)
    file_path: str
    mime_type: str | None = None
    uploaded_at: datetime = Field(default_factory=datetime.now)
    uploaded_by_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", index=True
    )
    # Free-form metadata: original filename, file size, description, etc.
    doc_metadata: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(SQLModel):
    document_type: DocumentType | None = None
    doc_metadata: dict[str, Any] | None = None


class Document(DocumentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class DocumentPublic(DocumentBase):
    id: uuid.UUID


class DocumentsPublic(SQLModel):
    data: list[DocumentPublic]
    count: int


# ==========================================
# Late binding — resolve forward references
# ==========================================

InvoiceLineItemPublic.model_rebuild()
InvoicePublic.model_rebuild()
InvoicesPublic.model_rebuild()
ReceiptPublic.model_rebuild()
ReceiptsPublic.model_rebuild()
PolicyPublic.model_rebuild()
PoliciesPublic.model_rebuild()
RiskNotePublic.model_rebuild()
RiskNotesPublic.model_rebuild()
