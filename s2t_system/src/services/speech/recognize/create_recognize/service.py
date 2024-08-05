import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable

import whisper
from fastapi import UploadFile
from whisper import Whisper


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def handle_upload_file(
    upload_file: UploadFile, handler: Callable[[Path], dict]
) -> dict:
    tmp_path = save_upload_file_tmp(upload_file)
    try:
        return handler(file_path=tmp_path)  # Do something with the saved temp file
    finally:
        tmp_path.unlink()  # Delete the temp file


def _get_recognize(file_path: Path):
    model: Whisper = whisper.load_model("base")
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


def recognize(file: UploadFile):
    result = handle_upload_file(file, _get_recognize)
    return result
