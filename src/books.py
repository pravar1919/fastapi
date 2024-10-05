from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

from typing import List

app = FastAPI()

books_data = [
    {
        "id": 1,
        "title": "book1",
        "author": "author1",
        "date": "2021-01-01"
    },
    {
        "id": 2,
        "title": "book2",
        "author": "author2",
        "date": "2021-02-01"
    },
    {
        "id": 3,
        "title": "book3",
        "author": "author3",
        "date": "2021-03-01"
    },
    {
        "id": 4,
        "title": "book4",
        "author": "author4",
        "date": "2021-04-01"
    },
    {
        "id": 5,
        "title": "book5",
        "author": "author5",
        "date": "2021-05-01"
    },
]


class BookModel(BaseModel):
    id: int
    title: str
    author: str
    date: str


class BookUpdate(BaseModel):
    title: str
    author: str
    date: str


@app.get('/books', response_model=List[BookModel], status_code=status.HTTP_200_OK)
async def get_books():
    return books_data


@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookModel) -> dict:
    new_book = book_data.model_dump()
    books_data.append(new_book)
    return new_book


@app.get('/book/{id}', response_model=List[BookModel])
async def get_book(id: int) -> dict:
    book = list(filter(lambda x: x['id'] == id, books_data))
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not found"
        )
    return book


@app.put('/book/{book_id}')
async def update_book(book_id: int, book_data: BookUpdate) -> dict:
    book = list(filter(lambda x: x['id'] == book_id, books_data))
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not found"
        )
    book[0]['title'] = book_data.title
    book[0]['author'] = book_data.author
    book[0]['date'] = book_data.date
    return book[0]


@app.delete('/book/{id}')
async def delete_book(id: int):
    book = list(filter(lambda x: x['id'] == id, books_data))
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not found"
        )
    books_data.remove(book[0])
    return {"detail": "Book deleted..."}
