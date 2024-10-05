from pydantic import BaseModel


class BookModel(BaseModel):
    id: int
    title: str
    author: str
    date: str


class BookUpdate(BaseModel):
    title: str
    author: str
    date: str
