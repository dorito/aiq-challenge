import os

class Config:
    TORTOISE_DB_URI = os.getenv("TORTOISE_DB", "sqlite://db.sqlite3")
    TORTOISE_TEST_DB_URI = os.getenv("TORTOISE_TEST_DB", "sqlite://:memory:")
