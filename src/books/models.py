from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
import uuid
from typing import Optional
from src.auth import models


class Book(SQLModel, table=True):
    __tablename__ = "book"
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: str
    author: str
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    published_date: date
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional["models.User"] = Relationship(back_populates="books")

    def __str__(self):
        return f"<Book {self.title}>"
