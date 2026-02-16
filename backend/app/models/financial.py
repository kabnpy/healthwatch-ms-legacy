import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import ConfigDict
from sqlalchemy import Numeric
from sqlmodel import Field, Relationship, SQLModel
from .mixins import AuditMixin
from .enums import InvoiceStatus, ReceiptStatus

if TYPE_CHECKING:
    from .client import Client
    from .policy import RiskNote, RiskNotePublic

# ==========================================
# Invoice Models (Pending Payment)
# ==========================================


class InvoiceBase(AuditMixin, SQLModel):
    model_config = ConfigDict(validate_assignment=True)
    invoice_number: str = Field(unique=True, index=True)
    client_id: uuid.UUID = Field(foreign_key="client.id", index=True)
    date_issued: date = Field(default_factory=date.today)
    due_date: date | None = None
    status: InvoiceStatus = Field(default=InvoiceStatus.UNPAID)  # Unpaid, Partial, Paid, Cancelled
    total_amount: Decimal = Field(
        default=Decimal("0.0"), sa_type=Numeric(precision=15, scale=2)
    )
    balance_due: Decimal = Field(
        default=Decimal("0.0"), sa_type=Numeric(precision=15, scale=2)
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


# ==========================================
# Invoice Line Item Models
# ==========================================


class InvoiceLineItemBase(SQLModel):
    invoice_id: uuid.UUID = Field(foreign_key="invoice.id", index=True)
    risk_note_id: uuid.UUID = Field(foreign_key="risknote.id", index=True)
    amount: Decimal = Field(sa_type=Numeric(precision=15, scale=2))
    description: str | None = None


class InvoiceLineItemCreate(InvoiceLineItemBase):
    pass


class InvoiceLineItem(InvoiceLineItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    invoice: "Invoice" = Relationship(back_populates="line_items")
    risk_note: "RiskNote" = Relationship(back_populates="invoice_line_items")


# ==========================================
# Receipt Models (Money Received)
# ==========================================


class ReceiptBase(AuditMixin, SQLModel):
    receipt_number: str = Field(unique=True, index=True)
    client_id: uuid.UUID = Field(foreign_key="client.id", index=True)
    date_received: date
    amount: Decimal = Field(sa_type=Numeric(precision=15, scale=2))
    unallocated_amount: Decimal = Field(
        default=Decimal("0.0"), sa_type=Numeric(precision=15, scale=2)
    )
    mode: str  # Cash, Cheque, MPESA, Bank Transfer
    reference: str  # Transaction ID, Cheque No
    notes: str | None = None
    status: ReceiptStatus = Field(default=ReceiptStatus.ACTIVE)
    created_by_id: uuid.UUID | None = Field(default=None, foreign_key="user.id", index=True)


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


# ==========================================
# Receipt Allocation Models
# ==========================================


class ReceiptAllocationBase(SQLModel):
    receipt_id: uuid.UUID = Field(foreign_key="receipt.id", index=True)
    invoice_id: uuid.UUID = Field(foreign_key="invoice.id", index=True)
    risk_note_id: uuid.UUID | None = Field(default=None, foreign_key="risknote.id", index=True)
    amount_allocated: Decimal = Field(sa_type=Numeric(precision=15, scale=2))


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


# ==========================================
# Public Schemas (Late Binding)
# ==========================================


class InvoiceLineItemPublic(InvoiceLineItemBase):
    id: uuid.UUID
    risk_note: Optional["RiskNotePublic"] = None


class InvoicePublic(InvoiceBase):
    id: uuid.UUID
    line_items: list[InvoiceLineItemPublic] = []
    allocations: list[ReceiptAllocationBase] = []


class InvoicesPublic(SQLModel):
    data: list[InvoicePublic]
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
