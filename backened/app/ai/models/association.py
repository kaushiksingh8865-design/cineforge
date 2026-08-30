from  sqlalchemy import ForeignKey , Column , Table
from app.ai.database.database  import Base

scene_characters = Table(
    "scene_characters",
    Base.metadata,
    Column(
        "scene_id",
        ForeignKey("scenes.id", ondelete ="CASCADE"),
        primary_key = True
    ),
    Column(
        "character_id",
        ForeignKey("characters.id", ondelete= "CASCADE" ),
        primary_key = True,
    )
)

scene_props = Table(
    "scene_props",
    Base.metadata,
    Column(
    "scene.id",
    ForeignKey("scenes.id", ondelete ="CASCADE"),
    primary_key= True
    ),
    Column(
        "prop_id",
        ForeignKey("props.id",ondelete= "CASCADE"),
        primary_key= True,

    )
)