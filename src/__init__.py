from fastapi import FastAPI, status

from src.db.main import initdb

from .auth.routers import auth_router
from .books.routes import book_router
from .demo.routers import demo_router
from .issues.routers import issues_router
from .reviews.routers import review_router
from .errors import register_all_errors
from .middleware import registe_middleware

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

register_all_errors(app)

registe_middleware(app)

app.include_router(demo_router, tags=["Demo"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["Reviews"])
app.include_router(issues_router, prefix=f"/api/{version}/issues", tags=["Issues"])
