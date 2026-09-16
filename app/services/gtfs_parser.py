import zipfile
from fastapi import UploadFile
from sqlalchemy.orm import Session
import csv
import io
from app.schemas.route import Route
from pydantic import ValidationError


def process_zip(zip_file: UploadFile):
    zip_file.file.seek(0) # MinIO'ya yüklerken stream yüketiliyor imleci başa al
    valid_routes = []
    invalid_rows = []

    with zipfile.ZipFile(zip_file.file) as z:
        print(z.namelist())

        with z.open("routes.txt") as f:
            text_file = io.TextIOWrapper(f, encoding="utf-8")
            reader = csv.DictReader(text_file)
            for row in reader:
                try:
                    route = Route(**row)
                    valid_routes.append(route)
                except ValidationError as e:
                    invalid_rows.append({"row": row, "error": str(e)})

    return valid_routes, invalid_rows