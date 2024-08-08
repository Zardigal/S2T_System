import time

from fastapi import UploadFile
from src.services.speech.recognize.send_recognize.utils import handle_upload_file
from src.tasks import celery, get_transcription


def recognize(file: UploadFile):
    task = handle_upload_file(file, get_transcription)
    time.sleep(3)
    task = celery.AsyncResult(task.id)
    if task.ready():
        return task.get()
    else:
        return {'id': task.id, 'status': 'pending'}
