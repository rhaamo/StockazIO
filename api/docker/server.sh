#!/bin/bash -eux
python /app/api/manage.py collectstatic --noinput
python /app/api/manage.py migrate
cd /app/api/
gunicorn --log-file=- --worker-tmp-dir /dev/shm config.asgi:application -w ${STOCKAZIO_WEB_WORKERS-2} --threads ${STOCKAZIO_WEB_THREADS-4} -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 ${GUNICORN_ARGS-}
