from pydantic import BaseModel


class FilmProject(BaseModel):
    title: str
    logline: str | None = None