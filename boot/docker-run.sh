#!/bin/bash

# 1. (Optional) Run database migrations here
# python manage.py migrate 



source /opt/venv/bin/activate

cd /app
RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

# Replace Gunicorn with this for development to enable auto-reload
exec fastapi dev main.py --host $RUN_HOST --port $RUN_PORT

# gunicorn -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT main:app 