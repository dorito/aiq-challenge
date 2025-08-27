from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

import app.config as Config

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
  is_test = True
  if not is_test:
      generate_schemas = False
      _create_db = False
  else:
      generate_schemas = True
      _create_db = True
  db_config = Config.get_db_config(is_test=is_test)
  async with RegisterTortoise(
        app=app,
        config=db_config,
        generate_schemas=generate_schemas,
        _create_db=_create_db,
  ):
      yield
  if is_test:
    await Tortoise._drop_databases()