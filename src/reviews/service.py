from fastapi import Depends, HTTPException, status
from src.db.models import Reviews
from src.auth.service import UserService
from src.books.service import BookService
from src.db.main import get_sessions
from .schema import ReviewCreateModel
import logging
from sqlalchemy.ext.asyncio.session import AsyncSession


book_service = BookService()
user_service = UserService()

class ReviewService:
    async def add_review(
        self,
        user_email: str,
        book_id: str,
        data: ReviewCreateModel,
        session: AsyncSession = Depends(get_sessions),
    ):
        try:
            book = await book_service.get_book(book_id, session)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "Invalid book Id.",
                        "resolution": "Please get valid book."
                    }
            )
            user = await user_service.get_user_by_email(user_email, session)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "Invalid User."
                    }
            )
            review_data_dict = data.model_dump()
            review = Reviews(**review_data_dict)
            review.book = book
            review.user = user
            session.add(review)
            await session.commit()
            return review
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Opps!! something went wrong." # TODO
            )
