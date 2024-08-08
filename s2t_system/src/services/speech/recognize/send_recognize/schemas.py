from pydantic import BaseModel

class TaskBase(BaseModel):
    id: int
    status: str


class Word(BaseModel):
    startTime: str
    endTime: str
    word: str


class Transcription(BaseModel):
    words: list[Word]
    text: str
