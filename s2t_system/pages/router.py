from typing import Annotated
from fastapi import APIRouter, Depends, File, Request
from fastapi.templating import Jinja2Templates

from src.services.speech.recognize.create_recognize.schemas import Transcription
from src.services.speech.recognize.create_recognize.routers import send_recognize



router = APIRouter(
    tags=['Pages'],
)

templates = Jinja2Templates(directory='templates')


@router.get('/')
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.post('/result')
async def send_recognize_page(request: Request, file: Annotated[bytes, File()]) -> Transcription:
    transcription = await send_recognize(file)
    text = transcription['text']
    words = transcription['words']
    return templates.TemplateResponse('result.html', {'request': request, 'text': text, 'words': words})
