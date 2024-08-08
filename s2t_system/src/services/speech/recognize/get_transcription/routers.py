from typing import Union

from fastapi import APIRouter, HTTPException
from src.services.speech.recognize.get_transcription.schemas import (
    TaskBase,
    Transcription,
)
from src.tasks import celery

router = APIRouter(prefix='/transcription', tags=['Recognize'])


@router.get('/', response_model=Union[TaskBase, Transcription])
async def get_transcription(task_id: str) -> Transcription:
    try:
        task = celery.AsyncResult(task_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if task.ready():
        return task.get()
    else:
        return {'id': task.id, 'status': 'pending'}
