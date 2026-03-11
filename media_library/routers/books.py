from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from database import get_db
from models.book import Book
from models.category import Category
from schemas.book import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])



def _get_or_404(db: Session, book_id: int) -> Book:
    book = (
        db.query(Book)
        .options(joinedload(Book.category))
        .filter(Book.id == book_id)
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found.",
        )

    return book



def _validate_category(db: Session, category_id: int) -> None:
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with id {category_id} does not exist.",
        )


# CREATE BOOK
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):

    # Assignment rule: category must exist
    _validate_category(db, payload.category_id)

    book = Book(**payload.model_dump())

    db.add(book)
    db.commit()
    db.refresh(book)

    return _get_or_404(db, book.id)


# LIST BOOKS (pagination + optional category filter)
@router.get("/", response_model=List[BookResponse])
def list_books(
    category_id: Optional[int] = Query(default=None, description="Filter by category ID"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):

    query = db.query(Book).options(joinedload(Book.category))

    if category_id is not None:
        query = query.filter(Book.category_id == category_id)

    books = query.offset(skip).limit(limit).all()

    return books


# GET BOOK BY ID
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):

    return _get_or_404(db, book_id)


# UPDATE BOOK
@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):

    book = _get_or_404(db, book_id)

    update_data = payload.model_dump(exclude_unset=True)

    # Validate category if it is being updated
    if "category_id" in update_data:
        _validate_category(db, update_data["category_id"])

    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)

    return _get_or_404(db, book.id)


# DELETE BOOK
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):

    book = _get_or_404(db, book_id)

    db.delete(book)
    db.commit()

    return
