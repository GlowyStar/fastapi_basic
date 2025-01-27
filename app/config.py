from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
from typing import Optional


load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str = Field(..., description="Database host")
    DB_PORT: int = Field(..., description="Database port")
    DB_NAME: str = Field(..., description="Database name")
    DB_USER: str = Field(..., description="Database user")
    DB_PASSWORD: str = Field(..., description="Database password")

    # post-init models
    DATABASE_URL: Optional[str] = None

    def model_post_init(self, __context: dict = None):
        self.DATABASE_URL = (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    class Config:
        env_file = ".env"


settings = Settings()
