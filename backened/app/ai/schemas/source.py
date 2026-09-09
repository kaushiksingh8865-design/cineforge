
from typing import Literal

from pydantic import BaseModel, Field


class SourceFileCreate(BaseModel):
    name: str
    source_type: Literal["uploaded_file", "screenplay"]
    mime_type: str | None = None
    file_path: str | None = None
    content: str | None = None
    file_metadata: dict = Field(default_factory=dict)


class SourceFileResponse(BaseModel):
    id: int
    project_id: int
    name: str
    source_type: Literal["uploaded_file", "screenplay"]
    mime_type: str | None
    file_path: str | None
    content: str | None
    file_metadata: dict