from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from fastapi import HTTPException, Request, status

from .utils import decode_access_token


class TokenBearer(HTTPBearer):
    # here we can override the existing HTTPBearer method. If needed.
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        # Here we are checking if the token is valid or not
        creds = await super().__call__(request)

        token_data = decode_access_token(creds.credentials)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token.",
            )
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
