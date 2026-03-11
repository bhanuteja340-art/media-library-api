#  Media Library API

A REST API for managing **Books** and **Podcasts** with a shared **Category** system, built with FastAPI, PostgreSQL, SQLAlchemy, and Alembic.

---

## Tech Stack

| Layer        | Technology            |
|--------------|-----------------------|
| Framework    | FastAPI               |
| Database     | PostgreSQL            |
| ORM          | SQLAlchemy 2.x        |
| Migrations   | Alembic               |
| Validation   | Pydantic v2           |

---

## Project Structure

```
media_library/
├── main.py                  # App entry point, router registration
├── database.py              # Engine, session factory, settings
├── alembic.ini              # Alembic config
├── requirements.txt
├── models/
│   ├── category.py
│   ├── book.py
│   └── podcast.py
├── schemas/
│   ├── category.py          # CategoryCreate / CategoryUpdate / CategoryResponse
│   ├── book.py              # BookCreate / BookUpdate / BookResponse
│   └── podcast.py           # PodcastCreate / PodcastUpdate / PodcastResponse
├── routers/
│   ├── categories.py
│   ├── books.py
│   └── podcasts.py
└── migrations/
    ├── env.py
    ├── script.py.mako
    └── versions/
        └── xxxx_create_tables.py
```

---

## Setup & Running Locally

### 1. Prerequisites

- Python 3.11+
- PostgreSQL running locally

### 2. Clone the repository

```bash
git clone https://github.com/bhanuteja340-art/media-library-api.git
cd media-library-api/media_library
```

### 3. Create and activate virtual environment

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create PostgreSQL database

```bash
psql -U postgres -c "CREATE DATABASE media_library;"
```

### 6. Create `.env` file

Create a `.env` file inside the `media_library` folder:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/media_library
```

### 7. Run Alembic migrations

```bash
alembic upgrade head
```

### 8. Start the API

```bash
uvicorn main:app --reload
```

API is live at **http://localhost:8000**

Interactive docs: **http://localhost:8000/docs**

---

## API Endpoints

### Categories

| Method | Endpoint           | Description         |
|--------|--------------------|---------------------|
| POST   | `/categories/`     | Create a category   |
| GET    | `/categories/`     | List all categories |
| GET    | `/categories/{id}` | Get one category    |
| PUT    | `/categories/{id}` | Update a category   |
| DELETE | `/categories/{id}` | Delete a category   |

### Books

| Method | Endpoint      | Description   |
|--------|---------------|---------------|
| POST   | `/books/`     | Create a book |
| GET    | `/books/`     | List all books|
| GET    | `/books/{id}` | Get one book  |
| PUT    | `/books/{id}` | Update a book |
| DELETE | `/books/{id}` | Delete a book |

### Podcasts

| Method | Endpoint         | Description      |
|--------|------------------|------------------|
| POST   | `/podcasts/`     | Create a podcast |
| GET    | `/podcasts/`     | List all podcasts|
| GET    | `/podcasts/{id}` | Get one podcast  |
| PUT    | `/podcasts/{id}` | Update a podcast |
| DELETE | `/podcasts/{id}` | Delete a podcast |

---

## Bonus Features

| Feature | How to use |
|---|---|
| Filter by category | `GET /books/?category_id=1` |
| Pagination | `GET /books/?skip=0&limit=10` |
| Alembic migrations | `alembic upgrade head` |

---

## Business Rules

- Category must exist before assigning to a book or podcast — returns `400` if invalid
- Deleting a category that has books or podcasts returns `400`
- Unique category names enforced
- Book and Podcast responses include full category object with name

---

## HTTP Status Codes

| Code | Meaning                        |
|------|--------------------------------|
| 200  | OK                             |
| 201  | Created                        |
| 204  | Deleted successfully           |
| 400  | Bad request / validation error |
| 404  | Resource not found             |
| 422  | Invalid data type sent         |