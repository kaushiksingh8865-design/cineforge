from pydantic import BaseModel , Field

class characterstate(BaseModel):
    name:str
    status:str | None = None
    Injuries: list[str] = Field(default_factory =list)
    wardrobe: list[str] =Field(default_factory = list)


class PropState(BaseModel):
    name:str
    holder:str|None = None
    location:str|None =None


class Scene(BaseModel):
    scene_number:int
    header:str |None = None
    location:str |None =None
    time_of_day:str

    characters: list[characterstate] = Field(default_factory=list)
    props: list[PropState]= Field(default_factory=list)
    visual_prompt:str |None =None

    

    
    
