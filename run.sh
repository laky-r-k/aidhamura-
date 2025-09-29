
#!/usr/bin/env bash
# exit on error
set -o errexit

# This command tells Django to gather all static files (CSS, JS, images)
# from your apps into the single STATIC_ROOT directory for serving.
echo "Collecting static files..."
python manage.py collectstatic --no-input

# This command applies any pending database migrations to your live
# PostgreSQL database, ensuring its schema is up-to-date.
echo "Applying database migrations..."
python manage.py migrate

# This is the command that starts your live production server.
# It uses Gunicorn to manage Uvicorn workers, which run your ASGI application.
echo "Starting Gunicorn..."
gunicorn aidhamura.asgi:application -k uvicorn.workers.UvicornWorker