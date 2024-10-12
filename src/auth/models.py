from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    is_verified: bool = Field(default=False)
    password: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __str__(self) -> str:
        return f"<User {self.username}>"
