from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.minio_client import minio_client
from app.core.config import settings
from app.routers.gtfs import router
from app.db.database import engine, Base 
import app.models

BUCKET_NAME = settings.minio_bucket_name


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Başlangıçta çalışacak kod ---
    Base.metadata.create_all(bind=engine)

    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)
    
    yield  # <-- uygulama burada çalışmaya devam ediyor, istekleri karşılıyor
    
    # --- Kapanırken çalışacak kod (şimdilik boş, ileride lazım olabilir) ---

app = FastAPI(lifespan=lifespan)

app.include_router(router)

