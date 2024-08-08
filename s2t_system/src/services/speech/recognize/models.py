from sqlalchemy import MetaData, Table, Column, Integer, String, JSON

metadata =  MetaData()

transcription = Table(
    "transcription",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("text", String),
    Column("words", JSON),
)
