from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from .books_data import books_data
from .schema import BookModel, BookUpdate
from typing import List

book_router = APIRouter()


@book_router.get('/', response_model=List[BookModel], status_code=status.HTTP_200_OK)
async def get_books():
    return books_data


@book_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookModel) -> dict:
    new_book = book_data.model_dump()
    books_data.append(new_book)
    return new_book


@book_router.get('/{id}', response_model=List[BookModel])
async def get_book(id: int) -> dict:
    book = list(filter(lambda x: x['id'] == id, books_data))
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not found"
        )
    return book


@book_router.put('/{book_id}')
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


@book_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int):
    book = list(filter(lambda x: x['id'] == id, books_data))
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not found"
        )
    books_data.remove(book[0])
    return {}
