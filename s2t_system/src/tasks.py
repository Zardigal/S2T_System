from pathlib import Path

import whisper
from whisper import Whisper
from celery import Celery, Task
from src.config import REDIS_HOST

celery = Celery('tasks', broker=REDIS_HOST, backend=REDIS_HOST)
celery.autodiscover_tasks(force=True)


class GetTranscriptionTaskBase(Task):
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        # Delete the temp file
        tmp_path = Path(kwargs['file_path'])
        tmp_path.unlink()
        return super().after_return(status, retval, task_id, args, kwargs, einfo)

@celery.task(base=GetTranscriptionTaskBase)
def get_transcription(file_path: str):
    model: Whisper = whisper.load_model("tiny")
    audio = whisper.load_audio(file_path)
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
