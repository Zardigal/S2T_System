from fastapi import APIRouter, Depends, Request, UploadFile, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.services.speech.recognize.send_recognize.schemas import Transcription
from src.services.speech.recognize.send_recognize.routers import send_recognize
from src.services.speech.recognize.get_transcription.routers import get_transcription



router = APIRouter(
    tags=['Pages'],
)

templates = Jinja2Templates(directory='templates')


@router.get('/')
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.post('/')
async def send_recognize_page(request: Request, file: UploadFile = Form(...)) -> Transcription:
    transcription = await send_recognize(file)
    text = transcription['text']
    words = transcription['words']
    return templates.TemplateResponse('result.html', {'request': request, 'text': text, 'words': words})


# @router.get('/result')
# def get_transcription_page(request: Request, transcription: Depends(get_transcription)):
#     return templates.TemplateResponse('result.html', {'request': request})
