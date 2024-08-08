FROM python:3.9-slim

RUN mkdir /s2t_system

WORKDIR /s2t_system

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt 
RUN apt update && \
apt install \
ffmpeg \
redis-server\
-y

COPY . .

RUN chmod a+x docker/app.sh
