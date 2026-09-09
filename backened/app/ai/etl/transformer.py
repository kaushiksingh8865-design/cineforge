
import os

from google.adk import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel, Field

from app.ai.core.settings import settings
from app.ai.schemas.scene import Scene
from app.ai.schemas.character import Character
from app.ai.schemas.property import Prop


os.environ.setdefault(
    "GEMINI_API_KEY",
    settings.gemini_api_key,
)


class ExtractedCharacter(BaseModel):
    name: str
    status: str | None = None
    injuries: list[str] = Field(default_factory=list)
    wardrobe: list[str] = Field(default_factory=list)


class ExtractedProp(BaseModel):
    name: str
    description: str | None = None
    holder: str | None = None
    location: str | None = None
    status: str | None = None


class ExtractedFilmData(BaseModel):
    scene: Scene
    characters: list[ExtractedCharacter] = Field(
        default_factory=list
    )
    props: list[ExtractedProp] = Field(
        default_factory=list
    )
    scene_state_data: dict = Field(
        default_factory=dict
    )


transformer_agent = Agent(
    name="source_transformer",
    model="gemini-3.6-flash",

    instruction="""
You are CineForge's Source Transformation Agent.

Your responsibility is to transform raw screenplay/source
text into structured filmmaking data.

Rules:

1. Use ONLY the supplied source text.
2. Do not perform web research.
3. Do not invent characters, props, locations, or events
   that are not supported by the source.
4. Extract the primary scene information.
5. Extract all characters explicitly present in the scene.
6. Extract all important props explicitly present in the scene.
7. Extract character state information such as:
   - status
   - injuries
   - wardrobe
8. Extract prop state information such as:
   - holder
   - location
   - status
9. Put scene-level dynamic information into
   scene_state_data.
10. If information is not present, use null or empty lists.
11. Preserve the wording and meaning of the source as much
    as practical.
12. This is an extraction/transformation operation,
    not creative story generation.
13. Return ONLY valid JSON.
14. Do not use markdown code fences.
""",
)


async def transform_source(
    source_text: str,
) -> ExtractedFilmData:

    session_service = InMemorySessionService()

    runner = Runner(
        app_name="cineforge_source_transformer",
        agent=transformer_agent,
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="cineforge_source_transformer",
        user_id="etl_user",
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=f"""
Transform the following source into structured
CineForge film data.

Return ONLY valid JSON with this structure:

{{
    "scene": {{
        "scene_number": 1,
        "header": "string",
        "location": "string",
        "time_of_day": "string",
        "characters": [],
        "props": [],
        "visual_prompt": null
    }},
    "characters": [
        {{
            "name": "string",
            "status": null,
            "injuries": [],
            "wardrobe": []
        }}
    ],
    "props": [
        {{
            "name": "string",
            "description": null,
            "holder": null,
            "location": null,
            "status": null
        }}
    ],
    "scene_state_data": {{}}
}}

SOURCE:

{source_text}
"""
            )
        ],
    )

    final_response = None

    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response():
            final_response = event

    if final_response is None:
        raise RuntimeError(
            "Source Transformer did not return a final response."
        )

    response_text = final_response.content.parts[0].text.strip()

    if response_text.startswith("```"):
        response_text = response_text.removeprefix(
            "```json"
        ).removeprefix(
            "```"
        ).removesuffix(
            "```"
        ).strip()

    return ExtractedFilmData.model_validate_json(
        response_text
    )