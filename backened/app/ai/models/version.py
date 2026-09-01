from sqlalchemy.orm import Mapped , mapped_column ,relationship
from sqlalchemy import ForeignKey , Text , String 

from app.ai.database.database import Base
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import DateTime , func 
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from app.ai.models.film_project import FilmProject
    from app.ai.models.generated import GeneratedFile

class Version(Base):
    __tablename__ = "versions"

    id:Mapped[int] = mapped_column(
        primary_key = True,
    )
    project_id:Mapped[int] = mapped_column(
        ForeignKey("film_projects.id", ondelete="CASCADE"),
        nullable= False
    )
    version_number:Mapped[str] = mapped_column(
        Text,
        nullable = False,
    )
    description:Mapped[str|None] = mapped_column(
        Text,
        nullable = True,
    )
    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone =True),
        server_default = func.now(),
        nullable= False,
    )
    state_snapshot:Mapped[dict] = mapped_column(
        JSONB,
        default = dict,
        nullable= False,
    )
    project:Mapped["FilmProject"] = relationship(
        "FilmProject",
        back_populates = "versions"
    )
    generated_files:Mapped["GeneratedFile"] = relationship(
        "GeneratedFile",
        back_populates = "version"
    )