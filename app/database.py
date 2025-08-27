from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from tortoise.contrib.fastapi import RegisterTortoise

import app.config as Config

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
  generate_schemas = False
  _create_db = False
  db_config = Config.get_db_config()
  async with RegisterTortoise(
        app=app,
        config=db_config,
        generate_schemas=generate_schemas,
        _create_db=_create_db,
  ):
      yield