# app/core/config.py
import os
from pydantic import BaseSettings
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "CostByte"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "costbyte-secret-key-2023")
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./costbyte.db")
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "https://costbyte.co.za"]
    
    # Email settings
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    
    # AI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    
    # Social media API keys
    LINKEDIN_API_KEY: str = os.getenv("LINKEDIN_API_KEY", "")
    FACEBOOK_API_KEY: str = os.getenv("FACEBOOK_API_KEY", "")
    TWITTER_API_KEY: str = os.getenv("TWITTER_API_KEY", "")
    
    # Monitoring settings
    MONITORING_INTERVAL: int = int(os.getenv("MONITORING_INTERVAL", 300))  # 5 minutes
    
    class Config:
        case_sensitive = True

settings = Settings()
