from fastapi import APIRouter, HTTPException, UploadFile
from sqlalchemy import insert
from src.services.speech.recognize.send_recognize.schemas import Transcription
from src.services.speech.recognize.send_recognize.service import recognize
from src.services.speech.recognize.models import transcription as transcription_model
from src.database import async_session_maker

router = APIRouter(prefix='/recognize', tags=['Recognize'])

audio_types = [
    'audio/basic',
    'audio/mpeg',
    'audio/mp4',
]


@router.post('')
async def send_recognize(file: UploadFile) -> Transcription:
    async with async_session_maker() as session: 
        if file.content_type not in audio_types:
            raise HTTPException(400, detail="Invalid audio type")
        transcription_result = Transcription.model_validate(recognize(file))
        stmt = insert(transcription_model).values(**transcription_result.model_dump())
        await session.execute(stmt)
        await session.commit()

        return transcription_result.model_dump()
