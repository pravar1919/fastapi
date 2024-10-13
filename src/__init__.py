from fastapi import FastAPI, status

from src.db.main import initdb

from .auth.routers import auth_router
from .books.routes import book_router
from .demo.routers import demo_router
from .reviews.routers import review_router
from .errors import (BooklyException, InvalidToken, RevokedToken, create_exception_handler)

from contextlib import asynccontextmanager


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is staring...")
    await initdb()
    # everyting above yield executed when the server is started.
    yield
    # everyting below yield executed when the server is stopped.
    print("Server hase been stopped...")


version = "v1"

app = FastAPI(
    title="Book Crud",
    description="Book Review Service Crud",
    version=version,
    # removed this lifespan for creating db, will use alembic.
    # lifespan=life_span 
)

app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": "This token is invalid or expired.",
            "resolution": "Please get a new token."
        }
    )
)
app.include_router(demo_router, tags=["Demo"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["Reviews"])
