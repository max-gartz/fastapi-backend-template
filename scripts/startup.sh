#!/bin/bash
echo "Running startup script."
gunicorn app.main:root \
 --workers ${APP_WORKERS:-1} \
 --worker-class uvicorn.workers.UvicornWorker \
 --bind ${APP_HOST:-0.0.0.0}:${APP_PORT:-8080} \
 --timeout ${APP_TIMEOUT:-0} \
 --access-logfile - \
 --logger-class app.main.CustomGunicornLogger