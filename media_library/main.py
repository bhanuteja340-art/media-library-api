from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
import models.category
import models.book
import models.podcast

from routers.categories import router as categories_router
from routers.books import router as books_router
from routers.podcasts import router as podcasts_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Media Library API",
    description="A REST API for managing Books and Podcasts with a shared Category system.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories_router)
app.include_router(books_router)
app.include_router(podcasts_router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Media Library API is running."}