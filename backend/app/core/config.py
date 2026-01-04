from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional, Union
from pydantic import field_validator


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
    
    # Clerk Authentication
    CLERK_SECRET_KEY: Optional[str] = None
    CLERK_PUBLISHABLE_KEY: Optional[str] = None
    
    # Admin Dashboard
    ADMIN_PASSWORD: str = "admin123"  # À changer en production !
    
    # CORS - Accepte string (ex: "*") ou liste séparée par virgules
    CORS_ORIGINS: Union[str, list[str]] = "http://localhost:3000,http://localhost:8081,http://10.0.2.2:8000"
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS depuis string ou liste"""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # Si c'est "*", retourner ["*"]
            if v.strip() == "*":
                return ["*"]
            # Sinon, split par virgule
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()

