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

    # Schema ile onaylama
    valid_routes, invalid_routes, valid_stops, invalid_stops, valid_trips, invalid_trips, valid_stop_times, invalid_stop_times = gtfs_parser.process_zip(zip_file)

    # DB kaydetme 
    route_id_map = import_service.save_routes(db, snapshot.id, valid_routes)
    stop_id_map = import_service.save_stops(db, snapshot.id, valid_stops)
    trip_id_map = import_service.save_trips(db, snapshot.id, valid_trips, route_id_map)
    import_service.save_stop_times(db, snapshot.id, valid_stop_times, trip_id_map, stop_id_map)

    
    return {
        "snapshot_id": snapshot.id,
        "status": "uploaded",
        "routes": {"valid": len(valid_routes), "invalid": len(invalid_routes)},
        "stops": {"valid": len(valid_stops), "invalid": len(invalid_stops)},
        "trips": {"valid": len(valid_trips), "invalid": len(invalid_trips)},
        "stop_times": {"valid": len(valid_stop_times), "invalid": len(invalid_stop_times)}
    }