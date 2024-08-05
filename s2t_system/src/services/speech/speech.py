# from pydantic import BaseModel
# from sqlalchemy import create_engine
# import psycopg2

# DATABASE_URL = "postgresql://postgres:postgres@postgresserver/db"

# engine = create_engine(
#     DATABASE_URL
# )


# class Word(BaseModel):
#     startTime: str
#     endTime: str
#     word: str


# class Speech(BaseModel):
#     words: list[Word]
#     text: str
