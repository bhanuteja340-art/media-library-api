from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from database import get_db
from models.podcast import Podcast
from models.category import Category
from schemas.podcast import PodcastCreate, PodcastUpdate, PodcastResponse

router = APIRouter(prefix="/podcasts", tags=["Podcasts"])


# Helper: get podcast or return 404
def _get_or_404(db: Session, podcast_id: int) -> Podcast:
    podcast = (
        db.query(Podcast)
        .options(joinedload(Podcast.category))
        .filter(Podcast.id == podcast_id)
        .first()
    )
    if not podcast:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Podcast with id {podcast_id} not found.",
        )
    return podcast


# Helper: validate category existence
def _validate_category(db: Session, category_id: int) -> None:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with id {category_id} does not exist.",
        )


# CREATE PODCAST
@router.post("/", response_model=PodcastResponse, status_code=status.HTTP_201_CREATED)
def create_podcast(payload: PodcastCreate, db: Session = Depends(get_db)):
    # Only validate category if one is provided
    if payload.category_id is not None:
        _validate_category(db, payload.category_id)

    podcast = Podcast(**payload.model_dump())
    db.add(podcast)
    db.commit()
    db.refresh(podcast)
    return _get_or_404(db, podcast.id)


# LIST PODCASTS (pagination + optional category filter)
@router.get("/", response_model=List[PodcastResponse])
def list_podcasts(
    category_id: Optional[int] = Query(default=None, description="Filter by category ID"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Podcast).options(joinedload(Podcast.category))
    if category_id is not None:
        query = query.filter(Podcast.category_id == category_id)
    podcasts = query.offset(skip).limit(limit).all()
    return podcasts


# GET PODCAST BY ID
@router.get("/{podcast_id}", response_model=PodcastResponse)
def get_podcast(podcast_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, podcast_id)


# UPDATE PODCAST
@router.put("/{podcast_id}", response_model=PodcastResponse)
def update_podcast(podcast_id: int, payload: PodcastUpdate, db: Session = Depends(get_db)):
    podcast = _get_or_404(db, podcast_id)

    update_data = payload.model_dump(exclude_unset=True)

    # Only validate category if it's being set to a real value (not None)
    if "category_id" in update_data and update_data["category_id"] is not None:
        _validate_category(db, update_data["category_id"])

    for field, value in update_data.items():
        setattr(podcast, field, value)

    db.commit()
    db.refresh(podcast)
    return _get_or_404(db, podcast.id)


# DELETE PODCAST
@router.delete("/{podcast_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_podcast(podcast_id: int, db: Session = Depends(get_db)):
    podcast = _get_or_404(db, podcast_id)
    db.delete(podcast)
    db.commit()