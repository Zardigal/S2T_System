from fastapi import APIRouter
from src.services.speech.recognize.create_recognize.routers import router as create_recognize_router
from src.services.speech.recognize.get_recognize.routers import router as get_recognize_router

router = APIRouter(
    prefix='/speech',
)

router.include_router(create_recognize_router)
router.include_router(get_recognize_router)
