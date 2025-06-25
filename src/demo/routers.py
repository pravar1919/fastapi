from fastapi import APIRouter, Header
from typing import Optional
from .schema import BookModel

demo_router = APIRouter()


@demo_router.get('/')
async def home() -> dict:
    return {"Hello": "world"}


@demo_router.get('/greet/{name}')
def greet_name(name: str) -> dict:
    return {"Hello": f"world {name}"}


# making parameter optional using typing module
@demo_router.get('/hello')
async def hello_name(age: Optional[int] = 0, name: Optional[str] = None) -> dict:
    return {"Hello": f"world {name}", "age": age}


'''
Request body to server
For that we need to verify our data using pydantic BaseModel
'''


@demo_router.post('/create_book')
async def create_book(book_data: BookModel):
    return {
        "title": book_data.title,
        "author": book_data.author
    }

'''
We can also access all the headers in FastAPI using Header in fastapi module

'''


@demo_router.get('/get_headers', status_code=200)
async def get_headers(
    # Each headers can be accessed here using lowercase of that header
    accept: str = Header(None),
    content_type: str = Header(None),
    x_custom_jwt: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None)
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Content Type"] = content_type
    request_headers["x_custom_jwt"] = x_custom_jwt
    request_headers["User Agent"] = user_agent
    request_headers["Host"] = host

    return request_headers
