from datetime import datetime

from pydantic import BaseModel, Field


class Version(BaseModel):
    version_number: str
    description: str | None = None
    state_snapshot: dict = Field(default_factory=dict)
    created_at: datetime | None = None