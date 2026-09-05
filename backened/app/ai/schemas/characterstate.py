from pydantic import BaseModel , Field



class CharacterState(BaseModel):
    
    character_id:int
    scene_id:int
    status:str | None = None
    injuries: list[str] = Field(default_factory =list)
    wardrobe: list[str] =Field(default_factory = list)
