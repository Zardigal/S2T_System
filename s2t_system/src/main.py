import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import CORS_ALLOWED_ORIGINS
from src.services.auth.routers import router as auth_router
from src.services.speech.routers import router as speech_router

app = FastAPI(
    title='S2T System'
)

cors_allowed_origins = CORS_ALLOWED_ORIGINS.split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router)
app.include_router(speech_router)
