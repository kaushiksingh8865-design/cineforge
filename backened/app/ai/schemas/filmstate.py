from pydantic import BaseModel, Field


class CharacterFilmState(BaseModel):
    character_id: int
    name: str
    status: str | None = None
    injuries: list[str] = Field(default_factory=list)
    wardrobe: list[str] = Field(default_factory=list)


class PropFilmState(BaseModel):
    prop_id: int
    name: str
    holder: str | None = None
    location: str | None = None
    status: str | None = None


class FilmState(BaseModel):
    scene_id: int
    scene_state: dict = Field(default_factory=dict)
    characters: list[CharacterFilmState] = Field(default_factory=list)
    props: list[PropFilmState] = Field(default_factory=list)