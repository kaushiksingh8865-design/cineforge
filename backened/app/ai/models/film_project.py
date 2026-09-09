from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ai.database.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ai.models.scene1 import Scene
    from app.ai.models.characters import Character
    from app.ai.models.property import Prop
    from app.ai.models.proposal import ProposalModel
    from app.ai.models.version import Version
    from app.ai.models.generated import GeneratedFile
    from app.ai.models.source import SourceFile

class FilmProject(Base):
    __tablename__ = "film_projects"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    logline: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    scenes: Mapped[list["Scene"]] = relationship(
        "Scene",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    characters: Mapped[list["Character"]] = relationship(
    "Character",
    back_populates="project",
    cascade="all, delete-orphan",
    )
    props:Mapped[list['Prop']] = relationship(
        "Prop",
        back_populates="project",
        cascade= "all, delete-orphan"
    )

    proposals:Mapped[list["ProposalModel"]] = relationship(
        "ProposalModel",
        back_populates="project"
    )
    versions: Mapped[list["Version"]] = relationship(
        "Version",
        back_populates="project",
    ) 
    generated_files:Mapped["GeneratedFile"] = relationship(
        "GeneratedFile",
        back_populates="project",
    ) 
    source_files: Mapped[list["SourceFile"]] = relationship(
    "SourceFile",
    back_populates="project",
    cascade="all, delete-orphan",
)