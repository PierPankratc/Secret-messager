from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()
DSN = os.getenv('DSN')

class Base(DeclarativeBase):
    pass

engine = create_engine(url=DSN)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db():
    Base.metadata.create_all(bind=engine)


# схемы pydantyc
# функции хеширования
# апи
