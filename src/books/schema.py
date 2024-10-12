from pydantic import BaseModel
import uuid
from typing import List
from datetime import datetime, date
from src.reviews.schema import ReviewModel


class BookModel(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    published_date: date
    created_at: datetime
    update_at: datetime


class BookDetailModel(BookModel):
    reviews: List[ReviewModel]


class BookCreateModel(BaseModel):
    title: str
    author: str
    published_date: str


class BookUpdate(BaseModel):
    title: str
    author: str
