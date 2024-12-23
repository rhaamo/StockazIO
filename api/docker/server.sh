#!/bin/bash -eux
/venv/bin/python /app/api/manage.py migrate
cd /app/api/
/venv/bin/python /app/api/manage.py collectstatic --noinput
/venv/bin/gunicorn --log-file=- --worker-tmp-dir /dev/shm config.asgi:application -w ${STOCKAZIO_WEB_WORKERS-2} --threads ${STOCKAZIO_WEB_THREADS-4} -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 ${GUNICORN_ARGS-}
