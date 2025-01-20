import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    # Database
    DATABASE_URL: str = 'mysql+pymysql://root:admin@127.0.0.1:3306/mohre'
    FIRECRAWL_URL: str = "http://localhost:3002"
    REDIS_URL: str = "redis://localhost:6379"
    PORT: int = 3001
    
    
    class Config:
        env_file = ".env"
        
        
        
settings = Settings()