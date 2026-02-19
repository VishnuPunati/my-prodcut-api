import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):

        self.API_PORT: int = int(os.getenv("API_PORT", 8000))

       
        self.DATABASE_URL: str = os.getenv("DATABASE_URL")
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")

      
        self.REDIS_HOST: str = os.getenv("REDIS_HOST")
        if not self.REDIS_HOST:
            raise ValueError("REDIS_HOST environment variable is required")

        self.REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

   
        self.CACHE_TTL_SECONDS: int = int(
            os.getenv("CACHE_TTL_SECONDS", 3600)
        )


settings = Settings()
