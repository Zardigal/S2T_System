from typing import Annotated

from fastapi import APIRouter, File
from src.services.speech.recognize.create_recognize.schemas import Transcription
from src.services.speech.recognize.create_recognize.service import recognize

router = APIRouter(prefix='/recognize', tags=['Recognize'])

@router.post('')
def send_recognize(file: Annotated[bytes, File()]) -> Transcription:
    transcription = recognize(file)
    return transcription
