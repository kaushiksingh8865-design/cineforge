from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas.scene import Scene
from app.ai.models.scene1 import Scene as SceneModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class SceneService:

    @staticmethod
    async def create_scene(db:AsyncSession , project_id: int, scene_data: Scene,) -> SceneModel:
        scene = SceneModel(
            project_id= project_id,
            scene_number=scene_data.scene_number,
            header=scene_data.header,
            location=scene_data.location,
            time_of_day= scene_data.time_of_day,
            visual_prompt=scene_data.visual_prompt,
        )
        db.add(scene)
        await db.commit()
        await db.refresh(scene)

        return scene

    @staticmethod
    async def get_scene(db: AsyncSession, scene_id:int , ) -> SceneModel | None:
        result = await db.execute(select(SceneModel).where(SceneModel.id == scene_id))

        return result.scalar_one_or_none()


    @staticmethod
    async def get_scene_by_number(db:AsyncSession, project_id:int, scene_number:int,) -> SceneModel|None:
        result = await db.execute(
            select(SceneModel).where(SceneModel.project_id == project_id, SceneModel.scene_number == scene_number)

        )
        return result.scalar_one_or_none()
    @staticmethod
    async def update_scene(db: AsyncSession , scene_id:int , scene_data:Scene,) -> SceneModel|None:
        result = await db.execute(select(SceneModel).where(SceneModel.id == scene_id))

        scene = result.scalar_one_or_none()

        if scene is None:
            return None

        scene.scene_number = scene_data.scene_number
        scene.header = scene_data.header
        scene.location =scene_data.location
        scene.time_of_day = scene_data.time_of_day
        scene.visual_prompt = scene_data.visual_prompt

        await db.commit()
        await db.refresh(scene)

        return scene
    @staticmethod
    async def delete_scene( db: AsyncSession , scene_id:int,)-> bool:
        result = await db.execute(select (SceneModel).where(SceneModel.id == scene_id))
        scene = result.scalar_one_or_none()

        if scene is None:
            return False
        await db.delete(scene)
        await db.commit()

        return True


    @staticmethod
    async def list_scenes( db:AsyncSession , project_id:int,) -> list[SceneModel]:
        result = await db.execute(select(SceneModel).where(SceneModel.project_id==project_id).order_by(SceneModel.scene_number) )
        return result.scalars().all()

    @staticmethod
    async def get_scene_with_relationships( db: AsyncSession , scene_id:int,) -> SceneModel | None:
        result = await db.execute( select(SceneModel).options(
        selectinload(SceneModel.characters),
        selectinload(SceneModel.props),
        selectinload(SceneModel.state),
        selectinload(SceneModel.character_states),
        selectinload(SceneModel.prop_states),
        ).where(SceneModel.id == scene_id)
        )
        return result.scalar_one_or_none()


    @staticmethod
    async def scene_exists(db :AsyncSession , project_id: int , scene_number:int,) -> bool:
        result = await db.execute( select(SceneModel.id).where(SceneModel.project_id == project_id, SceneModel.scene_number==scene_number,))
        return result.scalar_one_or_none() is not None
    
    @staticmethod
    async def get_scene_state_context( db:AsyncSession , scene_id:int,) -> SceneModel |None:
        result = await db.execute(select(SceneModel).options(
            selectinload(SceneModel.state),
            selectinload(SceneModel.character_states),
            selectinload(SceneModel.prop_states),
        ).where(SceneModel.id == scene_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_previous_scene(db:AsyncSession , project_id:int, scene_number: int,) ->SceneModel | None:
        result = await db.execute(select(SceneModel).where(SceneModel.project_id == project_id, SceneModel.scene_number == scene_number - 1))
        return result.scalar_one_or_none()
    @staticmethod
    async def get_next_scene(db:AsyncSession, project_id:int , scene_number: int,) -> SceneModel |None:
        result = await db.execute(select(SceneModel).where(SceneModel.project_id == project_id, SceneModel.scene_number == scene_number + 1))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_scene_range(db:AsyncSession , project_id:int , start_scene:int , end_scene:int,) -> list[SceneModel]:
        result = await db.execute(select(SceneModel).where(SceneModel.project_id == project_id, SceneModel.scene_number >= start_scene, SceneModel.scene_number <= end_scene).order_by(SceneModel.scene_number))
        return result.scalars().all()
