from fastapi import APIRouter, Form, Request, UploadFile
from fastapi.templating import Jinja2Templates
from src.services.speech.recognize.get_transcription.routers import get_transcription
from src.services.speech.recognize.send_recognize.routers import send_recognize
from src.services.speech.recognize.send_recognize.schemas import Transcription

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
    if "status" in transcription:
        return templates.TemplateResponse('index.html', {'request': request, 'id': transcription['id'], 'status': transcription['status']})
    context = {'request': request, 'text': transcription['words'], 'words': transcription['text']}
    return templates.TemplateResponse('result.html', context=context)


@router.get('/result')
async def get_transcription_page(request: Request, task_id: str) -> Transcription:
    transcription = await get_transcription(task_id)
    if "status" in transcription:
        return templates.TemplateResponse('index.html', {'request': request, 'id': task_id, 'status': transcription['status']})
    context = {'request': request, 'text': transcription['text'], 'words': transcription['words']}
    return templates.TemplateResponse('result.html', context=context)
