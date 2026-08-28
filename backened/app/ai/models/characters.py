from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ai.database.database import Base

if TYPE_CHECKING:
    from app.ai.models.film_project import FilmProject


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("film_projects.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    status: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    injuries: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    wardrobe: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    project: Mapped["FilmProject"] = relationship(
        "FilmProject",
        back_populates="characters",
    )