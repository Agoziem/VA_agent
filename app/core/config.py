from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL: str = REDIS_URL
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "your-google-api-key")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "your-groq-api-key")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "your-tavily-api-key")
    LANGSMITH_TRACING: bool = os.getenv("LANGSMITH_TRACING", "false").lower() in ("true", "1", "t")
    LANGSMITH_ENDPOINT: str = os.getenv("LANGSMITH_ENDPOINT", "https://api.langsmith.com")
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "your-langsmith-api-key")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "default-project")


    class Config:
        env_file = ".env"  # Load from .env file
        env_file_encoding = "utf-8"


# Create an instance of settings
settings = Settings()
