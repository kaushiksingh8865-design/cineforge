#test transformer
import asyncio
from pprint import pprint

from app.ai.database.database import SessionLocal
from app.ai.service.sourceservice import SourceService
from app.ai.etl.extractor import SourceExtractor
from app.ai.etl.transformer import transform_source


async def main():

    async with SessionLocal() as db:

        # Get sources already saved for project 1
        sources = await SourceService.get_project_sources(
            db,
            project_id=1,
        )

        if not sources:
            print("No sources found.")
            return

        # Test the most recent source
        source = sources[-1]

        print("\n===== SOURCE =====")
        print("ID:", source.id)
        print("Name:", source.name)
        print("Type:", source.source_type)

        # Extract original text
        source_text = await SourceExtractor.extract(
            source
        )

        print("\n===== RAW SOURCE =====")
        print(source_text)

        # Transform source into structured data
        result = await transform_source(
            source_text
        )

        print("\n===== TRANSFORMED RESULT =====")

        pprint(
            result.model_dump(),
            sort_dicts=False,
        )

        print("===============================\n")


if __name__ == "__main__":
    asyncio.run(main())