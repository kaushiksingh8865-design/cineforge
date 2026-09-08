import os
from pprint import pprint

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.core.settings import settings
from app.ai.orchestrator.workflow import story_visual_pipeline
from app.ai.service.filmstartengine import FilmStateEngine
from app.ai.orchestrator.film_context import build_film_context
from app.ai.schemas.workflow import CineForgeRequest
from app.ai.agents.research_runner import run_research_agent
from app.ai.agents.continuity_runner import run_continuity_analysis


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
    db: AsyncSession,
    request: CineForgeRequest,
    research_question:str| None = None,
):
    continuity_context = await FilmStateEngine.get_continuity_context(
        db,
        request.project_id,
        request.scene_number,
    )

    if continuity_context is None:
        return None

    context = build_film_context(
        continuity_context
    )
    
        
    print("\n===== FILM CONTEXT =====")
    pprint(context)
    print("========================\n")

    continuity_result = await run_continuity_analysis(
        db,
        request.project_id,
        request.scene_number,

    )

    print("\n=== CONTINUITY RESULT=====")
    print(
        continuity_result.model_dump()
        if continuity_result
        else None
    )

    print("++++++++++++++++++\n")





    research_result = None 
    if research_question:
        research_result = await run_research_agent(
            research_question
        )
        print("\n==== RESEARCH RESSULT ====")
        pprint(research_result.model_dump())
        print("=======================\n")

    

   
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text =f"""
User request:
{request.request}

Film context:
{context}

Continuity analysis:
{
    continuity_result.model_dump()
    if continuity_result
    else None
}

Research result:
{
    research_result.model_dump()
    if research_result
    else None
}

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