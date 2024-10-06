from pydantic import BaseModel
import uuid
from datetime import datetime, date


class BookModel(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    published_date: date
    created_at: datetime
    update_at: datetime


class BookCreateModel(BaseModel):
    title: str
    author: str
    published_date: str


class BookUpdate(BaseModel):
    title: str
    author: str
