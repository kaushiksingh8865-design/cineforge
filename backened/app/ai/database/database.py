from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , DeclarativeBase , Session
from app.ai.core.settings import settings
from collections.abc import Generator

engine =create_engine(
    settings.database_url,
    pool_pre_ping =True,
)
SessionLocal = sessionmaker(
    bind = engine,
    autoflush=False,
    autocommit = False,
    )
class Base(DeclarativeBase):
    pass

def get_db() -> Generator[Session , None , None]:
    db = SessionLocal()

    try:
        yield db
    finally: 
        db.close()



if __name__ == "__main__":
    with engine.connect() as connection:
        print("PostgreSQL connection successful")