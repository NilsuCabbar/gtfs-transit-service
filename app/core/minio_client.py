from minio import Minio
from app.core.config import settings

minio_client = Minio(
    endpoint=settings.minio_endpoint,
    access_key=settings.minio_root_user,
    secret_key=settings.minio_root_password,
    secure=False
)