from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.models.proposal import ProposalModel
from app.ai.schemas.proposal import StateChange

from app.ai.service.stateservice import StateService
from app.ai.service.scene_service import SceneService
from app.ai.schemas.save import SaveRequest


class StateUpdateError(Exception):
    pass


class StateUpdateService:

    @staticmethod
    async def apply_proposal(
        db: AsyncSession,
        proposal_id: str,
    ):

        result = await db.execute(
            select(ProposalModel).where(
                ProposalModel.proposal_id == proposal_id
            )
        )

        proposal = result.scalar_one_or_none()

        if proposal is None:
            raise StateUpdateError(
                "Proposal not found."
            )

        if proposal.status != "approved":
            raise StateUpdateError(
                "Only approved proposals can update Film State."
            )

        change = StateChange.model_validate(
            proposal.change_data
        )

        if change.target_type == "character":
            return await StateUpdateService._apply_character_change(
                db,
                change,
            )

        if change.target_type == "prop":
            return await StateUpdateService._apply_prop_change(
                db,
                change,
            )

        if change.target_type == "scene":
            return await StateUpdateService._apply_scene_change(
                db,
                change,
            )

        raise StateUpdateError(
            f"Unsupported target type: {change.target_type}"
        )

    @staticmethod
    async def apply_save(
        db: AsyncSession,
        changes: list[StateChange],
    ):
        try:
            results = []

            for change in changes:

                if change.target_type == "character":
                    result = await StateUpdateService._apply_character_change(
                        db,
                        change,
                    )

                elif change.target_type == "prop":
                    result = await StateUpdateService._apply_prop_change(
                        db,
                        change,
                    )

                elif change.target_type == "scene":
                    result = await StateUpdateService._apply_scene_change(
                        db,
                        change,
                    )

                else:
                    raise StateUpdateError(
                        f"Unsupported target type: {change.target_type}"
                    )

                results.append(result)

            await db.commit()

            return results

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def _apply_character_change(
        db: AsyncSession,
        change: StateChange,
    ):
        state = await StateService.get_character_state(
            db=db,
            character_id=change.target_id,
            scene_id=change.scene_id,
        )

        if state is None:
            raise StateUpdateError(
                "Character state not found."
            )

        allowed_fields = {
            "status",
            "injuries",
            "wardrobe",
        }

        if change.field not in allowed_fields:
            raise StateUpdateError(
                f"Invalid character state field: {change.field}"
            )

        current_value = getattr(state, change.field)

        if current_value != change.old_value:
            raise StateUpdateError(
                f"Character state changed since this save was created. "
                f"Expected {change.old_value!r}, "
                f"but current value is {current_value!r}."
            )

        setattr(
            state,
            change.field,
            change.new_value,
        )

        await db.flush()

        return state
    @staticmethod
    async def _apply_prop_change(
        db: AsyncSession,
        change: StateChange,
    ):
        state = await StateService.get_prop_state(
            db=db,
            prop_id=change.target_id,
            scene_id=change.scene_id,
        )

        if state is None:
            raise StateUpdateError(
                "Prop state not found."
            )

        allowed_fields = {
            "holder",
            "location",
            "status",
        }

        if change.field not in allowed_fields:
            raise StateUpdateError(
                f"Invalid prop state field: {change.field}"
            )

        current_value = getattr(state, change.field)

        if current_value != change.old_value:
            raise StateUpdateError(
                f"Prop state changed since this save was created. "
                f"Expected {change.old_value!r}, "
                f"but current value is {current_value!r}."
            )

        setattr(
            state,
            change.field,
            change.new_value,
        )

        await db.flush()

        return state


    @staticmethod
    async def _apply_scene_change(
        db: AsyncSession,
        change: StateChange,
    ):
        scene = await SceneService.get_scene(
            db=db,
            scene_id=change.target_id,
        )

        if scene is None:
            raise StateUpdateError(
                "Scene not found."
            )

        if scene.id != change.scene_id:
            raise StateUpdateError(
                "Scene ID mismatch."
            )

        allowed_fields = {
            "scene_number",
            "header",
            "location",
            "time_of_day",
            "visual_prompt",
        }

        if change.field not in allowed_fields:
            raise StateUpdateError(
                f"Invalid scene field: {change.field}"
            )

        current_value = getattr(scene, change.field)

        if current_value != change.old_value:
            raise StateUpdateError(
                f"Scene changed since this save was created. "
                f"Expected {change.old_value!r}, "
                f"but current value is {current_value!r}."
            )

        setattr(
            scene,
            change.field,
            change.new_value,
        )

        await db.flush()

        return scene

    @staticmethod
    async def apply_save_request(
        db: AsyncSession,
        save_request: SaveRequest,
    ):
        if not save_request.state_changes:
            return []

        for change in save_request.state_changes:

            if change.scene_id != save_request.scene_id:
                raise StateUpdateError(
                    "State change scene does not match save request scene."
                )

        return await StateUpdateService.apply_save(
            db=db,
            changes=save_request.state_changes,
        )

    
