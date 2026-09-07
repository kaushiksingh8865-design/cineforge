from typing import Any, Literal

from pydantic import BaseModel


class StateChange(BaseModel):
    target_type: Literal["scene", "character", "prop"]
    target_id: int
    scene_id: int
    field: str
    old_value: Any
    new_value: Any