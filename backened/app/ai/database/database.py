from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , DeclarativeBase
from backened. app.ai.core.settings import settings


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



if __name__ == "__main__":
    with engine.connect() as connection:
        print("PostgreSQL connection successful")