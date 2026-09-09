from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.models.source import SourceFile
from app.ai.schemas.source import SourceFileCreate
from app.ai.core.file_storage import FileStorage


class SourceService:

    @staticmethod
    async def create_source(
        db: AsyncSession,
        project_id: int,
        source_data: SourceFileCreate,
    ) -> SourceFile:

        source = SourceFile(
            project_id=project_id,
            name=source_data.name,
            source_type=source_data.source_type,
            mime_type=source_data.mime_type,
            file_path=source_data.file_path,
            content=source_data.content,
            file_metadata=source_data.file_metadata,
        )

        db.add(source)

        await db.commit()
        await db.refresh(source)

        return source

    @staticmethod
    async def get_source(
        db: AsyncSession,
        source_id: int,
    ) -> SourceFile | None:

        result = await db.execute(
            select(SourceFile).where(
                SourceFile.id == source_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_project_sources(
        db: AsyncSession,
        project_id: int,
    ) -> list[SourceFile]:

        result = await db.execute(
            select(SourceFile)
            .where(SourceFile.project_id == project_id)
            .order_by(SourceFile.created_at)
        )

        return result.scalars().all()

    @staticmethod
    async def delete_source(
        db: AsyncSession,
        source_id: int,
    ) -> bool:

        source = await SourceService.get_source(
            db,
            source_id,
        )

        if source is None:
            return False

        await db.delete(source)
        await db.commit()

        return True
    @staticmethod
    async def create_uploaded_source(
        db: AsyncSession,
        project_id: int,
        filename: str,
        file_content: bytes,
        mime_type: str | None = None,
        file_metadata: dict | None = None,
    ) -> SourceFile:

        storage = FileStorage()

        file_path = await storage.save(
            file_content=file_content,
            original_filename=filename,
        )

        source_data = SourceFileCreate(
            name=filename,
            source_type="uploaded_file",
            mime_type=mime_type,
            file_path=file_path,
            content=None,
            file_metadata=file_metadata or {},
        )

        return await SourceService.create_source(
            db=db,
            project_id=project_id,
            source_data=source_data,
        )