from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime
from src.db.models import Book
from .schema import BookCreateModel, BookUpdate


class BookService:
    async def get_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)
        if not result:
            return None
        return result.all()
    
    async def get_user_books(self, user_id, session):
        statement = select(Book).where(Book.user_id==user_id).order_by(desc(Book.created_at))

        result = await session.exec(statement)
        if not result:
            return None
        return result.all()

    async def get_book(self, id: str, session: AsyncSession):
        statement = select(Book).where(Book.id == id)

        result = await session.exec(statement)
        if not result:
            return None
        return result.first()

    async def create_book(self, data: BookCreateModel, user_id: str, session: AsyncSession):
        book_dict = data.model_dump()

        book_obj = Book(**book_dict)
        book_obj.published_date = datetime.strptime(
            book_dict['published_date'], '%Y-%m-%d')
        book_obj.user_id = user_id
        session.add(book_obj)
        await session.commit()
        return book_obj

    async def update_book(self, id: str, data: BookUpdate, session: AsyncSession):
        book_to_update = await self.get_book(id, session)

        if book_to_update:
            update_data_dict = data.model_dump()

            for k, v in update_data_dict.items():
                setattr(book_to_update, k, v)

            await session.commit()
            return book_to_update
        return None

    async def delete_book(self, id: str, session: AsyncSession):
        book_to_delete = await self.get_book(id, session)
        if book_to_delete:
            await session.delete(book_to_delete)
            await session.commit()
            return True
        else:
            return None
