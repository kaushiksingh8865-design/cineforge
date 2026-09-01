from sqlalchemy import ForeignKey , Column , Text , String, DateTime, func
from datetime import datetime 
from typing import TYPE_CHECKING
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped , mapped_column , relationship
from app.ai.database.database import Base
if TYPE_CHECKING:
    from app.ai.models.scene1 import Scene


class SceneState(Base):
    __tablename__ = "scenestate"




    #primary key 
    id:Mapped[int] = mapped_column(
        primary_key=True,

    )
    scene_id:Mapped[int] = mapped_column(
        ForeignKey("scenes.id",ondelete="CASCADE") , 
        
        nullable= False,
        unique= True,
    )

    state_data:Mapped[dict] = mapped_column(
        JSONB,
        default= dict,
        nullable = False,
        

    )
    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default= func.now(),
        nullable= False
    )
    updated_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate= func.now(),
        server_default= func.now(),
        nullable= False,
    )
    scene: Mapped["Scene"] = relationship(
        "Scene",
        back_populates="state"
    )