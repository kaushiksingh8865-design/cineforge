
import os
from pathlib import Path

from google import genai
from google.genai import types

from app.ai.core.settings import settings
from app.ai.schemas.image import (
    GeneratedImage,
    ImageGenerationResult,
)


class ImageGenerator:

    def __init__(self):
        os.environ.setdefault(
            "GEMINI_API_KEY",
            settings.gemini_api_key,
        )

        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

        self.model = "gemini-3.1-flash-image"

    async def generate(
        self,
        prompt: str,
        output_path: str,
    ) -> ImageGenerationResult:

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                ),
            ),
        )

        output_file = Path(output_path)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        image_found = False

        for part in response.parts:

            if part.inline_data is not None:

                image = part.as_image()

                image.save(output_file)

                image_found = True

                break

        if not image_found:
            raise RuntimeError(
                "Image generation returned no image."
            )

        return ImageGenerationResult(
            prompt=prompt,
            images=[
                GeneratedImage(
                    mime_type="image/png",
                    file_path=str(output_file),
                )
            ],
        )