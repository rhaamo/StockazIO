#!/bin/bash -eux
python /app/api/manage.py collectstatic --noinput
gunicorn config.asgi:application -w ${STOCKAZIO_WEB_WORKERS-1} -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 ${GUNICORN_ARGS-}