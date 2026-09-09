from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.ai.models.property import Prop as PropModel
from app.ai.schemas.property import Prop


class PropService:

    @staticmethod
    async def create_prop(db:AsyncSession ,project_id:int , prop_data:Prop,commit: bool =True)-> PropModel:
        prop = PropModel(project_id=project_id, name = prop_data.name , description = prop_data.description,)
        db.add(prop)

        if commit:
            await db.commit()
        else:
            await db.flush()
        await db.refresh(prop)

        return prop

    @staticmethod
    async def get_prop(db:AsyncSession ,prop_id: int,  )-> PropModel |None:
        result = await db.execute(select(PropModel).where(PropModel.id == prop_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_prop_by_name(db:AsyncSession, project_id:int , name:str,)-> PropModel|None:
        result = await db.execute(select(PropModel).where(PropModel.project_id == project_id , PropModel.name ==name))
        return result.scalar_one_or_none()
    @staticmethod
    async def updata_prop(db:AsyncSession , prop_id:int , prop_data:Prop,)-> PropModel|None:
        result = await db.execute(select(PropModel).where(PropModel.id == prop_id,))
        prop = result.scalar_one_or_none()

        if prop is None:
            return None

        prop.name = prop_data.name
        prop.description = prop_data.description

        await db.commit()
        await db.refresh(prop)

        return prop 

    @staticmethod
    async def delete_prop(db:AsyncSession , prop_id:int,)-> bool:
        result = await db.execute(select(PropModel).where(PropModel.id==prop_id))
        prop = result.scalar_one_or_none()

        if prop is None:
            return False
        await db.delete(prop)
        await db.commit()

        return 

    @staticmethod
    async def list_props(db:AsyncSession, project_id:int ,) -> list[PropModel]:
        result = await db.execute(select(PropModel).where(PropModel.project_id == project_id).order_by(PropModel.name))
        return result.scalars().all()

    @staticmethod
    async def prop_exist(db:AsyncSession , project_id:int,name:str)-> bool:
        result = await db.execute(select(PropModel).where(PropModel.project_id == project_id, PropModel.name == name))

        return result.scalar_one_or_none() is not None

    

    
    