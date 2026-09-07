from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.models.proposal import ProposalModel
from app.ai.schemas.proposal import StateChange

from app.ai.service.stateservice import StateService


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
