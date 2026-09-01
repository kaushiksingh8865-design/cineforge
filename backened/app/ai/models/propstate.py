from sqlalchemy import ForeignKey , Column , Text , String, DateTime, func
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped , mapped_column , relationship
from app.ai.database.database import Base

if TYPE_CHECKING:
    from app.ai.models.scene1 import Scene
    from app.ai.models.property import Prop

class PropState(Base):
    __tablename__ = "prop_states"

    id:Mapped[int] = mapped_column(
        primary_key=True,
    )
    prop_id:Mapped[int] = mapped_column(
        ForeignKey("props.id",ondelete="CASCADE"),
        nullable= False,
    )
    scene_id:Mapped[int] = mapped_column(
        ForeignKey("scenes.id",ondelete="CASCADE"),
        nullable= False,
    )
    holder:Mapped[str|None] = mapped_column(
        Text,
        nullable= True,
    )
    location:Mapped[str|None] = mapped_column(
        Text,
        nullable= True,
    )
    status:Mapped[str|None] = mapped_column(
        Text,
        nullable= True,
    )
    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default= func.now(),
        nullable= False,
    )
    prop:Mapped["Prop"] = relationship(
        "Prop",
        back_populates= "states",
    )
    scene:Mapped["Scene"] = relationship(
        "Scene",
        back_populates= "prop_states",
    )