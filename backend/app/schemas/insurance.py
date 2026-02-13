from pydantic import BaseModel, Field, ConfigDict

class MotorPrivateRiskDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    registration_number: str = Field(..., alias="Reg. No", min_length=1)
    make: str = Field(..., alias="Make", min_length=1)
    year_of_manufacture: int | str = Field(..., alias="Year")
    value: float | str = Field(..., alias="Value Kshs.")
