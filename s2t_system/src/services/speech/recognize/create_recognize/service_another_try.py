##########################
# With tmp file without ray serve

# import shutil
# import whisper
# from whisper import Whisper
# from pathlib import Path
# from tempfile import NamedTemporaryFile
# from typing import Callable
# from fastapi import UploadFile


# def save_upload_file_tmp(upload_file: UploadFile) -> Path:
#     try:
#         suffix = Path(upload_file.filename).suffix
#         with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#             shutil.copyfileobj(upload_file.file, tmp)
#             tmp_path = Path(tmp.name)
#     finally:
#         upload_file.file.close()
#     return tmp_path


# def handle_upload_file(
#     upload_file: UploadFile, handler: Callable[[Path], dict]
# ) -> dict:
#     tmp_path = save_upload_file_tmp(upload_file)
#     try:
#         return handler(file_path=tmp_path)
#     finally:
#         tmp_path.unlink()  # Delete the temp file


# def _get_recognize(file_path: Path):
#     model: Whisper = whisper.load_model("tiny")
#     audio = whisper.load_audio(file_path)
#     transcript = model.transcribe(
#         word_timestamps=True,
#         audio=audio
#     )

#     words_result: list = []
#     for words in [segment['words'] for segment in transcript['segments']]:
#         for word in words:
#             words_result.append(
#                 {
#                     "startTime": f"{float(word['start'])}s",
#                     "endTime": f"{float(word['end'])}s",
#                     "word": word['word']
#                 }
#             )
#     return {'words': words_result, 'text': transcript['text']}


# def recognize(file: UploadFile):
#     result = handle_upload_file(file, _get_recognize)
#     return result


##########################
# With bytes file in memory #
# import ffmpeg
# import numpy as np
# import whisper
# from typing import Annotated, Optional
# from ray import serve
# from fastapi import File, APIRouter
# from ray.serve.handle import DeploymentHandle

# from src.services.speech.recognize.create_recognize.schemas import Transcription


# router = APIRouter(prefix='/recognize', tags=['Recognize'])

# SAMPLE_RATE = 16000


# @router.post('')
# async def send_recognize(file: Annotated[bytes, File()]) -> Transcription:
#     result = await handle.remote(file)
#     return result


# def load_audio(file_bytes: bytes, sr: int = 16_000) -> np.ndarray:
#     """
#     Use file's bytes and transform to mono waveform, resampling as necessary
#     Parameters
#     ----------
#     file: bytes
#         The bytes of the audio file
#     sr: int
#         The sample rate to resample the audio if necessary
#     Returns
#     -------
#     A NumPy array containing the audio waveform, in float32 dtype.
#     """
#     try:
#         # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
#         # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
#         out, _ = (
#             ffmpeg.input('pipe:', threads=0)
#             .output("pipe:", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
#             .run_async(pipe_stdin=True, pipe_stdout=True)
#         ).communicate(input=file_bytes)

#     except ffmpeg.Error as e:
#         raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

#     return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


# @serve.deployment(max_ongoing_requests=2, num_replicas=1, ray_actor_options={"num_cpus": 0.4, "num_gpus": 0.4})
# class Recognizer:
#     def __init__(self):
#         self.model = whisper.load_model("tiny")

#     def recognize(self, file: Annotated[bytes, File()]) -> dict:
#         text: Optional[str]
#         words_result: list = []

#         audio = load_audio(file=file)
#         transcript = self.model.transcribe(
#             word_timestamps=True,
#             audio=audio
#         )
#         text = transcript['text']
#         for words in [segment['words'] for segment in transcript['segments']]:
#             for word in words:
#                 words_result.append(
#                     {
#                         "startTime": f"{float(word['start'])}s",
#                         "endTime": f"{float(word['end'])}s",
#                         "word": word['word']
#                     }
#                 )

#         if not text or words_result:
#             return {'words': [], 'text': 'No one word'}

#         return {'words': words_result, 'text': text}

#     async def __call__(self, file: Annotated[bytes, File()]) -> dict:
#         return self.recognize(file)


# recognizer_app = Recognizer.bind()
# handle: DeploymentHandle = serve.run(recognizer_app)


###################
# With temp file #

# import shutil
# import whisper
# from pathlib import Path
# from tempfile import NamedTemporaryFile
# from typing import Callable, Optional
# from fastapi import UploadFile, APIRouter
# from ray import serve
# from ray.serve.handle import DeploymentHandle

# from src.services.speech.recognize.create_recognize.schemas import Transcription


# router = APIRouter(prefix='/recognize', tags=['Recognize'])

# @router.post('')
# async def send_recognize(file: UploadFile) -> Transcription:
#     transcription = handle.remote(file)
#     result = await transcription
#     return result


# def save_upload_file_tmp(upload_file: UploadFile) -> Path:
#     try:
#         suffix = Path(upload_file.filename).suffix
#         with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#             shutil.copyfileobj(upload_file.file, tmp)
#             tmp_path = Path(tmp.name)
#     finally:
#         upload_file.file.close()
#     return tmp_path


# def handle_upload_file(
#     upload_file: UploadFile, handler: Callable[[Path], dict]
# ) -> dict:
#     tmp_path = save_upload_file_tmp(upload_file)
#     try:
#         return handler(file_path=tmp_path)  # Do something with the saved temp file
#     finally:
#         tmp_path.unlink()  # Delete the temp file


# @serve.deployment(max_ongoing_requests=2, num_replicas=1, ray_actor_options={"num_cpus": 0.4, "num_gpus": 0.4})
# class Recognizer:
#     def __init__(self):
#         self.model = whisper.load_model("tiny")

#     def recognize(self, file: UploadFile) -> dict:
#         text: Optional[str]
#         words_result: list = []

#         audio = whisper.load_audio(file)
#         transcript = self.model.transcribe(
#             word_timestamps=True,
#             audio=audio
#         )

#         text = transcript['text']
#         words_result: list = []

#         for words in [segment['words'] for segment in transcript['segments']]:
#             for word in words:
#                 words_result.append(
#                     {
#                         "startTime": f"{float(word['start'])}s",
#                         "endTime": f"{float(word['end'])}s",
#                         "word": word['word']
#                     }
#                 )

#         if not text or words_result:
#             return {'words': [], 'text': 'No one word'}

#         return {'words': words_result, 'text': text}

#     async def __call__(self, file: UploadFile) -> dict:
#         return self.recognize(file)


# recognizer_app = Recognizer.bind()
# handle: DeploymentHandle = serve.run(recognizer_app)
