import asyncio
import os

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.ai.agents.story import story_agent
from app.ai.core.settings import settings
from app.ai.schemas.story import StoryResult


os.environ.setdefault("GEMINI_API_KEY", settings.gemini_api_key)


APP_NAME = "cineforge_story"
USER_ID = "test_user"


session_service = InMemorySessionService()

runner = Runner(
    app_name=APP_NAME,
    agent=story_agent,
    session_service=session_service,
)


async def run_story_agent(
    story_request: str,
    story_context: str = "",
    research_context: str = "",
) -> StoryResult:

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=f"""
Story request:
{story_request}

Story context:
{story_context}

Research material:
{research_context}

Develop the requested story content using the supplied
context and return the required structured StoryResult.
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
            "Story Agent did not return a final response."
        )

    return StoryResult.model_validate_json(
        final_response.content.parts[0].text
    )