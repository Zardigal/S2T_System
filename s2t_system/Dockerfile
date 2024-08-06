FROM python:3.9-slim

RUN mkdir /s2t_system

WORKDIR /s2t_system

# COPY Pipfile Pipfile
# COPY Pipfile.lock Pipfile.lock
RUN apt update && \
apt install \
ffmpeg \
-y
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
COPY Pipfile* /app/
COPY Pipfile.lock* /app/
RUN cd /app && pipenv install


COPY . .

RUN chmod a+x docker/app.sh
