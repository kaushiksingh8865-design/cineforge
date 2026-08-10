from pydantic import BaseModel

class Scene(BaseModel):
    scene_number:int
    location:str
    time_of_day:str
    
    

    
    
