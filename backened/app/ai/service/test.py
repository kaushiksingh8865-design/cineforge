import asyncio
from pprint import pprint

from app.ai.database.database import SessionLocal
from app.ai.service.sourceservice import SourceService


async def main():

    async with SessionLocal() as db:

        fake_file = b"""
INT. ABANDONED LAB - NIGHT

Vance enters the laboratory.
The room is silent.
"""

        source = await SourceService.create_uploaded_source(
            db=db,
            project_id=1,
            filename="test_screenplay.txt",
            file_content=fake_file,
            mime_type="text/plain",
            file_metadata={
                "test": True,
                "origin": "upload",
            },
        )

        print("\n===== UPLOADED SOURCE =====")

        pprint({
            "id": source.id,
            "project_id": source.project_id,
            "name": source.name,
            "source_type": source.source_type,
            "mime_type": source.mime_type,
            "file_path": source.file_path,
            "content": source.content,
            "metadata": source.file_metadata,
        })

        print("===========================\n")


if __name__ == "__main__":
    asyncio.run(main())