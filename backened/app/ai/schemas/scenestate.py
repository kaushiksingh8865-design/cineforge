from datetime import datetime
from pydantic import BaseModel, Field

class SceneState(BaseModel):
    scene_id:int
    state_data:dict = Field(default_factory= dict)
    created_at:datetime | None = None
    updated_at: datetime | None = None

    