"""from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.ai.models.characters import Character
from app.ai.schemas.character import Character  as CharacterModel


class CharacterService:
    @staticmethod
    async def create_character(db:AsyncSession, project_id:int, character_data:Character,)-> CharacterModel:
        character= CharacterModel(project_id = project_id, name = character_data.name,)
        db.add(character)
        await db.flush()
        await db.refresh(character)


        return character

    @staticmethod
    async def get_character( db:AsyncSession, character_id:int)-> CharacterModel |None:
        result = await db.execute(select(CharacterModel).where(CharacterModel.id == character_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_character_by_name(db:AsyncSession , project_id:int , name:str,) -> CharacterModel |None:
        result = await db.execute(select(CharacterModel).where(CharacterModel.project_id==project_id, CharacterModel.name== name,))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_character(db:AsyncSession , charcater_id:int , character_data:Character,) -> CharacterModel|None:
        result = await db.execute(select(CharacterModel).where(CharacterModel.id == charcater_id ,))
        character = result.scalar_one_or_none()

        if character is None:
            return None

        character.name = character_data.name
        await db.commit()
        await db.refresh(character)

        return character

    @staticmethod
    async def delete_character(db:AsyncSession , character_id:int,) -> bool:
        result = await db.execute(select(CharacterModel).where(CharacterModel.id == character_id))
        character = result.scalar_one_or_none()

        if character is None :
            return None

        await db.delete(character)
        await db.commit()

        return True

    @staticmethod
    async def list_character(db:AsyncSession , project_id:int) -> list[CharacterModel]:
        result = await db.execute(select(CharacterModel).where(CharacterModel.project_id == project_id).order_by(select(CharacterModel.name)))
        return result.scalars().all()

    

    

         
    
    
    
    

    """


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.models.characters import Character as CharacterModel
from app.ai.schemas.character import Character as CharacterSchema


class CharacterService:

    @staticmethod
    async def create_character(
        db: AsyncSession,
        project_id: int,
        character_data: CharacterSchema,
        commit:bool =True,
    ) -> CharacterModel:

        character = CharacterModel(
            project_id=project_id,
            name=character_data.name,
        )

        db.add(character)

        if commit:
            await db.commit()
        else:
            await db.flush()
        await db.refresh(character)

        return character

    @staticmethod
    async def get_character(
        db: AsyncSession,
        character_id: int,
    ) -> CharacterModel | None:

        result = await db.execute(
            select(CharacterModel).where(
                CharacterModel.id == character_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_character_by_name(
        db: AsyncSession,
        project_id: int,
        name: str,
    ) -> CharacterModel | None:

        result = await db.execute(
            select(CharacterModel).where(
                CharacterModel.project_id == project_id,
                CharacterModel.name == name,
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update_character(
        db: AsyncSession,
        character_id: int,
        character_data: CharacterSchema,
    ) -> CharacterModel | None:

        result = await db.execute(
            select(CharacterModel).where(
                CharacterModel.id == character_id
            )
        )

        character = result.scalar_one_or_none()

        if character is None:
            return None

        character.name = character_data.name

        await db.commit()
        await db.refresh(character)

        return character

    @staticmethod
    async def delete_character(
        db: AsyncSession,
        character_id: int,
    ) -> bool:

        result = await db.execute(
            select(CharacterModel).where(
                CharacterModel.id == character_id
            )
        )

        character = result.scalar_one_or_none()

        if character is None:
            return False

        await db.delete(character)
        await db.commit()

        return True

    @staticmethod
    async def list_character(
        db: AsyncSession,
        project_id: int,
    ) -> list[CharacterModel]:

        result = await db.execute(
            select(CharacterModel)
            .where(
                CharacterModel.project_id == project_id
            )
            .order_by(
                CharacterModel.name
            )
        )

        return result.scalars().all()