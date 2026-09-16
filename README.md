# GTFS Transit Service

A backend service that imports BURULAS's GTFS (General Transit Feed Specification) data, versions it in a relational database using a dataset/snapshot model, and exposes it through a REST API.

## Tech Stack

- **FastAPI** — API framework
- **PostgreSQL** + **SQLAlchemy** (ORM) — relational data storage
- **MinIO** — object storage for the raw uploaded GTFS zip files
- **Pydantic** — validation of incoming GTFS data and shaping of API responses
- **Docker Compose** — local development environment for PostgreSQL and MinIO

## Architecture Notes

- Every GTFS upload belongs to a **Dataset** (e.g. `"burulas"` — the data source) and is recorded as a **Snapshot** (a specific upload of that source at a point in time). This keeps uploads from different times from mixing with each other.
- The raw zip file is uploaded to MinIO **before** validation, so that even an invalid upload remains inspectable for debugging (raw/bronze-layer pattern).
- `shapes.txt` is intentionally out of scope for this project.
- Foreign keys reference the internal integer primary keys of related tables (e.g. `trips.route_id → routes.id`), not the raw GTFS string IDs, since a GTFS ID is only unique within a single snapshot. During import, `save_routes`/`save_stops`/`save_trips` each return a `{gtfs_id: db_id}` map, which is used to resolve these references for dependent tables (trips → routes, stop_times → trips & stops).
- Validation is **partial-acceptance**: invalid rows are collected and reported (`valid`/`invalid` counts per file) rather than failing the entire import.
- Empty CSV cells (`""`) are converted to `None` before Pydantic validation, since GTFS optional fields are typically left blank rather than omitted.
- Separate Pydantic schemas are used for input (raw GTFS data, e.g. `Route`) and output (API responses, e.g. `RouteOut`) — the same field can have a different type between the two (e.g. `route_id` is a `str` on input, an `int` foreign key on output for `Trip`/`StopTime`).

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

On startup, the app creates any missing database tables (`Base.metadata.create_all`) and ensures the MinIO bucket exists.

## Endpoints

- `POST /import` — accepts `slug` (form, text) and `zip_file` (form, file). Validates the zip, uploads it to MinIO, parses `routes.txt`/`stops.txt`/`trips.txt`/`stop_times.txt`, and writes valid rows to the database under a new snapshot. Returns per-file valid/invalid counts.
- `GET /snapshots/{snapshot_id}/download` — streams the original uploaded zip back from MinIO.
- `GET /routes?snapshot_id=...` — all routes for a given snapshot.
- `GET /stops?snapshot_id=...` — all stops for a given snapshot.
- `GET /trips?snapshot_id=...` — all trips for a given snapshot.

## Roadmap

- [ ] Parse and store `calendar.txt` (service calendar)
- [ ] Learn Alembic and replace `Base.metadata.create_all()` with proper migrations — the current approach only creates missing tables, it does not add new columns to existing ones
- [ ] Generalize `gtfs_parser.process_zip` using a `FILES_TO_PARSE` list + loop instead of one block per file
- [ ] Generalize `import_service.save_routes/save_stops/save_trips/save_stop_times` into a single reusable `save_items` function (using `.model_dump()`)
- [ ] Add field descriptions (`Field(description=...)`) to Pydantic schemas for better auto-generated docs
- [ ] Add cross-field validation where relevant (e.g. `arrival_time` vs `departure_time`)
- [ ] Tests (pytest, instead of manual testing via Postman)
