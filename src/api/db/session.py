# use sqlmodel its built over sqlalchemy makes life better
from sqlmodel import create_engine, Session,SQLModel
from .config  import DATABASE_URL,DB_TIMEZONE
import timescaledb 
# engine= 
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set, please set it in config.py")
try:
    engine= create_engine(DATABASE_URL, echo=True)
    # engine=timescaledb.create_engine(DATABASE_URL,timezone=DB_TIMEZONE)
except Exception as e:
    print(f"Error creating engine: {e}, check if db url is set correctly and if db is running")


def init_db():
    print("creating db") 
    SQLModel.metadata.create_all(engine)
    # print("creating hypertables")
    # timescaledb.metadata.create_all(engine)


def get_session():
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        print(f"Error creating session: {e}, check if db url is set correctly and if db is running")