from fastapi import FastAPI

from src.db.main import initdb

from .auth.routers import auth_router
from .books.routes import book_router
from .demo.routers import demo_router

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


app.include_router(demo_router, tags=["Demo"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
