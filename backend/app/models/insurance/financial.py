import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .client import Client
    from .policy import RiskNote

# ==========================================
# Invoice Models (Pending Payment)
# ==========================================


class InvoiceBase(SQLModel):
    invoice_number: str = Field(unique=True, index=True)
    client_id: uuid.UUID = Field(foreign_key="client.id")
    date_issued: date = Field(default_factory=date.today)
    due_date: date | None = None
    status: str = "Unpaid"  # Unpaid, Partial, Paid, Cancelled
    total_amount: float = 0.0
    balance_due: float = 0.0
    notes: str | None = None


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(SQLModel):
    invoice_number: str | None = None
    due_date: date | None = None
    status: str | None = None
    total_amount: float | None = None
    balance_due: float | None = None
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
    invoice_id: uuid.UUID = Field(foreign_key="invoice.id")
    risk_note_id: uuid.UUID = Field(foreign_key="risknote.id")
    amount: float
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


class ReceiptBase(SQLModel):
    receipt_number: str = Field(unique=True, index=True)
    client_id: uuid.UUID = Field(foreign_key="client.id")
    date_received: date
    amount: float
    unallocated_amount: float = Field(default=0.0)
    mode: str  # Cash, Cheque, MPESA, Bank Transfer
    reference: str  # Transaction ID, Cheque No
    notes: str | None = None
    status: str = "Active"  # Active, Voided
    created_by_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptUpdate(SQLModel):
    receipt_number: str | None = None
    date_received: date | None = None
    amount: float | None = None
    unallocated_amount: float | None = None
    mode: str | None = None
    reference: str | None = None
    notes: str | None = None
    status: str | None = None


# ==========================================
# Receipt Allocation Models
# ==========================================


class ReceiptAllocationBase(SQLModel):
    receipt_id: uuid.UUID = Field(foreign_key="receipt.id")
    invoice_id: uuid.UUID = Field(foreign_key="invoice.id")
    risk_note_id: uuid.UUID | None = Field(default=None, foreign_key="risknote.id")
    amount_allocated: float


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


class InvoicePublic(InvoiceBase):
    id: uuid.UUID
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
