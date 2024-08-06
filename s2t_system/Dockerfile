FROM python:3.9-slim

RUN mkdir /s2t_system

WORKDIR /s2t_system

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pip install pipenv
RUN pipenv install

RUN apt update && \
apt install \
ffmpeg \
-y

COPY . .

RUN chmod a+x docker/app.sh
