from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

from app.ai.database.database import Base

from app.ai.models.film_project import FilmProject
from app.ai.models.scene1 import Scene
from app.ai.models.characters import Character
from app.ai.models.property import Prop
from app.ai.models.association import scene_props, scene_characters
from app.ai.models.scenestate import SceneState
from app.ai.models.characterstate import CharacterState
from app.ai.models.propstate import PropState

from app.ai.core.settings import settings


# Alembic Config object
config = context.config


# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# SQLAlchemy metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    database_url = settings.database_url.replace(
        "+asyncpg",
        "+psycopg",
    )

    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""

    database_url = settings.database_url.replace(
        "+asyncpg",
        "+psycopg",
    )

    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

    connectable.dispose()


# Actually run Alembic
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()