from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ai.database.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ai.models.scene1 import Scene
    from app.ai.models.characters import Character
    from app.ai.models.property import PropState


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
    prop:Mapped[list['PropState']] = relationship(
        "PropState",
        back_populates="project",
        cascade= "all, delete-orphan"
    )