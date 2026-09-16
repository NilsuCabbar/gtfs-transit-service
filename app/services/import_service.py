from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.core.minio_client import minio_client
from app.core.config import settings
from app.models.dataset import Dataset
from app.models.snapshot import Snapshot
from app.models.route import Route as RouteModel
from app.schemas.route import Route as RouteSchema

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

def save_routes(db: Session, snapshot_id: int, valid_routes: list[RouteSchema]) -> None:
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
    db.commit()
