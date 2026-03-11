from pydantic import BaseModel
from typing import Optional
from schemas.category import CategoryResponse


class BookCreate(BaseModel):
    title: str
    author: str
    pages: Optional[int] = None
    published_year: Optional[int] = None
    category_id: Optional[int] = None  # optional — book can exist without category


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    pages: Optional[int] = None
    published_year: Optional[int] = None
    category_id: Optional[int] = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    pages: Optional[int] = None
    published_year: Optional[int] = None
    category_id: Optional[int] = None  # nullable in DB
    category: Optional[CategoryResponse] = None  # full category object with name

    model_config = {"from_attributes": True}
    