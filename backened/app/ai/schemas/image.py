from pydantic import BaseModel, Field


class GeneratedImage(BaseModel):
    mime_type: str = Field(
        description="MIME type of the generated image."
    )
    file_path: str = Field(
        description="Path where the generated image is stored."
    )


class ImageGenerationResult(BaseModel):
    prompt: str = Field(
        description="The prompt used for image generation."
    )
    images: list[GeneratedImage] = Field(
        default_factory=list,
        description="Generated image files."
    )