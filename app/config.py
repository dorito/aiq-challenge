import os
from tortoise import generate_config

def get_db_config(is_test: bool = False):
    return generate_config(
        TORTOISE_TEST_DB_URI if is_test else TORTOISE_DB_URI,
        testing=is_test,
        app_modules={"models": ["data.models", "aerich.models"]},
        connection_label="models",
    )
    
APP_ENV = os.getenv("APP_ENV")
TORTOISE_DB_URI = os.getenv("TORTOISE_DB", "asyncpg://postgres:postgres@database:5432/postgres")
TORTOISE_TEST_DB_URI = os.getenv("TORTOISE_TEST_DB", "sqlite://:memory:")
TORTOISE_ORM = get_db_config()
REDIS_HOST = os.getenv("REDIS_HOST", "cache")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)