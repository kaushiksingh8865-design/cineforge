from pydantic import BaseModel


class CineForgeRequest(BaseModel):
    project_id: int
    scene_number: int
    request: str