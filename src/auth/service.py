from .schemas import UserCreateModel
from .models import User
from .utils import generate_password_hash, verify_password
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        user = await session.exec(statement)

        user_obj = user.first()
        return user_obj

    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user else False

    async def create_user(self, data: UserCreateModel, session: AsyncSession):
        data_dict = data.model_dump()

        new_user = User(**data_dict)

        new_user.password = generate_password_hash(data_dict['password'])

        session.add(new_user)
        await session.commit()
        return new_user
