from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.ai.models.proposal import ProposalModel
from app.ai.schemas.proposal import Proposal


class ProposalStatus:
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ProposalService:

    @staticmethod
    async def create_proposal(
        db: AsyncSession,
        project_id: int,
        scene_id: int | None,
        proposal_data: Proposal,
    ) -> ProposalModel:

        proposal = ProposalModel(
            proposal_id=str(uuid4()),
            project_id=project_id,
            scene_id=scene_id,
            description=proposal_data.description,
            reason=proposal_data.reason,
            status=ProposalStatus.PENDING,
            change_data = proposal_data.change.model_dump(),
        )

        db.add(proposal)

        await db.commit()
        await db.refresh(proposal)

        return proposal

    @staticmethod
    async def get_proposal(
        db: AsyncSession,
        proposal_id: str,
    ) -> ProposalModel | None:

        result = await db.execute(
            select(ProposalModel).where(
                ProposalModel.proposal_id == proposal_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def list_proposals(
        db: AsyncSession,
        project_id: int,
    ) -> list[ProposalModel]:

        result = await db.execute(
            select(ProposalModel)
            .where(
                ProposalModel.project_id == project_id
            )
            .order_by(ProposalModel.created_at.desc())
        )

        return result.scalars().all()

    @staticmethod
    async def approve_proposal(
        db: AsyncSession,
        proposal_id: str,
    ) -> ProposalModel | None:

        result = await db.execute(
            select(ProposalModel).where(
                ProposalModel.proposal_id == proposal_id
            )
        )

        proposal = result.scalar_one_or_none()

        if proposal is None:
            return None

        if proposal.status != ProposalStatus.PENDING:
            return proposal

        proposal.status = ProposalStatus.APPROVED

        await db.commit()
        await db.refresh(proposal)

        return proposal

    @staticmethod
    async def reject_proposal(
        db: AsyncSession,
        proposal_id: str,
    ) -> ProposalModel | None:

        result = await db.execute(
            select(ProposalModel).where(
                ProposalModel.proposal_id == proposal_id
            )
        )

        proposal = result.scalar_one_or_none()

        if proposal is None:
            return None

        if proposal.status != ProposalStatus.PENDING:
            return proposal

        proposal.status = ProposalStatus.REJECTED

        await db.commit()
        await db.refresh(proposal)

        return proposal
