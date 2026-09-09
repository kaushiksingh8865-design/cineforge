import asyncio

from app.ai.database.database import SessionLocal
from app.ai.service.sourceservice import SourceService
from app.ai.etl.extractor import SourceExtractor


async def main():

    async with SessionLocal() as db:

        sources = await SourceService.get_project_sources(
            db,
            project_id=1,
        )

        for source in sources:

            print("\n===== SOURCE =====")
            print("ID:", source.id)
            print("Name:", source.name)
            print("Type:", source.source_type)

            text = await SourceExtractor.extract(source)

            print("\n===== EXTRACTED TEXT =====")
            print(text)
            print("===========================\n")


if __name__ == "__main__":
    asyncio.run(main())