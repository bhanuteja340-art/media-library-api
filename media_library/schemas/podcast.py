from pydantic import BaseModel
from typing import Optional
from schemas.category import CategoryResponse


class PodcastCreate(BaseModel):
    title: str
    host: str
    episode_count: Optional[int] = None
    avg_duration_minutes: Optional[int] = None
    category_id: Optional[int] = None  # optional — podcast can exist without category


class PodcastUpdate(BaseModel):
    title: Optional[str] = None
    host: Optional[str] = None
    episode_count: Optional[int] = None
    avg_duration_minutes: Optional[int] = None
    category_id: Optional[int] = None


class PodcastResponse(BaseModel):
    id: int
    title: str
    host: str
    episode_count: Optional[int] = None
    avg_duration_minutes: Optional[int] = None
    category_id: Optional[int] = None  # nullable in DB
    category: Optional[CategoryResponse] = None  # full category object with name

    model_config = {"from_attributes": True}