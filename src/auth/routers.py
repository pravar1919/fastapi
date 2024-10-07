from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_sessions
from .schemas import UserCreateModel, User
from .service import UserService

auth_router = APIRouter()
user_service = UserService()


@auth_router.post('/signup', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user_account(data: UserCreateModel, session: AsyncSession = Depends(get_sessions)):
    email = data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with this email already exists, User another email."
        )
    new_user = await user_service.create_user(data, session)
    print(new_user.__dict__)
    return new_user
