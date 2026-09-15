# GTFS Transit Service

A backend service that imports BURULAS's GTFS (General Transit Feed Specification) data, versions it in a relational database using a dataset/snapshot model, and will expose it through a REST API.

## Tech Stack

- **FastAPI** — API framework
- **PostgreSQL** + **SQLAlchemy** (ORM) — relational data storage
- **MinIO** — object storage for the raw uploaded GTFS zip files
- **Pydantic** — validation of incoming GTFS data
- **Docker Compose** — local development environment for PostgreSQL and MinIO

## Architecture Notes

- Every GTFS upload belongs to a **Dataset** (e.g. `"burulas"` — the data source) and is recorded as a **Snapshot** (a specific upload of that source at a point in time). This keeps uploads from different times from mixing with each other.
- The raw zip file is uploaded to MinIO **before** validation, so that even an invalid upload remains inspectable for debugging (raw/bronze-layer pattern).
- `shapes.txt` is intentionally out of scope for this project.
- Foreign keys reference the internal integer primary keys of related tables (e.g. `trips.route_id → routes.id`), not the raw GTFS string IDs, since a GTFS ID is only unique within a single snapshot.

## Setup

1. Start the required services:
   ```bash
   docker compose up -d
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your own values.

## Running

```bash
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- MinIO console: http://localhost:9001

## Endpoints

- `POST /import` — accepts `slug` (form, text) and `zip_file` (form, file). Uploads the GTFS zip to MinIO and creates the dataset/snapshot records.
  *(Currently only uploads the raw file; parsing the contents into the database is not yet implemented.)*

## Roadmap

- [ ] Parse zip contents (routes, stops, trips, stop_times), validate with Pydantic, and write to the database
- [ ] Add a `calendar.txt` table/model
- [ ] GET endpoints for routes/stops
- [ ] Tests (pytest, instead of manual testing via Postman)
- [ ] Learn Alembic and replace `Base.metadata.create_all()` with proper migrations
