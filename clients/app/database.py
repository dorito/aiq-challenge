from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from tortoise import Tortoise, generate_config
from tortoise.contrib.fastapi import RegisterTortoise

from app.config import Config

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
  testing = getattr(app.state, "testing", None)
  if testing:
    generate_schemas = True
    _create_db = True
    db_uri = Config.TORTOISE_TEST_DB_URI
  else:
    generate_schemas = False
    _create_db = False
    db_uri = Config.TORTOISE_DB_URI
  config = generate_config(
        db_uri,
        app_modules={"models": ["data.models", "aerich.models"]},
        testing=testing,
        connection_label="models",
  )
  async with RegisterTortoise(
        app=app,
        config=config,
        generate_schemas=generate_schemas,
        _create_db=_create_db,
  ):
      yield
  if testing:
    await Tortoise._drop_databases()