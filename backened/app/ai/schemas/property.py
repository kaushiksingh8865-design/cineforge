from pydantic import BaseModel


class Prop(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None