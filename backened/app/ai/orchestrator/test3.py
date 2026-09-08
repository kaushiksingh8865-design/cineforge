import asyncio

from app.ai.database.database import SessionLocal
from app.ai.orchestrator.runner import run_story_visual_pipeline
from app.ai.schemas.workflow import CineForgeRequest 
from app.ai.service.filmstartengine import FilmStateEngine
from app.ai.orchestrator.film_context import build_film_context

async def main():
    async with SessionLocal() as db:

        cineforge_request = CineForgeRequest(
            db=db,
            project_id = 1,
            scene_number = 1,
            request = (
                "Continue the current scene while maintaining "
                "character, prop, and location continuity. "
                "Then create the visual direction for the scene."

            )
           
            
        )
        events = await run_story_visual_pipeline(
            db=db,
            request=cineforge_request,
            research_question=(
                "What are realistic ways to portray "
                "a police investigation in a modern crime thriller?"
            ),
        )
       

        if events is None:
            print("No scene/context found.")
            return

        print("=" * 80)
        print("DB → FILM STATE → ADK WORKFLOW TEST")
        print("=" * 80)

        for index, event in enumerate(events, start=1):
            print(f"\nEVENT {index}")
            print("-" * 80)

            print("AUTHOR:", event.author)

            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print("TEXT:")
                        print(part.text)


if __name__ == "__main__":
    asyncio.run(main())