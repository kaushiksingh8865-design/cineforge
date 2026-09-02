from pydantic import BaseModel , Field

class Character(BaseModel):
    id:int| None = None
    name: str
    