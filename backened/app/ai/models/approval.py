from sqlalchemy import ForeignKey , Text , String 
from sqlalchemy.orm import Mapped , mapped_column , relationship 
from app.ai.database.database import Base
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import DateTime , func
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from app.ai.models.proposal import ProposalModel

class ApprovalModel(Base):
    __tablename__= "approvals"

    id:Mapped[int] = mapped_column(
        primary_key=True,
    )
    proposal_id:Mapped[int] = mapped_column(
        ForeignKey("proposals.id",ondelete="CASCADE"),
        nullable= False,
        
    )
    approved:Mapped[bool] = mapped_column(
        nullable=False,
    )
    reviewer:Mapped[str|None]= mapped_column(
        Text,
        nullable=True,
    )
    comment:Mapped[str|None] = mapped_column(
        Text,
        nullable=True,
    )
    timestamp:Mapped[datetime] = mapped_column(
        DateTime(timezone= True),
        server_default = func.now(),
        nullable=False
    )
    proposal:Mapped["ProposalModel"]  = relationship(
        "ProposalModel",
        back_populates= "approvals,"

    )