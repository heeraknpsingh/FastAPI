from typing import Optional

from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
app = FastAPI()


class Book:
    bid: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None, description='id field is optional')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1900, lt=2025)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "A new book",
                "author": "Heera",
                "description": "A new description of book",
                "rating": 5,
                "published_date": 2000
            }
        }


BOOKS = [
    Book(1, "Computer Science Pro", "heera", "A very nice book!", 5, 2010),
    Book(2, "Be Fast with FastAPI", "heera", "A great book!", 5, 2010),
    Book(3, "Master Endpoints", "heera", "A awesome book!", 5, 2009),
    Book(4, "HP1", "Author 1", "Book Description", 2, 2008),
    Book(5, "HP2", "Author 2", "Book Description", 3, 2021),
    Book(6, "HP3", "Author 3", "Book Description", 1, 2016)
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='no book found with the given id')


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    book_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_return.append(book)
    return book_to_return


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(gt=1900, lt=2025)):
    book_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            book_to_return.append(book)
    return book_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='no book found to update with the given id')


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='no book found to delete with the given id')
