from pydantic import BaseModel , Field



class CharacterState(BaseModel):
    name:str
    status:str | None = None
    injuries: list[str] = Field(default_factory =list)
    wardrobe: list[str] =Field(default_factory = list)
