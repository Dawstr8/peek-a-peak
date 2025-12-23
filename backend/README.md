# 🏔️ Peek-a-Peak - Backend API

> **High-performance FastAPI backend with PostGIS geospatial engine, async processing, and robust session authentication**

A production-ready backend service designed for scalability and maintainability. This project leverages modern Python features, SQLModel for type-safe database interactions, and PostGIS for advanced geospatial capabilities.

## 🚀 Quick Start

> **Tip:** The recommended way to run this project is using the VS Code Dev Container, which comes with Postgres, PostGIS, and MinIO pre-configured. See the [Dev Container README](../.devcontainer/README.md) for details.

1. **Install Dependencies**

   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**

   ```bash
   cp .env.example .env
   # Update DB_HOST, DB_USER, DB_PASSWORD if needed
   ```

   Ensure PostgreSQL is running with PostGIS extension enabled.

3. **Run Migrations & Seed Database**

   ```bash
   alembic upgrade head
   python3 -m src.database.seed.run_seed
   ```

4. **Start Server**

   ```bash
   python3 -m fastapi dev main.py
   ```

   Visit **http://localhost:8000/docs** for Swagger UI.

## 🧱 Tech Stack

| Category         | Technologies                                       |
| :--------------- | :------------------------------------------------- |
| **Core**         | Python 3.11+, FastAPI, Pydantic v2                 |
| **Database**     | PostgreSQL 15, PostGIS, SQLModel, SQLAlchemy 2.0   |
| **Migrations**   | Alembic                                            |
| **Geospatial**   | GeoAlchemy2, PostGIS (`ST_Distance`, `ST_DWithin`) |
| **Async/Queue**  | FastAPI BackgroundTasks (Weather enrichment)       |
| **Storage**      | Local Filesystem / MinIO (S3 Compatible)           |
| **Data Seeding** | BeautifulSoup4, Pandas, Requests                   |
| **Testing**      | Pytest, AsyncClient, Factory Boy                   |

## ✨ Engineering Highlights

### 🏗️ Domain-Driven Architecture

- **Modular Design**: Codebase organized by domain (`auth`, `peaks`, `weather`) rather than technical layers, facilitating easier maintenance and feature addition.
- **Type Safety**: Extensive use of **SQLModel** and **Pydantic** ensures strict type validation from the database layer up to the API response.

### 🌍 Geospatial Intelligence

- **PostGIS Integration**: Utilizes `Geography(Point, 4326)` for accurate location storage.
- **Spatial Queries**: Efficiently performs radius searches and distance calculations directly in the database using optimized spatial indices.

### ⚡ Performance & Scalability

- **Async Processing**: Heavy operations like weather data fetching are offloaded to background tasks to keep the API response time low.
- **Pluggable Storage**: Abstracted storage interface allows seamless switching between local filesystem (dev) and S3/MinIO (prod).
- **Session Auth**: Secure, HttpOnly cookie-based session management with server-side storage.

## 📁 Project Structure

```
backend/
├── src/
│   ├── api.py                  # API Router aggregation
│   ├── main.py                 # App entrypoint & middleware
│   ├── config.py               # Environment configuration
│   ├── auth/                   # Authentication & Session logic
│   ├── database/               # DB connection & session handling
│   ├── peaks/                  # Peak management & geospatial logic
│   ├── photos/                 # Photo upload & processing
│   ├── weather/                # Async weather enrichment service
│   └── ...                     # Other domain modules
├── alembic/                    # Database migrations
├── tests/                      # Async test suite
└── requirements.txt
```

## 🛠️ Available Commands

| Command                                 | Description                               |
| :-------------------------------------- | :---------------------------------------- |
| `python -m fastapi dev main.py`         | Start development server with hot reload  |
| `alembic upgrade head`                  | Apply pending database migrations         |
| `alembic revision --autogenerate`       | Generate new migration from model changes |
| `python3 -m src.database.seed.run_seed` | Seed database with initial peak data      |
| `pytest`                                | Run the full async test suite             |

## 🧪 Testing

The project maintains a high standard of code quality with a comprehensive test suite using `pytest`.

- **Async Tests**: Fully async test execution using `httpx.AsyncClient`.
- **Fixtures**: Reusable test data and states defined in `tests/conftest.py`.
- **Isolation**: Tests run against a separate test database to ensure data integrity.

---

_Part of the Peek-a-Peak project._
