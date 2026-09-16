import zipfile
from fastapi import UploadFile
from sqlalchemy.orm import Session
import csv
import io
from app.schemas.route import Route
from app.schemas.stop import Stop
from app.schemas.trip import Trip
from app.schemas.stop_time import StopTime
from pydantic import ValidationError


def process_zip(zip_file: UploadFile):
    zip_file.file.seek(0) # MinIO'ya yüklerken stream yüketiliyor imleci başa al
    valid_routes = []
    invalid_routes = []
    valid_stops = []
    invalid_stops = []
    valid_trips = []
    invalid_trips = []
    valid_stop_times = []
    invalid_stop_times = []

    with zipfile.ZipFile(zip_file.file) as z:

       # ROUTES doğrulama
       valid_routes, invalid_routes = parse_csv_from_zip(z, "routes.txt", Route)
       # STOPS doğrulama
       valid_stops, invalid_stops = parse_csv_from_zip(z, "stops.txt", Stop)
       # TRIPS doğrulama
       valid_trips, invalid_trips = parse_csv_from_zip(z, "trips.txt", Trip)   
       # STOP TIMES doğrulama
       valid_stop_times, invalid_stop_times = parse_csv_from_zip(z, "stop_times.txt", StopTime)    
           

    return valid_routes, invalid_routes, valid_stops, invalid_stops, valid_trips, invalid_trips, valid_stop_times, invalid_stop_times

def parse_csv_from_zip(z: zipfile.ZipFile, filename: str, schema_class):
    valid = []
    invalid = []

    with z.open(filename) as f:
      text_file = io.TextIOWrapper(f, encoding="utf-8")
      reader = csv.DictReader(text_file)
      for row in reader:
          row = {k: (v if v!="" else None)for k, v in row.items()} # None olanları None yapıyoruz "" yapmaktansa. Yoksa hata 
          try:
              item = schema_class(**row)
              valid.append(item)
          except ValidationError as e:
              invalid.append({"row": row, "error": str(e)})

    return valid, invalid
