from sqlalchemy import UUID, text

from .create_db import Base
from sqlalchemy.orm import mapped_column, Mapped
import uuid




class Users(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user: Mapped[str] = mapped_column(nullable=False)
    hached_passwd: Mapped[str | None] 


class Messages(Base):
    __tablename__ = 'messages'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    encrypted_message: Mapped[str] = mapped_column(nullable=False)


