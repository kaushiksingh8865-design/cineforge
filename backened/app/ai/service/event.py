from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.models.event import EventModel
from app.ai.models.proposal import ProposalModel
from app.ai.schemas.event import Event


class EventService:

    @staticmethod
    async def create_event(
        db: AsyncSession,
        proposal_id: str,
        event_type: str,
        description: str,
    ) -> EventModel | None:

        # Find proposal using its public proposal_id
        result = await db.execute(
            select(ProposalModel).where(
                ProposalModel.proposal_id == proposal_id
            )
        )

        proposal = result.scalar_one_or_none()

        if proposal is None:
            return None

        event = EventModel(
            proposal_id=proposal.id,
            event_id=str(uuid4()),
            event_type=event_type,
            description=description,
        )

        db.add(event)

        await db.commit()
        await db.refresh(event)

        return event

    @staticmethod
    async def get_event(
        db: AsyncSession,
        event_id: str,
    ) -> EventModel | None:

        result = await db.execute(
            select(EventModel).where(
                EventModel.event_id == event_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def list_events_for_proposal(
        db: AsyncSession,
        proposal_id: str,
    ) -> list[EventModel]:

        result = await db.execute(
            select(EventModel)
            .join(ProposalModel)
            .where(
                ProposalModel.proposal_id == proposal_id
            )
            .order_by(EventModel.timestamp.desc())
        )

        return result.scalars().all()