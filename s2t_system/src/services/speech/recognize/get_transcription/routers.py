from fastapi import APIRouter, Depends
from sqlalchemy import select
from src.database import get_async_session
from src.services.speech.recognize.get_transcription.schemas import Transcription
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.speech.recognize.models import transcription


router = APIRouter(prefix='/transcription', tags=['Recognize'])


@router.get('/')
async def get_transcription(transcription_id: int, session: AsyncSession = Depends(get_async_session)) -> Transcription:
    query = select(transcription).where(transcription.c.id == transcription_id)
    result = await session.execute(query)
    return result.first()
