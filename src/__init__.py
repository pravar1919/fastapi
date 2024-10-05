from fastapi import FastAPI
from .books.routes import book_router
from .demo.routers import demo_router

version = "v1"

app = FastAPI(
    title="Book Crud",
    description="Book Review Service Crud",
    version=version
)


app.include_router(demo_router, tags=["demo"])
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
