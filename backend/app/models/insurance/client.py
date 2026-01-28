import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .policy import Policy

# ==========================================
# Client Models
# ==========================================


class ClientBase(SQLModel):
    client_type: str = Field(default="Individual")  # "Individual" or "Corporate"
    name: str = Field(index=True)
    kra_pin: str = Field(unique=True, index=True)
    email: str | None = None
    phone: str
    postal_address: str | None = None

    # Corporate specific
    contact_person: str | None = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(SQLModel):
    client_type: str | None = None
    name: str | None = None
    kra_pin: str | None = None
    email: str | None = None
    phone: str | None = None
    postal_address: str | None = None
    contact_person: str | None = None


class ClientPublic(ClientBase):
    id: uuid.UUID


class Client(ClientBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    policies: list["Policy"] = Relationship(back_populates="client")
    correspondence: list["Correspondence"] = Relationship(back_populates="client")


class ClientsPublic(SQLModel):
    data: list[ClientPublic]
    count: int


# ==========================================
# Correspondence Models
# ==========================================


class CorrespondenceBase(SQLModel):
    client_id: uuid.UUID = Field(foreign_key="client.id")
    subject: str
    summary: str | None = None  # For Search
    file_path: str
    date_logged: datetime = Field(default_factory=datetime.now)


class CorrespondenceCreate(CorrespondenceBase):
    pass


class CorrespondenceUpdate(SQLModel):
    client_id: uuid.UUID | None = None
    subject: str | None = None
    summary: str | None = None
    file_path: str | None = None
    date_logged: datetime | None = None


class CorrespondencePublic(CorrespondenceBase):
    id: uuid.UUID


class Correspondence(CorrespondenceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    client: "Client" = Relationship(back_populates="correspondence")


class CorrespondencesPublic(SQLModel):
    data: list[CorrespondencePublic]
    count: int
