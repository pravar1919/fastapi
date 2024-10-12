from datetime import datetime, timedelta

from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status
from src.db.main import get_sessions

from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from .schemas import Token, User, UserCreateModel, UserLogin, UserBooksModel
from .service import UserService
from .utils import create_access_token, decode_access_token, verify_password
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
role_checker = Depends(RoleChecker(['admin', 'user']))


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
    return new_user


@auth_router.post('/login')
async def login_user(data: UserLogin, session: AsyncSession = Depends(get_sessions)):
    user = await user_service.get_user_by_email(data.email, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No User found."
        )
    password_valid = verify_password(data.password, user.password)
    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either email or password is incorrect."
        )
    access = create_access_token(
        data={"email": user.email, "id": str(user.id), "role": user.role}
    )
    refresh = create_access_token(
        data={"email": user.email, "id": str(user.id)},
        refresh=True,
        expiry=timedelta(7)
    )

    return JSONResponse(
        content={
            "access": access,
            "refresh": refresh,
        },
        status_code=status.HTTP_200_OK
    )

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            data = token_details['user']
        )
        return JSONResponse(
            content={"access_token": new_access_token}
        )
    
    raise HTTPException(
        status_code= status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired token."
    )


@auth_router.get('/me', response_model=UserBooksModel, dependencies=[role_checker])
async def get_current_user(user = Depends(get_current_user)):
    return user

@auth_router.get('/logout')
async def revoke_token(token_detail: dict = Depends(AccessTokenBearer())):
    jti = token_detail['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message": "Logged out successfully."
        },
        status_code= status.HTTP_200_OK
    )


