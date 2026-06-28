from uuid import UUID
from pydantic import BaseModel, Field


class Users(BaseModel):
    user: str = Field(max_length=50)
    passwd: str = Field(max_digits=810)


class UserResponse(BaseException):
    id: UUID
    name: str


class Message(BaseModel):
    message: str


class ResponseMessege(BaseModel):
    id: UUID
    message: str