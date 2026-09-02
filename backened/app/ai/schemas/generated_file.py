from datetime import datetime

from pydantic import BaseModel, Field


class GeneratedFile(BaseModel):
    file_type: str
    file_path: str
    metadata: dict = Field(default_factory=dict)
    created_at: datetime | None = None