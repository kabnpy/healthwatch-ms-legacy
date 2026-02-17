from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MotorPrivateRiskDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    registration_number: str = Field(..., alias="Reg. No", min_length=1)
    make: str = Field(..., alias="Make", min_length=1)
    year_of_manufacture: int = Field(..., alias="Year")
    value: float = Field(..., alias="Value Kshs.")

    @field_validator("year_of_manufacture", mode="before")
    @classmethod
    def parse_year(cls, v: Any) -> int:
        if isinstance(v, str):
            # Remove commas and whitespace
            v = v.replace(",", "").strip()
            if not v:
                return 0
            return int(float(v))
        return int(v)

    @field_validator("value", mode="before")
    @classmethod
    def parse_value(cls, v: Any) -> float:
        if isinstance(v, str):
            # Remove commas and whitespace
            v = v.replace(",", "").strip()
            if not v:
                return 0.0
            return float(v)
        return float(v)
