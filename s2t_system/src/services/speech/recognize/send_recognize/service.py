import time

from fastapi import UploadFile
from src.tasks import celery, _recognize


def recognize(file: UploadFile):
    task = _recognize.delay(file.file.read())
    time.sleep(3)
    task = celery.AsyncResult(task.id)
    if task.ready():
        return task.get()
    else:
        return {'id': task.id, 'status': 'pending'}
