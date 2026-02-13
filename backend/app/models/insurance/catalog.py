import uuid
from typing import TYPE_CHECKING, Any, Optional

from pydantic import ConfigDict
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel
from ..mixins import AuditMixin

if TYPE_CHECKING:
    from .policy import Policy

from enum import Enum


class PricingStrategy(str, Enum):
    PERCENTAGE = "Percentage"
    FIXED_TIERED = "FixedTiered"
    MANUAL = "Manual"


# ==========================================
# Insurer Models
# ==========================================


class InsurerBase(AuditMixin, SQLModel):
    model_config = ConfigDict(validate_assignment=True)
    name: str = Field(unique=True, index=True)
    email: str | None = None
    phone: str | None = None


class InsurerCreate(InsurerBase):
    pass


class InsurerUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class InsurerPublic(InsurerBase):
    id: uuid.UUID


class Insurer(InsurerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    products: list["Product"] = Relationship(back_populates="insurer")


class InsurersPublic(SQLModel):
    data: list[InsurerPublic]
    count: int


# ==========================================
# Product Models
# ==========================================


class ProductBase(AuditMixin, SQLModel):
    insurer_id: uuid.UUID = Field(foreign_key="insurer.id")
    name: str
    class_of_insurance: str  # "Motor Private", "Fire"

    product_details: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)

    # Defaults to pre-fill the form
    default_commission_rate: float = 10.0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    insurer_id: uuid.UUID | None = None
    name: str | None = None
    class_of_insurance: str | None = None
    product_details: dict[str, Any] | None = None
    default_commission_rate: float | None = None


class ProductPublic(ProductBase):
    id: uuid.UUID
    insurer: Optional["InsurerPublic"] = None


class Product(ProductBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    insurer: "Insurer" = Relationship(back_populates="products")
    policies: list["Policy"] = Relationship(back_populates="product")


class ProductsPublic(SQLModel):
    data: list[ProductPublic]
    count: int


ProductPublic.model_rebuild()
