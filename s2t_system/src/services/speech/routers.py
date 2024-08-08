from fastapi import APIRouter
from src.services.speech.recognize.send_recognize.routers import router as router_send_recognize
from src.services.speech.recognize.get_transcription.routers import router as router_get_transcription

router = APIRouter(
    prefix='/speech',
)

router.include_router(router_send_recognize)
router.include_router(router_get_transcription)
