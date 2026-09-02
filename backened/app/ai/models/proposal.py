from sqlalchemy import ForeignKey , Column , Text , String, DateTime, func
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped , mapped_column , relationship
from app.ai.database.database import Base

if TYPE_CHECKING:
    from app.ai.models.scene1 import Scene
    from app.ai.models.film_project import FilmProject
    from app.ai.models.event import EventModel
    from app.ai.models.approval import ApprovalModel

class ProposalModel(Base):
    __tablename__ = "proposals"

    id:Mapped[int] = mapped_column(
        primary_key=True,
    )
    proposal_id:Mapped[str] = mapped_column(
        Text,
        nullable= False,
        unique= True
    )
    project_id:Mapped[int] = mapped_column(
        ForeignKey("film_projects.id",ondelete="CASCADE"),
        nullable= False,
    )
    scene_id:Mapped[int] = mapped_column(
        ForeignKey("scenes.id",ondelete="CASCADE"),
        nullable= True,
    )
    description:Mapped[str|None]= mapped_column(
        Text,
        nullable =True,
    )
    reason:Mapped[str|None] = mapped_column(
        Text,
        nullable =True
    )
    status:Mapped[str|None] = mapped_column(
        Text,
        nullable = True
    )
    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default = func.now(),
        nullable =False

    )
    project:Mapped["FilmProject"] = relationship(
        "FilmProject",
        back_populates = "proposals"
    )
    scenes:Mapped["Scene | None"]= relationship(
        "Scene",
        back_populates= "proposals"
    )
    events:Mapped["EventModel"] = relationship(
        "EventModel",
        back_populates="Proposal"
    )
    approvals:Mapped["ApprovalModel"] = relationship (
        "ApprovaModel",
        back_populates= "proposal"
    )