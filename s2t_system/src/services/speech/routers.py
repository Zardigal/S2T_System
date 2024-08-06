from fastapi import APIRouter
from src.services.speech.recognize.create_recognize.routers import router as router_create_recognize
from src.services.speech.recognize.get_recognize.routers import router as router_get_recognize

router = APIRouter(
    prefix='/speech',
)

router.include_router(router_create_recognize)
router.include_router(router_get_recognize)
