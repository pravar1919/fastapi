from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class BooklyException(Exception):
    """
    Base class for all the exceptions
    """

    pass


class InvalidToken(BooklyException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(BooklyException):
    """User has provided a token that has been revoked"""

    pass


def create_exception_handler(
    status_code: int, content: Any
) -> Callable[[Request, Exception], JSONResponse]:
    
    async def exception_handler(request: Request, exc: BooklyException):

        return JSONResponse(content=content, status_code=status_code)

    return exception_handler

