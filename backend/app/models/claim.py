import uuid
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, Numeric
from sqlmodel import Field, Relationship, SQLModel

from .audit import AuditMixin

if TYPE_CHECKING:
    from .policy import Policy



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


class ClaimBase(AuditMixin, SQLModel):
    claim_number: str = Field(unique=True, index=True)
    policy_id: uuid.UUID = Field(foreign_key="policy.id", index=True)
    date_of_loss: date
    date_reported: date = Field(default_factory=date.today)
    description: str
    status: ClaimStatus = Field(default=ClaimStatus.REPORTED)
    reserve_amount: Decimal = Field(
        default=Decimal("0.0"), sa_column=Column(Numeric(precision=15, scale=2))
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


class ClaimEventPublic(ClaimEventBase):
    id: uuid.UUID


class ClaimEvent(ClaimEventBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    claim: "Claim" = Relationship(back_populates="events")


class ClaimEventsPublic(SQLModel):
    data: list[ClaimEventPublic]
    count: int
