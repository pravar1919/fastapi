from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from src.books import schema
import uuid


class User(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    password: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime

class UserBooksModel(User):
    books: List[schema.BookModel]


class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: str
    first_name: str
    last_name: str
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access: str
