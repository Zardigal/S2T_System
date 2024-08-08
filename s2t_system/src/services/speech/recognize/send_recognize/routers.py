from typing import Union

from fastapi import APIRouter, HTTPException, UploadFile
from sqlalchemy import insert
from src.database import async_session_maker
from src.services.speech.recognize.models import transcription as transcription_model
from src.services.speech.recognize.send_recognize.schemas import TaskBase, Transcription
from src.services.speech.recognize.send_recognize.service import recognize

router = APIRouter(prefix='/recognize', tags=['Recognize'])

audio_types = [
    'audio/basic',
    'audio/mpeg',
    'audio/mp4',
]


@router.post('', response_model=Union[TaskBase, Transcription])
async def send_recognize(file: UploadFile):
    async with async_session_maker() as session: 
        if file.content_type not in audio_types:
            raise HTTPException(400, detail="Invalid audio type")
        transcription_result = recognize(file)
        if "status" in transcription_result:
            return transcription_result
        valid_result = Transcription.model_validate(transcription_result)
        stmt = insert(transcription_model).values(**valid_result.model_dump())
        await session.execute(stmt)
        await session.commit()

        return valid_result.model_dump()
