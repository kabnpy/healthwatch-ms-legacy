import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class AuditMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    deleted_at: datetime | None = Field(default=None, index=True)
    deleted_by_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", index=True
    )
