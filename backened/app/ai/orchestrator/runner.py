import os

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.ai.core.settings import settings
from app.ai.orchestrator.workflow import story_visual_pipeline


os.environ.setdefault(
    "GEMINI_API_KEY",
    settings.gemini_api_key,
)


APP_NAME = "cineforge_orchestrator"
USER_ID = "test_user"


session_service = InMemorySessionService()

runner = Runner(
    app_name=APP_NAME,
    agent=story_visual_pipeline,
    session_service=session_service,
)


async def run_story_visual_pipeline(
    request: str,
    context: str = "",
):
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=f"""
User request:
{request}

Film context:
{context}

Execute the CineForge story-to-visual workflow.
"""
            )
        ],
    )

    events = []

    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=message,
    ):
        events.append(event)

    return events