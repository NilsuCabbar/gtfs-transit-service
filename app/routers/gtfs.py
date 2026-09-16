from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services import import_service, gtfs_parser
import zipfile

router = APIRouter()

@router.post("/import")
async def import_gtfs(
    slug: str = Form(...),
    zip_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    zip_file.file.seek(0)
    if not zipfile.is_zipfile(zip_file.file):
        raise HTTPException(status_code=400, detail="Yüklenen dosya geçerli bir zip arşivi değil")
    
    dataset = import_service.get_or_create_dataset(db, slug)
    snapshot = import_service.create_snapshot(db, dataset.id, slug)
    import_service.upload_zip_to_minio(zip_file, snapshot)
    valid_routes, invalid_rows = gtfs_parser.process_zip(zip_file)
    import_service.save_routes(db, snapshot.id, valid_routes)

    
    return {"snapshot_id": snapshot.id, 
            "status": "uploaded",
            "valid_count": len(valid_routes),
            "invalid_count": len(invalid_rows)}