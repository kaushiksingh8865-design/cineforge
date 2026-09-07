from pydantic import BaseModel, Field


class StoryBeat(BaseModel):
    description: str = Field(
        description="What happens in this story beat."
    )
    purpose: str = Field(
        description="The narrative purpose of this beat."
    )


class StoryResult(BaseModel):
    summary: str = Field(
        description="A concise summary of the proposed story development."
    )
    beats: list[StoryBeat] = Field(
        default_factory=list,
        description="Ordered story beats for the proposed scene or sequence."
    )
    dialogue_suggestions: list[str] = Field(
        default_factory=list,
        description="Optional dialogue suggestions relevant to the scene."
    )
    character_actions: list[str] = Field(
        default_factory=list,
        description="Important character actions or emotional developments."
    )