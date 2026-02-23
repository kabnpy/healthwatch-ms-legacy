import uuid
import re
from decimal import Decimal
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BenefitLineItem(BaseModel):
    name: str
    amount: Decimal


class BaseFinancialBreakdown(BaseModel):
    type: Literal["base"] = "base"
    net_premium: Decimal
    taxes: dict[str, Decimal] = Field(default_factory=dict)
    commission_amount: Decimal
    total_amount: Decimal


class MotorFinancialBreakdown(BaseFinancialBreakdown):
    type: Literal["motor"] = "motor"
    benefits: list[BenefitLineItem] = Field(default_factory=list)
    basic_rate: Decimal | None = None
    is_high_end: bool = False


class FinancialBreakdown(BaseModel):
    product_class: str
    breakdown: Annotated[
        MotorFinancialBreakdown | BaseFinancialBreakdown,
        Field(discriminator="type"),
    ]


class QuoteRequest(BaseModel):
    product_id: uuid.UUID
    risk_details: dict[str, Any]


class QuoteResponse(BaseModel):
    breakdown: MotorFinancialBreakdown | BaseFinancialBreakdown


class MotorPrivateRiskDetails(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore"
    )

    registration_number: str = Field(..., min_length=1)
    make: str = Field(..., min_length=1)
    year_of_manufacture: int = Field(...)
    sum_insured: Decimal = Field(...)

    @field_validator("sum_insured", mode="before")
    @classmethod
    def parse_sum_insured(cls, v: Any) -> Decimal:
        from app.services.rating import RatingStrategy
        return RatingStrategy.parse_decimal(v)


class MotorPrivateRiskDetailsLegacy(MotorPrivateRiskDetails):
    """Temporary helper for legacy data migration if needed"""
    model_config = ConfigDict(populate_by_name=True)
    registration_number: str = Field(..., alias="Reg. No")
    sum_insured: float = Field(..., alias="Value Kshs.")
