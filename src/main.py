from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get('/')
async def home() -> dict:
    return {"Hello": "world"}


@app.get('/greet/{name}')
def greet_name(name: str, age: int) -> dict:
    return {"Hello": f"world {name}", "age": age}


# making parameter optional using typing module
@app.get('/hello')
async def hello_name(age: Optional[int] = 0, name: Optional[str] = None) -> dict:
    return {"Hello": f"world {name}", "age": age}


'''
Request body to server
For that we need to verify our data using pydantic BaseModel
'''


class BookModel(BaseModel):
    title: str
    author: str


@app.post('/create_book')
async def create_book(book_data: BookModel):
    return {
        "title": book_data.title,
        "author": book_data.author
    }

'''
We can also access all the headers in FastAPI using Header in fastapi module

'''


@app.get('/get_headers')
async def get_headers(
    # Each headers can be accessed here using lowercase of that header
    accept: str = Header(None),
    request_url: str = Header(None),
    content_type: str = Header(None),
    x_custom_jwt: str = Header(None)
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Request URL"] = request_url
    request_headers["Content Type"] = content_type
    request_headers["x_custom_jwt"] = x_custom_jwt

    return request_headers
