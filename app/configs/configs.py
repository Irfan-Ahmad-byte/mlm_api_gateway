from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv

class Configs(BaseSettings):
    """
    Configuration class to hold all the configurations for the application.
    """

    # Load environment variables from .env file
    load_dotenv(find_dotenv())

    # Database configuration
    MLM_SERVICE_BASE_URL: str
    MLM_SERVICE_API_KEY: str
    MLM_SERVICE_API_SECRET: str
    AUTH_BASE_URL: str
    AUTH_API_KEY: str
    AUTH_API_SECRET: str
    SHORTENER_BASE_URL: str
    SHORTENER_API_KEY: str
    SHORTENER_API_SECRET: str
    REDIS_URL: str = "redis://localhost:6379/0"
    # Other configurations can be added here

    # Example: API keys, secret keys, etc.
    model_config = {
        "extra": "allow",
        "env_file": ".env"
    }

settings = Configs()