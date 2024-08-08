from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from redis import asyncio as aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pages.router import router as router_pages
from src.config import CORS_ALLOWED_ORIGINS, REDIS_HOST
from src.services.auth.routers import router as router_auth
from src.services.speech.routers import router as router_speech


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(REDIS_HOST)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    title='S2T System',
    lifespan=lifespan
)


cors_allowed_origins = CORS_ALLOWED_ORIGINS.split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allowed_origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST','PATCH', 'PUT', 'DELETE', 'OPTIONS'],
    allow_headers=['*'],
)
app.include_router(router_auth)
app.include_router(router_speech)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router_pages)
