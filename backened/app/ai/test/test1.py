import asyncio

from app.ai.database.database import SessionLocal
from app.ai.schemas.characterstate import CharacterState
from app.ai.service.stateservice import StateService


async def main():
    async with SessionLocal() as db:

        state_data = CharacterState(
            character_id=1,
            scene_id=1,
            status="injured",
            injuries=["bullet wound"],
            wardrobe=["black coat"],
        )

        exists = await StateService.character_state_exist(
            db,
            character_id=state_data.character_id,
            scene_id=state_data.scene_id,
        )

        if exists:
            state = await StateService.update_character_state(
                db,
                character_id=state_data.character_id,
                scene_id=state_data.scene_id,
                state_data=state_data,
            )
            print("UPDATED")
        else:
            state = await StateService.create_character_state(
                db,
                character_id=state_data.character_id,
                scene_id=state_data.scene_id,
                state_data=state_data,
            )
            print("CREATED")

        print("Character ID:", state.character_id)
        print("Scene ID:", state.scene_id)
        print("Status:", state.status)
        print("Injuries:", state.injuries)
        print("Wardrobe:", state.wardrobe)


if __name__ == "__main__":
    asyncio.run(main())