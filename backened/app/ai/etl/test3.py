import asyncio
from pprint import pprint

from app.ai.database.database import SessionLocal
from app.ai.service.sourceservice import SourceService
from app.ai.etl.extractor import SourceExtractor
from app.ai.etl.transformer import transform_source
from app.ai.etl.loader import FilmDataLoader


async def main():

    async with SessionLocal() as db:

        # 1. Get an existing source
        sources = await SourceService.get_project_sources(
            db,
            project_id=1,
        )

        if not sources:
            print("No sources found.")
            return

        source = sources[-1]

        print("\n===== SOURCE =====")
        pprint({
            "id": source.id,
            "name": source.name,
            "type": source.source_type,
        })

        # 2. Extract
        source_text = await SourceExtractor.extract(
            source
        )

        print("\n===== EXTRACTED TEXT =====")
        print(source_text)

        # 3. Transform
        film_data = await transform_source(
            source_text
        )

        print("\n===== TRANSFORMED DATA =====")
        pprint(
            film_data.model_dump(),
            sort_dicts=False,
        )

        # 4. Load into PostgreSQL
        scene = await FilmDataLoader.load(
            db=db,
            project_id=1,
            film_data=film_data,
        )

        print("\n===== LOADED SCENE =====")
        pprint({
            "id": scene.id,
            "scene_number": scene.scene_number,
            "header": scene.header,
            "location": scene.location,
            "time_of_day": scene.time_of_day,
        })

        # 5. Reload relationships
        loaded_source = await SourceService.get_source(
            db,
            source.id,
        )

        print("\n===== ETL COMPLETE =====")
        print("Source preserved:", loaded_source is not None)
        print("Scene ID:", scene.id)
        print("========================\n")


if __name__ == "__main__":
    asyncio.run(main())