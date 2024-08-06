FROM python:3.9-slim

RUN mkdir /s2t_system

WORKDIR /s2t_system

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN apt install python3-pip -y
RUN pip install pipenv
RUN pipenv install --deploy --system

RUN apt update && \
apt install \
ffmpeg \
-y

COPY . .

RUN chmod a+x docker/app.sh

# CMD [ "gunicorn" , "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000" ]