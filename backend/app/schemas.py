import json
import uuid
from decimal import Decimal
from typing import Annotated, Any, Literal

import pydantic
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
    type: Literal["motor"] = "motor"  # type: ignore[assignment]
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
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    vehicle: MotorVehicleDetails
    extensions: MotorExtensions = Field(default_factory=MotorExtensions)
    # Reworked terms structure: generic dict of plain text strings
    terms: dict[str, str] = Field(default_factory=dict)

    @pydantic.model_validator(mode="before")
    @classmethod
    def wrap_legacy_and_flat_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        # 1. Handle legacy sub-object names (case-insensitive)
        for k in list(data.keys()):
            low_k = k.lower()
            if low_k == "vehicle_details" or low_k == "vehicle":
                if "vehicle" not in data or k == "VEHICLE":
                    data["vehicle"] = data.pop(k)
            elif low_k == "added_benefits" or low_k == "extensions":
                if "extensions" not in data or k == "EXTENSIONS":
                    data["extensions"] = data.pop(k)

        # 2. Extract potential sub-objects
        vehicle = data.get("vehicle", {})
        if not isinstance(vehicle, dict):
            vehicle = {}

        extensions = data.get("extensions", {})
        if not isinstance(extensions, dict):
            extensions = {}

        existing_terms = data.get("terms", {})
        if not isinstance(existing_terms, dict):
            existing_terms = {}

        # 3. Define mappings
        vehicle_mapping = {
            "Reg. No": "registration_number",
            "registration_number": "registration_number",
            "Make": "make",
            "make": "make",
            "Year": "year_of_manufacture",
            "year_of_manufacture": "year_of_manufacture",
            "Value Kshs.": "sum_insured",
            "sum_insured": "sum_insured",
        }

        extension_mapping = {
            "pvt": "pvt",
            "excess_protector": "excess_protector",
            "om_rescue_plus": "om_rescue_plus",
            "passenger_liability": "passenger_liability",
        }

        term_keys = ["benefits_and_limits", "excesses", "special_clauses"]

        # 4. Pull keys from top-level data AND nested objects into clean normalized structures
        final_vehicle = {}
        final_extensions = {}
        final_terms = existing_terms.copy()

        # Helper to get the best value among candidates
        def get_best_val(*candidates: Any) -> Any:
            for c in candidates:
                if c is not None and c != "[ EMPTY ]" and c != "":
                    return c
            return None

        # 5. Execute mappings
        for legacy_key, semantic_key in vehicle_mapping.items():
            top_val = data.get(legacy_key)
            nested_val = vehicle.get(legacy_key)

            best = get_best_val(top_val, nested_val)
            if best is not None:
                final_vehicle[semantic_key] = best
                if legacy_key in data:
                    data.pop(legacy_key)

        for legacy_key, semantic_key in extension_mapping.items():
            top_val = data.get(legacy_key)
            nested_val = extensions.get(legacy_key)

            best = get_best_val(top_val, nested_val)
            if best is not None:
                final_extensions[semantic_key] = best
                if legacy_key in data:
                    data.pop(legacy_key)

        # 6. Group terms into the new dictionary
        for term_key in term_keys:
            # Check top level first, then inside existing 'terms' dict
            val = data.get(term_key) or existing_terms.get(term_key)
            if val is not None:
                if isinstance(val, list | dict):
                    final_terms[term_key] = json.dumps(val, indent=2)
                else:
                    final_terms[term_key] = str(val)

                if term_key in data:
                    data.pop(term_key)

        # 7. Final assignment with strict satisfaction
        # If we are missing required fields for the schema, we inject [ EMPTY ] placeholders
        if "registration_number" not in final_vehicle:
            final_vehicle["registration_number"] = "[ EMPTY ]"
        if "make" not in final_vehicle:
            final_vehicle["make"] = "[ EMPTY ]"

        data["vehicle"] = final_vehicle
        data["extensions"] = final_extensions
        data["terms"] = final_terms

        return data
