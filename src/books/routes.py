from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import BookModel, BookCreateModel, BookUpdate
from src.db.main import get_sessions
from src.books.service import BookService
from typing import List
import uuid
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()
security = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin', 'user']))


@book_router.get("/", response_model=List[BookModel], status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_books(
    session: AsyncSession = Depends(get_sessions), token_details: dict=Depends(security)
):
    books = await book_service.get_books(session)
    return books


@book_router.get("/user/{user_id}", response_model=List[BookModel], status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_user_book_submission(
    user_id: uuid.UUID, session: AsyncSession = Depends(get_sessions), token_details: dict=Depends(security)
):
    books = await book_service.get_user_books(user_id, session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookModel)
async def create_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_sessions),
    token_details: dict=Depends(security),
):
    user_id = token_details.get('user')['id']
    new_book = await book_service.create_book(book_data, user_id, session)
    return new_book


@book_router.get("/{id}", response_model=BookModel)
async def get_book(
    id: str,
    session: AsyncSession = Depends(get_sessions),
    token_details: dict=Depends(security),
) -> dict:
    book = await book_service.get_book(id, session)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book Not found"
        )
    return book


@book_router.put("/{book_id}", response_model=BookModel)
async def update_book(
    book_id: str,
    book_data: BookUpdate,
    session: AsyncSession = Depends(get_sessions),
    token_details: dict=Depends(security),
) -> dict:
    book = await book_service.update_book(book_id, book_data, session)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book Not found"
        )
    return book


@book_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    id: str,
    session: AsyncSession = Depends(get_sessions),
    token_details: dict=Depends(security),
):
    book = await book_service.delete_book(id, session)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book Not found"
        )
    return {}
