from fastapi import APIRouter
from src.services.speech.recognize.get_recognize.schemas import TaskBase

router = APIRouter(prefix='', tags=['Recognize'])

@router.get('/{task_id}')
async def get_recognize(task_id: int, response_model: TaskBase):
    return {"id": task_id, "status": "pending"}
