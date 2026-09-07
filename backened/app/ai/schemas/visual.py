from pydantic import BaseModel, Field


class VisualShot(BaseModel):
    shot_type: str = Field(
        description="The type of shot, such as wide shot, medium shot, close-up, or extreme close-up."
    )
    camera_angle: str = Field(
        description="The camera angle and perspective."
    )
    composition: str = Field(
        description="How characters, objects, and the environment are arranged in the frame."
    )
    lighting: str = Field(
        description="The lighting design and visual treatment."
    )
    environment: str = Field(
        description="Important environmental and location details visible in the shot."
    )
    character_positioning: str = Field(
        description="Where the characters are positioned and what they are doing visually."
    )
    atmosphere: str = Field(
        description="The mood and visual atmosphere of the shot."
    )


class VisualResult(BaseModel):
    summary: str = Field(
        description="A concise description of the overall visual direction."
    )
    shots: list[VisualShot] = Field(
        default_factory=list,
        description="Ordered visual shots representing the scene."
    )
    image_prompt: str = Field(
        description="A detailed prompt suitable for an image generation model."
    )