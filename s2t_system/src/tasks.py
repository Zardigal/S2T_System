import whisper
from celery import Celery
from src.config import REDIS_HOST
from src.services.speech.recognize.send_recognize.utils import load_audio
from whisper import Whisper

celery = Celery('tasks', broker=REDIS_HOST, backend=REDIS_HOST)
celery.autodiscover_tasks(force=True)


@celery.task
def _recognize(file: str):
    model: Whisper = whisper.load_model("tiny")
    audio = load_audio(file)
    transcript = model.transcribe(
        word_timestamps=True,
        audio=audio
    )

    words_result: list = []
    for words in [segment['words'] for segment in transcript['segments']]:
        for word in words:
            words_result.append(
                {
                    "startTime": f"{float(word['start'])}s",
                    "endTime": f"{float(word['end'])}s",
                    "word": word['word']
                }
            )
    return {'words': words_result, 'text': transcript['text']}
