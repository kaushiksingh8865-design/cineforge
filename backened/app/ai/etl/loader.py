from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.etl.transformer import ExtractedFilmData
from app.ai.schemas.scene import Scene
from app.ai.schemas.character import Character
from app.ai.schemas.property import Prop
from app.ai.schemas.scenestate import SceneState
from app.ai.schemas.characterstate import CharacterState
from app.ai.schemas.propstate import PropState

from app.ai.service.scene_service import SceneService
from app.ai.service.characterservice import CharacterService
from app.ai.service.prop_service import PropService
from app.ai.service.stateservice import StateService


class FilmDataLoader:

    @staticmethod
    async def load_scene(
        db: AsyncSession,
        project_id: int,
        film_data: ExtractedFilmData,
    ):

        scene_data = film_data.scene

        existing_scene = await SceneService.get_scene_by_number(
            db,
            project_id,
            scene_data.scene_number,
        )

        if existing_scene is not None:
            return existing_scene

        scene = await SceneService.create_scene(
            db,
            project_id,
            scene_data,
        )

        return scene

    @staticmethod
    async def load_characters(
        db: AsyncSession,
        project_id: int,
        scene,
        film_data: ExtractedFilmData,
    ):

        loaded_characters = []

        for extracted_character in film_data.characters:

            character = await CharacterService.get_character_by_name(
                db,
                project_id,
                extracted_character.name,
            )

            if character is None:

                character_data = Character(
                    name=extracted_character.name,
                )

                character = await CharacterService.create_character(
                    db,
                    project_id,
                    character_data,
                )

            if character not in scene.characters:
                scene.characters.append(character)

            loaded_characters.append(
                (
                    character,
                    extracted_character,
                )
            )

        await db.commit()

        return loaded_characters

    @staticmethod
    async def load_character_states(
        db: AsyncSession,
        scene,
        loaded_characters,
    ):

        for character, extracted_character in loaded_characters:

            state_data = CharacterState(
                character_id=character.id,
                scene_id=scene.id,
                status=extracted_character.status,
                injuries=extracted_character.injuries,
                wardrobe=extracted_character.wardrobe,
            )

            existing_state = await StateService.get_character_state(
                db,
                character.id,
                scene.id,
            )

            if existing_state is None:

                await StateService.create_character_state(
                    db,
                    character.id,
                    scene.id,
                    state_data,
                )

            else:

                await StateService.update_character_state(
                    db,
                    character.id,
                    scene.id,
                    state_data,
                )

    @staticmethod
    async def load_props(
        db: AsyncSession,
        project_id: int,
        scene,
        film_data: ExtractedFilmData,
    ):

        loaded_props = []

        for extracted_prop in film_data.props:

            prop = await PropService.get_prop_by_name(
                db,
                project_id,
                extracted_prop.name,
            )

            if prop is None:

                prop_data = Prop(
                    name=extracted_prop.name,
                    description=extracted_prop.description,
                )

                prop = await PropService.create_prop(
                    db,
                    project_id,
                    prop_data,
                )

            if prop not in scene.props:
                scene.props.append(prop)

            loaded_props.append(
                (
                    prop,
                    extracted_prop,
                )
            )

        await db.commit()

        return loaded_props

    @staticmethod
    async def load_prop_states(
        db: AsyncSession,
        scene,
        loaded_props,
    ):

        for prop, extracted_prop in loaded_props:

            state_data = PropState(
                name=extracted_prop.name,
                holder=extracted_prop.holder,
                location=extracted_prop.location,
                status=extracted_prop.status,
            )

            existing_state = await StateService.get_prop_state(
                db,
                prop.id,
                scene.id,
            )

            if existing_state is None:

                await StateService.create_prop_state(
                    db,
                    prop.id,
                    scene.id,
                    state_data,
                )

            else:

                await StateService.update_prop_state(
                    db,
                    prop.id,
                    scene.id,
                    state_data,
                )

    @staticmethod
    async def load_scene_state(
        db: AsyncSession,
        scene,
        film_data: ExtractedFilmData,
    ):

        state_data = SceneState(
            scene_id=scene.id,
            state_data=film_data.scene_state_data,
        )

        existing_state = await StateService.get_scene_state(
            db,
            scene.id,
        )

        if existing_state is None:

            await StateService.create_scene_state(
                db,
                scene.id,
                state_data,
            )

        else:

            await StateService.update_scene_state(
                db,
                scene.id,
                state_data,
            )

    @staticmethod
    async def load(
        db: AsyncSession,
        project_id: int,
        film_data: ExtractedFilmData,
    ):

        scene = await FilmDataLoader.load_scene(
            db,
            project_id,
            film_data,
        )

        loaded_characters = await FilmDataLoader.load_characters(
            db,
            project_id,
            scene,
            film_data,
        )

        await FilmDataLoader.load_character_states(
            db,
            scene,
            loaded_characters,
        )

        loaded_props = await FilmDataLoader.load_props(
            db,
            project_id,
            scene,
            film_data,
        )

        await FilmDataLoader.load_prop_states(
            db,
            scene,
            loaded_props,
        )

        await FilmDataLoader.load_scene_state(
            db,
            scene,
            film_data,
        )

        await db.commit()

        return scene