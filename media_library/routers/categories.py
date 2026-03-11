from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.category import Category
from models.book import Book
from models.podcast import Podcast
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


# CREATE CATEGORY
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):

    existing = db.query(Category).filter(Category.name == payload.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name '{payload.name}' already exists.",
        )

    category = Category(**payload.model_dump())

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


# GET ALL CATEGORIES (with pagination)
@router.get("/", response_model=List[CategoryResponse])
def list_categories(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):

    categories = db.query(Category).offset(skip).limit(limit).all()

    return categories


# GET CATEGORY BY ID
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):

    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found.",
        )

    return category


# UPDATE CATEGORY
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):

    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found.",
        )

    # Check duplicate name
    if payload.name and payload.name != category.name:
        name_conflict = db.query(Category).filter(Category.name == payload.name).first()

        if name_conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name '{payload.name}' already exists.",
            )

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


# DELETE CATEGORY
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):

    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found.",
        )

    # Assignment rule: cannot delete if books or podcasts exist
    if category.books or category.podcasts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category '{category.name}' because it has books or podcasts assigned.",
        )

    db.delete(category)
    db.commit()

    return