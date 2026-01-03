from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "NutriAI API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/nutriai_db"
    
    # OpenRouter
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_MODEL: str = "openai/gpt-3.5-turbo"
    
    # CORS - Si "*" dans la liste, permet toutes les origines
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8081", "http://10.0.2.2:8000"]
    
    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()

