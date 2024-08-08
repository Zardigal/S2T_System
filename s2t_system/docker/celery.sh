#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery --app=src.tasks:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    celery --app=src.tasks:celery flower
fi
