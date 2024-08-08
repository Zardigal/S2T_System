FROM python:3.9-slim

RUN mkdir /s2t_system

WORKDIR /s2t_system

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt 
RUN apt update && \
apt install \
ffmpeg \
-y
RUN apt-get install redis-server -y
RUN service redis-server start

COPY . .

RUN chmod a+x docker/app.sh
