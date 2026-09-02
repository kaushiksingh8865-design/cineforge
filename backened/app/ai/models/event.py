from sqlalchemy import ForeignKey , Column ,Text,String, DateTime
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column , relationship
from app.ai.database.database import Base
from sqlalchemy import func

if TYPE_CHECKING:
    from app.ai.models.proposal import ProposalModel

class EventModel(Base):
    __tablename__ = "events"

    id:Mapped[int] = mapped_column(
        primary_key = True,
    )
    proposal_id:Mapped[int] = mapped_column(
        ForeignKey("proposals.id", ondelete="CASCADE")

    )
    event_id:Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    event_type:Mapped[str] = mapped_column(
        Text,
        nullable= False
    )
    
    description:Mapped[str|None] = mapped_column(
        Text,
        nullable= True,
    )
    timestamp:Mapped[datetime]= mapped_column(
        DateTime(timezone= True),
        server_default = func.now(),
        nullable=False,
    )
    proposal:Mapped["ProposalModel"] = relationship(
        "ProposalModel",
        back_populates = "events"
    )