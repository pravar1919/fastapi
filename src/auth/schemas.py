from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class User(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    password: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: str
    first_name: str | None = None
    last_name: str | None = None
    password: str = Field(min_length=6)
