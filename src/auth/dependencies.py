from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_access_token


class AccessTokenBearer(HTTPBearer):
    # here we can override the existing HTTPBearer method. If needed.
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        # Here we are checking if the token is valid or not
        creds = await super().__call__(request)

        token_data = decode_access_token(creds.credentials)
        if not token_data or token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token.",
            )
        return token_data
