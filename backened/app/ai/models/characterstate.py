from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.ai.database.database import Base

if TYPE_CHECKING:
    from app.ai.models.characters import Character
    from app.ai.models.scene1 import Scene


class CharacterState(Base):
    __tablename__ = "character_states"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id", ondelete="CASCADE"),
        nullable=False,
    )

    scene_id: Mapped[int] = mapped_column(
        ForeignKey("scenes.id", ondelete="CASCADE"),
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

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    character: Mapped["Character"] = relationship(
        "Character",
        back_populates="states",
    )

    scene: Mapped["Scene"] = relationship(
        "Scene",
        back_populates="character_states",
    )