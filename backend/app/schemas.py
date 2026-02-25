import uuid
import pydantic
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


class MotorVehicleDetails(BaseModel):
    registration_number: str = Field(..., min_length=1)
    make: str = Field(..., min_length=1)
    year_of_manufacture: int = Field(...)
    sum_insured: Decimal = Field(...)

    @field_validator("sum_insured", mode="before")
    @classmethod
    def parse_sum_insured(cls, v: Any) -> Decimal:
        from app.services.rating import RatingStrategy
        return RatingStrategy.parse_decimal(v)


class MotorExtensions(BaseModel):
    pvt: bool = False
    excess_protector: bool = False
    om_rescue_plus: bool = False
    passenger_liability: bool = False


class MotorPrivateRiskDetails(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore"
    )

    vehicle_details: MotorVehicleDetails
    benefits_and_limits: dict[str, Any] = Field(default_factory=dict)
    excesses: dict[str, Any] = Field(default_factory=dict)
    added_benefits: MotorExtensions
    special_clauses: list[str] = Field(default_factory=list)

    @pydantic.model_validator(mode="before")
    @classmethod
    def wrap_flat_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        
        # If already structured correctly, return as is
        if "vehicle_details" in data and "added_benefits" in data:
            return data
            
        vehicle_keys = {"registration_number", "make", "year_of_manufacture", "sum_insured"}
        extension_keys = {"pvt", "excess_protector", "om_rescue_plus", "passenger_liability"}
        
        vehicle = data.get("vehicle_details", {})
        for k in vehicle_keys:
            if k in data:
                vehicle[k] = data.pop(k)
        
        added = data.get("added_benefits") or data.get("extensions") or {}
        for k in extension_keys:
            if k in data:
                added[k] = data.pop(k)
        
        if vehicle:
            data["vehicle_details"] = vehicle
        if added:
            data["added_benefits"] = added
            
        return data
