from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(extra='ignore')
    DB_HOST: str = Field(..., description="Database host")
    DB_PORT: int = Field(..., description="Database port")
    DB_NAME: str = Field(..., description="Database name")
    DB_USER: str = Field(..., description="Database user")
    DB_PASSWORD: str = Field(..., description="Database password")

    # post-init models
    DATABASE_URL: Optional[str] = None

    def model_post_init(self, __context: dict = None):
        self.DATABASE_URL = (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings(_env_file='.env')

print(settings.DB_HOST)
