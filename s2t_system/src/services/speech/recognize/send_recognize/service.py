import whisper
from whisper import Whisper
from pathlib import Path

from fastapi import UploadFile
from src.services.speech.recognize.send_recognize.utils import handle_upload_file


def _get_transcription(file_path: Path):
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


def recognize(file: UploadFile):
    result = handle_upload_file(file, _get_transcription)
    return result
