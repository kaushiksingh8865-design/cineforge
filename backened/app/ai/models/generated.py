from sqlalchemy import ForeignKey , String ,Text 
from sqlalchemy.orm import Mapped , mapped_column , relationship
from app.ai.database.database import Base
from datetime import datetime
from sqlalchemy import DateTime , func
from sqlalchemy.dialects.postgresql import JSONB
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ai.models.film_project import FilmProject
    from app.ai.models.version import Version

class GeneratedFile(Base):
    __tablename__ = "generated_files"

    id:Mapped[int] = mapped_column(
        primary_key = True ,
    )
    project_id:Mapped[int] = mapped_column(
        ForeignKey("film_projects.id" , ondelete="CASCADE"),
        nullable= False,

    )
    version_id:Mapped[int] = mapped_column(
        ForeignKey("versions.id", ondelete = "CASCADE"),
        nullable = False,
    )
    file_type:Mapped[str] = mapped_column(
        String(100),
        nullable = False,
    )
    file_path:Mapped[str] = mapped_column(
        Text,
        nullable = False,
    )
    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now(),
        nullable = False,
    
    )
    metadata:Mapped[dict] = mapped_column(
        JSONB,
        default= dict,
        nullable = False,
    )
    project:Mapped["FilmProject"] = relationship(
        "FilmProject",
        back_populates= "generated_files"
    )
    version:Mapped["Version"] = relationship(
        "Version",
        back_populates = "generated_files"
    )