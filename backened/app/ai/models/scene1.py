# schema for database scene
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ai.database.database import Base

if TYPE_CHECKING:
    from app.ai.models.film_project import FilmProject


class Scene(Base):
    __tablename__ = "scenes"

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("film_projects.id"),
        nullable=False,
    )

    scene_number: Mapped[int] = mapped_column(
        nullable=False,
    )

    header: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    location: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    time_of_day: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    visual_prompt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    project: Mapped["FilmProject"] = relationship(
        "FilmProject",
        back_populates="scenes",
    )