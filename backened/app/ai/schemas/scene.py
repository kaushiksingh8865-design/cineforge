from pydantic import BaseModel , Field
from app.ai.schemas.characterstate import CharacterState
from app.ai.schemas.propstate import PropState


class Scene(BaseModel):
    scene_number:int
    header:str 
    location:str 
    time_of_day:str

    characters: list[CharacterState] = Field(default_factory=list)
  
    props: list[PropState]= Field(default_factory=list)
    visual_prompt:str |None =None

    

    
    
