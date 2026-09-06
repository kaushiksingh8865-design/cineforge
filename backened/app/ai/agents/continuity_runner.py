from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from app.ai.schemas.continuity import ContinuityAnalysis

from app.ai.agents.continuity import continuity_agent
from app.ai.core.settings import settings
import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.service.filmstartengine import FilmStateEngine
from app.ai.validation.validation_engine import ValidationEngine
os.environ.setdefault("GEMINI_API_KEY", settings.gemini_api_key)


APP_NAME = "cineforge"
USER_ID = "test_user"


session_service = InMemorySessionService()

runner = Runner(
    app_name=APP_NAME,
    agent=continuity_agent,
    session_service=session_service,
)


async def run_continuity_agent(context: dict):
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=f"""
Analyze the following CineForge continuity context.

Continuity context:
{context}
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

    return ContinuityAnalysis.model_validate_json(
        final_response.content.parts[0].text
    )


async def run_continuity_analysis(
    db: AsyncSession,
    project_id: int,
    scene_number: int,
):
    context = await FilmStateEngine.get_continuity_context(
        db,
        project_id,
        scene_number,
    )

    if context is None:
        return None

    return await run_continuity_agent(context)

async def run_continuity_analysis(
    db: AsyncSession,
    project_id: int,
    scene_number: int,
):
    context = await FilmStateEngine.get_continuity_context(
        db,
        project_id,
        scene_number,
    )

    if context is None:
        return None

    validation = ValidationEngine.validate_state_transition(
        context
    )

    context["validation"] = validation

    return await run_continuity_agent(context)