from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

import redis.asyncio as aioredis

import app.config as Config

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
  redis = await aioredis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB)
  app.cache = redis
  yield
  await app.cache.aclose()
