from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from fastapi import HTTPException, Request, status, Depends

from .utils import decode_access_token
from src.db.redis import add_jti_to_blocklist, token_in_blocklist
from src.db.main import get_sessions
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from src.db.models import User
from src.errors import InvalidToken, RevokedToken
from typing import List

user_service = UserService()

class TokenBearer(HTTPBearer):
    # here we can override the existing HTTPBearer method. If needed.
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        # Here we are checking if the token is valid or not
        creds = await super().__call__(request)

        token_data = decode_access_token(creds.credentials)
        if not token_data:
            raise InvalidToken()
            # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN,
            #     detail={
            #         "error": "This token is invalid or expired.",
            #         "resolution": "Please get a new token."
            #     }
            # )
        if not await token_in_blocklist(token_data['jti']):
            raise RevokedToken()
            # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN,
            #     detail={
            #         "error": "This token is invalid or has been revoked.",
            #         "resolution": "Please get a new token."
            #     },
            # )

        self.verify_token_data(token_data) # just to check if it is using in the subclasses.
        return token_data

    def verify_token_data(self, token_data: dict):
        # Just to verify if this method is not overridden in the child classes.
        raise NotImplementedError("Please override this method in child classes.")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provide a valid access token.",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provide a valid refresh token.",
            )


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_sessions)
):
    user_email = token_details['user']['email']
    user = await user_service.get_user_by_email(user_email, session)

    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if not current_user.role in self.allowed_roles:
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail = "You are not authorize to do this action."
            )
        return True

