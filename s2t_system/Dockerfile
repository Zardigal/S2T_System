FROM python:3.9-slim

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pip install pipenv
RUN pipenv install --deploy --system

RUN sudo apt update && sudo apt install ffmpeg -y

COPY . .


CMD ["python", "main.py"]