from pydantic import BaseModel , Field
class PropState(BaseModel):
    name:str
    holder:str|None = None
    location:str|None =None
    status:str | None = None