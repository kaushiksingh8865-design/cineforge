import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.ai.agents.research import research_agent
from app.ai.schemas.research import ResearchResult
from app.ai.core.settings import settings

import os

os.environ.setdefault("GEMINI_API_KEY", settings.gemini_api_key)


APP_NAME = "cineforge_research_test"
USER_ID = "test_user"

session_service = InMemorySessionService()

runner = Runner(
    app_name=APP_NAME,
    agent=research_agent,
    session_service=session_service,
)


async def main():
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text="""
Research this filmmaking question:

What are common visual characteristics of a film noir scene?
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
            "Research Agent did not return a final response."
        )

    result = ResearchResult.model_validate_json(
        final_response.content.parts[0].text
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())