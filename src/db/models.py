import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .create_db import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user: Mapped[str] = mapped_column(nullable=False)
    hached_passwd: Mapped[str | None] = mapped_column(nullable=True)


class Messages(Base):
    __tablename__ = 'messages'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    encrypted_message: Mapped[str] = mapped_column(nullable=False)


