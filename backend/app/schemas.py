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
    year_of_manufacture: int | None = None
    sum_insured: Decimal = Field(default=Decimal("0"))

    @field_validator("sum_insured", mode="before")
    @classmethod
    def parse_sum_insured(cls, v: Any) -> Decimal:
        from app.utils import parse_decimal
        return parse_decimal(v)


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

    vehicle: MotorVehicleDetails
    extensions: MotorExtensions = Field(default_factory=MotorExtensions)
    # Terms as plain text/markdown
    benefits_and_limits: str = ""
    excesses: str = ""
    special_clauses: str = ""

    @pydantic.model_validator(mode="before")
    @classmethod
    def wrap_legacy_and_flat_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        
        # 1. Handle legacy "vehicle_details" -> "vehicle"
        if "vehicle_details" in data and "vehicle" not in data:
            data["vehicle"] = data.pop("vehicle_details")
            
        # 2. Handle legacy "added_benefits" -> "extensions"
        if "added_benefits" in data and "extensions" not in data:
            data["extensions"] = data.pop("added_benefits")

        # 3. Handle flat fields if they exist at top level or nested 'terms'
        if "terms" in data and isinstance(data["terms"], dict):
            terms = data.pop("terms")
            for k, v in terms.items():
                if k not in data:
                    data[k] = v

        vehicle_keys = {"registration_number", "make", "year_of_manufacture", "sum_insured"}
        extension_keys = {"pvt", "excess_protector", "om_rescue_plus", "passenger_liability"}
        
        vehicle = data.get("vehicle", {})
        for k in vehicle_keys:
            if k in data:
                vehicle[k] = data.pop(k)
        
        extensions = data.get("extensions", {})
        for k in extension_keys:
            if k in data:
                extensions[k] = data.pop(k)
        
        if vehicle:
            data["vehicle"] = vehicle
        if extensions:
            data["extensions"] = extensions
            
        # 4. Handle terms that might be list/dict in legacy data
        for term_key in ["benefits_and_limits", "excesses", "special_clauses"]:
            val = data.get(term_key)
            if isinstance(val, (list, dict)):
                import json
                data[term_key] = json.dumps(val, indent=2)
            elif val is None:
                data[term_key] = ""
                
        return data
