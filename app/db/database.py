from sqlalchemy import create_engine # Veritabanına nasıl bağlanılacağı
from sqlalchemy.orm import sessionmaker  # Veritabanı session'ı oluşturmak için
from sqlalchemy.orm import declarative_base # Base'den türeyecek table oluyorlar
from app.core.config import settings

# DATABASE_URL = "postgresql://admin:admin123@localhost:5433/gtfs_db" # Eğer postgresql mesela bulutta çalışıyor olsaydı gerçek adresi/ip adresi gerekli olcaktı

engine = create_engine(settings.database_url) # Veritabanına bağlanmak için engine oluşturuyoruz
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()