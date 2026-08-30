
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String , Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.ai.database.database import Base
from app.ai.models.association import scene_props
if TYPE_CHECKING :
    from app.ai.models.film_project import FilmProject
    from app.ai.models.scene1 import Scene


class PropState(Base):
    __tablename__ = "props"

    id:Mapped[int] = mapped_column(
        primary_key= True,
    ) 
    project_id:Mapped[int] = mapped_column(
        ForeignKey("film_projects.id"),
        nullable= False
    )
    name:Mapped[str] = mapped_column(
        Text, 
        nullable= False
    )
    holder:Mapped[str| None] = mapped_column(
        Text,
        nullable = True
    )
    location:Mapped[str|None] = mapped_column(
        Text,
        nullable = True
    )
    status:Mapped[str] = mapped_column(
        Text,
        nullable = False

    )
    discription:Mapped[str|None]= mapped_column(
        Text,
        nullable= True

    )
    project:Mapped["FilmProject"] =relationship(
        'FilmProject',
        back_populates="props"

    )
    #connection with scenes
    scenes:Mapped[list['Scene']] = relationship(
        scondary= scene_props,
        back_populates= 'props',
    )

