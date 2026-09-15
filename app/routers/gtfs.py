from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services import import_service

router = APIRouter()

@router.post("/import")
async def import_gtfs(
    slug: str = Form(...),
    zip_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    dataset = import_service.get_or_create_dataset(db, slug)
    snapshot = import_service.create_snapshot(db, dataset.id, slug)
    import_service.upload_zip_to_minio(zip_file, snapshot)
    
    return {"snapshot_id": snapshot.id, "status": "uploaded"}