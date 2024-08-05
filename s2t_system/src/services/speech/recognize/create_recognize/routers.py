from typing import Annotated

from fastapi import APIRouter, UploadFile
from src.services.speech.recognize.create_recognize.schemas import TaskBase, Transcription
from src.services.speech.recognize.create_recognize.service import recognize

router = APIRouter(prefix='/recognize', tags=['Recognize'])

@router.post('')
def send_recognize(file: UploadFile) -> Transcription:
    transcription = recognize(file)
    return transcription
