import os

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.ai.agents.visual import visual_agent
from app.ai.core.settings import settings
from app.ai.schemas.visual import VisualResult


os.environ.setdefault("GEMINI_API_KEY", settings.gemini_api_key)


APP_NAME = "cineforge_visual"
USER_ID = "test_user"


session_service = InMemorySessionService()

runner = Runner(
    app_name=APP_NAME,
    agent=visual_agent,
    session_service=session_service,
)


async def run_visual_agent(
    visual_request: str,
    story_context: str = "",
    film_context: str = "",
    research_context: str = "",
) -> VisualResult:

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=f"""
Visual request:
{visual_request}

Film context:
{film_context}

Story context:
{story_context}

Research material:
{research_context}

Translate the supplied story material into
cinematic visual direction and return the required
structured VisualResult.
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
            "Visual Agent did not return a final response."
        )

    return VisualResult.model_validate_json(
        final_response.content.parts[0].text
    )