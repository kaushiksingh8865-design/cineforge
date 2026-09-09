from pydantic import BaseModel, Field

from app.ai.schemas.statechange import StateChange


class SaveRequest(BaseModel):
    project_id: int
    scene_id: int

    state_changes: list[StateChange] = Field(
        default_factory=list
    )
 # the save request come from user 
 