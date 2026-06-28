import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


load_dotenv(Path(__file__).resolve().parents[1] / ".env")
DSN = os.getenv("DSN", "sqlite:///secrets.db")

engine = create_engine(url=DSN)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db():
    from src.db.models import Users, Messages  # noqa: F401

    Base.metadata.create_all(bind=engine)


# схемы pydantyc
# функции хеширования
# апи

create_db()