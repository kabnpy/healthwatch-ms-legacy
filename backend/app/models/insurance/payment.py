import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .policy import RiskNote

# ==========================================
# Payment Models
# ==========================================


class PaymentBase(SQLModel):
    receipt_number: str = Field(unique=True)
    date_received: date
    amount: float
    mode: str
    reference: str


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(SQLModel):
    receipt_number: str | None = None
    date_received: date | None = None
    amount: float | None = None
    mode: str | None = None
    reference: str | None = None


class PaymentPublic(PaymentBase):
    id: uuid.UUID


class Payment(PaymentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    allocations: list["PaymentAllocation"] = Relationship(back_populates="payment")


class PaymentsPublic(SQLModel):
    data: list[PaymentPublic]
    count: int


# ==========================================
# Payment Allocation Models
# ==========================================


class PaymentAllocationBase(SQLModel):
    payment_id: uuid.UUID = Field(foreign_key="payment.id", primary_key=True)
    risk_note_id: uuid.UUID = Field(foreign_key="risknote.id", primary_key=True)
    amount_allocated: float


class PaymentAllocationCreate(PaymentAllocationBase):
    pass


class PaymentAllocationUpdate(SQLModel):
    amount_allocated: float | None = None


class PaymentAllocationPublic(PaymentAllocationBase):
    pass


class PaymentAllocation(PaymentAllocationBase, table=True):
    payment: "Payment" = Relationship(back_populates="allocations")
    risk_note: "RiskNote" = Relationship(back_populates="allocations")


class PaymentAllocationsPublic(SQLModel):
    data: list[PaymentAllocationPublic]
    count: int
