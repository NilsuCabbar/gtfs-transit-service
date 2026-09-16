from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.core.minio_client import minio_client
from app.core.config import settings
from app.models.dataset import Dataset
from app.models.snapshot import Snapshot
from app.models.route import Route as RouteModel
from app.schemas.route import Route as RouteSchema
from app.models.stop import Stop as StopModel
from app.schemas.stop import Stop as StopSchema
from app.models.trip import Trip as TripModel
from app.schemas.trip import Trip as TripSchema
from app.models.stop_time import StopTime as StopTimeModel
from app.schemas.stop_time import StopTime as StopTimeSchema

BUCKET_NAME = settings.minio_bucket_name

def get_or_create_dataset(db: Session, slug: str) -> Dataset:
    dataset = db.query(Dataset).filter(Dataset.slug == slug).first()
    if dataset is None:
        dataset = Dataset(slug=slug, display_name=slug.upper())
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
    return dataset

def create_snapshot(db: Session, dataset_id: int, slug: str):
    snapshot = Snapshot(dataset_id = dataset_id, minio_object_path = None)
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    snapshot.minio_object_path = f"{slug}/snapshot_{snapshot.id}.zip"
    db.commit()
    return snapshot

def upload_zip_to_minio(zip_file: UploadFile, snapshot: Snapshot):
    zip_file.file.seek(0)
    minio_client.put_object(
        bucket_name=BUCKET_NAME,
        object_name=snapshot.minio_object_path,
        data=zip_file.file,
        length=zip_file.size,
        content_type="application/zip"
    )

# DB kaydetme servisleri gibi burası

def save_routes(db: Session, snapshot_id: int, valid_routes: list[RouteSchema]) -> dict:
    route_id_map = {}
    for route in valid_routes:
        db_route = RouteModel(
            snapshot_id=snapshot_id,
            route_id=route.route_id,
            route_short_name=route.route_short_name,
            route_long_name=route.route_long_name,
            agency_id=route.agency_id,
            route_type=route.route_type
        )
        db.add(db_route)
        db.flush()  # henüz commit değil, ama db_route.id'yi şimdiden almamızı sağlar
        route_id_map[route.route_id] = db_route.id
    db.commit()
    return route_id_map

def save_stops(db: Session, snapshot_id: int, valid_stops: list[StopSchema]) -> dict:
    stop_id_map = {}
    for stop in valid_stops:
        db_stop = StopModel(
            snapshot_id=snapshot_id,
            stop_id=stop.stop_id,
            stop_name=stop.stop_name,
            stop_lat=stop.stop_lat,
            stop_lon=stop.stop_lon,
            wheelchair_boarding=stop.wheelchair_boarding,
            location_type=stop.location_type
        )
        db.add(db_stop)
        db.flush()
        stop_id_map[stop.stop_id] = db_stop.id
    db.commit()
    return stop_id_map

def save_trips(db: Session, snapshot_id: int, valid_trips: list[TripSchema], route_id_map: dict) -> dict:
    trip_id_map = {}
    for trip in valid_trips:
        db_trip = TripModel(
            snapshot_id=snapshot_id,
            route_id=route_id_map[trip.route_id], # Foreign key unique olamadığından id ile buluyoruz
            service_id=trip.service_id,
            trip_id=trip.trip_id,
            trip_headsign=trip.trip_headsign,
            direction_id=trip.direction_id,
            shape_id=trip.shape_id
        )
        db.add(db_trip)
        db.flush()
        trip_id_map[trip.trip_id] = db_trip.id
    db.commit()
    return trip_id_map

def save_stop_times(db: Session, snapshot_id: int, valid_stop_times: list[StopTimeSchema], trip_id_map: dict, stop_id_map: dict) -> None:
    for stop_time in valid_stop_times:
        db_stoptime = StopTimeModel(
            snapshot_id=snapshot_id,
            trip_id=trip_id_map[stop_time.trip_id],
            arrival_time=stop_time.arrival_time,
            departure_time=stop_time.departure_time,
            stop_id=stop_id_map[stop_time.stop_id],
            stop_sequence=stop_time.stop_sequence,
            pickup_type=stop_time.pickup_type,
            drop_off_type=stop_time.drop_off_type,
            shape_dist_traveled=stop_time.shape_dist_traveled
        )
        db.add(db_stoptime)
    db.commit()

def get_snapshot(db: Session, snapshot_id: int) -> Snapshot:
    snapshot = db.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Snapshot is not found") # Mimari açıdan temiz değilmiş ama pratik ve yeterli şu an kullanmak için
    return snapshot