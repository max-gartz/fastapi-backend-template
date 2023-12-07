#!/bin/bash
DEFAULT_WORKERS="$(nproc 2>/dev/null || sysctl -n hw.ncpu)"
gunicorn app.main:root \
 --workers ${DEFAULT_WORKERS:-${WORKERS}} \
 --worker-class uvicorn.workers.UvicornWorker \
 --bind 0.0.0.0:8080 \
 --timeout 0