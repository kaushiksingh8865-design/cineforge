from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.ai.models.characterstate import CharacterState as model
from app.ai.schemas.characterstate import CharacterState
from app.ai.models.propstate import PropState as modelp
from app.ai.schemas.propstate import PropState

from app.ai.models.scenestate import SceneState as models
from app.ai.schemas.scenestate import SceneState
class StateService:
    @staticmethod
    async def get_character_states_for_scene(db:AsyncSession, scene_id:int,)-> list[model]:

        result = await db.execute(select(model).options(selectinload(model.character)).where(model.scene_id == scene_id))
        return result.scalars().all()

    @staticmethod
    async def get_character_state(db:AsyncSession ,character_id:int , scene_id:int , )-> model|None:
        result = await db.execute(select(model).options(selectinload(model.character)).where(model.character_id == character_id, model.scene_id==scene_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_character_state(db:AsyncSession , character_id:int, scene_id:int, state_data:CharacterState, commit:bool =True) -> model:
        state = model(character_id=character_id,
                      scene_id = scene_id,
                      status= state_data.status,
                      injuries=state_data.injuries,
                      wardrobe = state_data.wardrobe,)
        db.add(state)
        if commit:
            await db.commit()
        else:
            await db.flush()
        await db.refresh(state)
      
        return state

    @staticmethod
    async def character_state_exist(db:AsyncSession , character_id: int , scene_id: int,) -> bool:
        result = await db.execute(select(model).where(model.character_id==character_id , model.scene_id ==scene_id))
        return result.scalar_one_or_none() is not None
    @staticmethod
    async def update_character_state(db:AsyncSession , character_id: int , scene_id:int , state_data: CharacterState,)-> model |None:
        result = await db.execute(select(model).where(model.character_id ==character_id, model.scene_id ==scene_id))
        state = result.scalar_one_or_none()

        if state is None:
            return None

        state.status = state_data.status
        state.injuries= state_data.injuries
        state.wardrobe=state_data.wardrobe

        await db.flush()
        await db.refresh(state)

        return state

    @staticmethod
    async def delete_character_state(db:AsyncSession , character_id:int, scene_id:int) -> bool:
        result = await db.execute(select(model).where(model.character_id ==character_id , model.scene_id==scene_id))
        state = result.scalar_one_or_none()

        if state is None:
            return False

        await db.delete(state)
        await db.commit()

        return True






    #propstate service

    @staticmethod
    async def get_prop_state(db:AsyncSession , prop_id: int , scene_id:int, )-> modelp|None:
        result = await db.execute(select(modelp).options(selectinload(modelp.prop)).where(modelp.prop_id == prop_id , modelp.scene_id == scene_id,))
        return result.scalar_one_or_none()


    @staticmethod
    async def create_prop_state(db:AsyncSession , prop_id:int , scene_id:int , state_data:PropState,commit: bool = True,) -> modelp:
        state = modelp(
            prop_id = prop_id,
            scene_id = scene_id,
            holder = state_data.holder,
            location = state_data.location ,
            status= state_data.status,
        )
        db.add(state)

        if commit:
            await db.commit()
        else:
            await db.flush()
                           
        await db.refresh(state)
        

        return state
    @staticmethod
    async def prop_exist(db:AsyncSession , prop_id:int , scene_id:int,) -> bool:
        result = await db.execute(select(modelp).where(modelp.prop_id == prop_id,modelp.scene_id==scene_id))

        return result.scalar_one_or_none() is not None

    @staticmethod
    async def update_prop_state(db:AsyncSession, prop_id:int , scene_id:int,state_data:PropState) ->modelp|None:
        result = await db.execute(select(modelp).where(modelp.prop_id ==prop_id, modelp.scene_id ==scene_id,))
        state = result.scalar_one_or_none()
        if state is None:
            return None

        state.holder = state_data.holder
        state.location = state_data.location
        state.status = state_data.status

        await db.flush()
        await db.refresh(state)

        return state


    @staticmethod
    async def delete_prop_state(db:AsyncSession,prop_id :int , scene_id:int,) ->bool:
        result = await db.execute(select(modelp).where(modelp.prop_id ==prop_id , modelp.scene_id==scene_id,))
        state = result.scalar_one_or_none()

        if state is None:
            return False

        await db.delete(state)
        await db.commit()
        return True



    #scenestate 


    @staticmethod
    async def get_scene_state(db:AsyncSession, scene_id:int, ) ->models |None:
        result =await db.execute(select(models).where(models.scene_id == scene_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_scene_state(db:AsyncSession , scene_id:int, state_data:SceneState,commit:bool = True,)-> models:
        state = models(
            scene_id=scene_id,
            state_data=state_data.state_data
        )

        db.add(state)
        if commit:
            await db.commit()
        else:
            await db.flush()
        await db.refresh(state)
        return state

    @staticmethod   
    async def scene_state_exist(db:AsyncSession , scene_id:int,)->bool:
        result = await db.execute(select(models).where(models.scene_id ==scene_id))
        return result.scalar_one_or_none() is not None


    @staticmethod
    async def update_scene_state(db:AsyncSession, scene_id:int , state_data:SceneState)-> models |None:
        result = await  db.execute(select(models).where(models.scene_id==scene_id))

        state = result.scalar_one_or_none()

        if state is None:
            return None

        state.state_data = state_data.state_data

        await db.flush()
        await db.refresh(state)

        return state


    @staticmethod
    async def delete_scene_state(db:AsyncSession , scene_id:int , )->bool:
        result = await db.execute(select(models).where(models.scene_id==scene_id))

        state =result.scalar_one_or_none()

        if state is None:
            return False

        await db.delete(state)
        await db.commit()
        return True