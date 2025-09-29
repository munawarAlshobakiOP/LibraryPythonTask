from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str
   
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
