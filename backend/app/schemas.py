import uuid
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
        alias_generator=None,
        extra="ignore" # Allow sumInsured to be passed without crashing, though we prefer Value Kshs.
    )

    registration_number: str = Field(..., alias="Reg. No", min_length=1)
    make: str = Field(..., alias="Make", min_length=1)
    year_of_manufacture: int = Field(..., alias="Year")
    value: float = Field(..., alias="Value Kshs.")

    @field_validator("value", mode="before")
    @classmethod
    def parse_value(cls, v: Any) -> float:
        if v is None:
            return 0.0
        if isinstance(v, str):
            # Remove commas and whitespace, handle placeholders
            v = v.replace(",", "").replace("[ EMPTY ]", "").strip()
            # Handle KES prefix if present
            v = re.sub(r"[^\d.]", "", v)
            if not v:
                return 0.0
            return float(v)
        return float(v)
