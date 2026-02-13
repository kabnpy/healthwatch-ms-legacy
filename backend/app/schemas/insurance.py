from pydantic import BaseModel, Field, ConfigDict

class MotorPrivateRiskDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    registration_number: str = Field(..., alias="Reg. No", min_length=1)
    make: str = Field(..., alias="Make", min_length=1)
    model: str = Field(..., alias="Model", min_length=1)
    year_of_manufacture: int = Field(..., alias="Year", gt=1900)
    value: float = Field(..., alias="Value Kshs.", gt=0)
