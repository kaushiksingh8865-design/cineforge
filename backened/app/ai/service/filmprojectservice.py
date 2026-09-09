from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.ai.models.film_project import FilmProject as model
from app.ai.schemas.film_project import FilmProject

class FilmService:

    @staticmethod
    async def create_project(db:AsyncSession, project_data:FilmProject,) -> model:
        project = model(title = project_data.title , logline= project_data.logline,)

        db.add(project)
        await db.commit()
        await db.refresh(project)

        return project




    @staticmethod
    async def get_project(db:AsyncSession , project_id:int,)-> model| None:
        result = await db.execute((select(model).where(model.id == project_id)))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_project(db:AsyncSession , project_id:int , project_data: FilmProject,) -> model| None:
        result = await db.execute(select(model).where(model.id == project_id ))

        project = result.scalar_one_or_none()

        if project is None:
            return None

        project.title =project_data.title
        project.logline =project_data.logline

        await db.commit()
        await db.refresh(project)

        return project

    @staticmethod
    async def delete_project(db:AsyncSession , project_id: int)-> bool:
        result = await db.execute(select(model).where(model.id == project_id))
        project = result.scalar_one_or_none()

        if project is None:
            return None

        await db.delete(project)
        await db.commit()

        return True
    @staticmethod
    async def list_project(db:AsyncSession,) -> list[model]:
        result = await db.execute(select(model).order_by(model.created_at))
        return  result.scalars().all()

    @staticmethod
    async def project_exist(db:AsyncSession ,project_id:int)->bool:
        result = await db.execute(select(model).where(model.id == project_id))
        return result.scalar_one_or_none() is not None