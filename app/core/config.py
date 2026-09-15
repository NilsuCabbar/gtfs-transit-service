from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int

    minio_root_user: str
    minio_root_password: str
    minio_port: int
    minio_bucket_name: str = "gtfs-snapshots"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@localhost:{self.postgres_port}/{self.postgres_db}"

    @property
    def minio_endpoint(self) -> str:
        return f"localhost:{self.minio_port}"


settings = Settings()