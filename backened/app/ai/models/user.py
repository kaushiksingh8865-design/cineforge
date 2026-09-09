from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ai.database.database import Base


if TYPE_CHECKING:
    from app.ai.models.film_project import FilmProject


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    projects: Mapped[list["FilmProject"]] = relationship(
        "FilmProject",
        back_populates="user",
        cascade="all, delete-orphan",
    )