import uvicorn

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from src.services.speech.recognize.create_recognize.schemas import Transcription
from src.services.speech.recognize.create_recognize.service import recognize
from src.config import CORS_ALLOWED_ORIGINS
from src.services.auth.routers import router as auth_router
from src.services.speech.routers import router as speech_router

from ray import serve

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


@serve.deployment
@serve.ingress(app)
class MyFastAPIDeployment:
    @app.post('speech/recognize/send')
    def send_recognize(file: UploadFile) -> Transcription:
        transcription = recognize(file)
        return transcription

serve.run(MyFastAPIDeployment.bind())
