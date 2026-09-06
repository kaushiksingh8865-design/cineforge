import asyncio

from app.ai.agents.continuity_runner import run_continuity_analysis
from app.ai.database.database import SessionLocal


async def main():
    project_id = 1
    scene_number = 1

    async with SessionLocal() as db:
        result = await run_continuity_analysis(
            db,
            project_id,
            scene_number,
        )

        print(result)


if __name__ == "__main__":
    asyncio.run(main())