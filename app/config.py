import os
from tortoise import generate_config

def get_db_config():
    return generate_config(
        TORTOISE_DB_URI,
        app_modules={"models": ["data.models", "aerich.models"]},
        connection_label="models",
    )
    
APP_ENV = os.getenv("APP_ENV")
TORTOISE_DB_URI = os.getenv("TORTOISE_DB", "asyncpg://postgres:postgres@database:5432/postgres")
TORTOISE_ORM = get_db_config()
REDIS_HOST = os.getenv("REDIS_HOST", "cache")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)