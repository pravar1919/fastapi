from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_sessions
from src.db.models import User
from .service import ReviewService
from .schema import ReviewCreateModel
from src.auth.dependencies import get_current_user

review_router = APIRouter()
review_service = ReviewService()


@review_router.post("/book/{book_uid}")
async def add_review(
    book_uid: str,
    data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_sessions),
):
    review = await review_service.add_review(current_user.email, book_uid, data, session)
    return review
