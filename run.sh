#!/usr/bin/env bash
# exit on error
set -o errexit

# These commands are run by Render on every new deployment.
python manage.py collectstatic --no-input
python manage.py migrate

# This command starts your live ASGI server for production.
gunicorn aidhamura.asgi:application -k uvicorn.workers.UvicornWorker
