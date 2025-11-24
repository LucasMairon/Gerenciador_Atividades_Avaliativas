#!/bin/sh

set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Waiting for Postgres Database Startup ($POSTGRES_HOST:$POSTGRES_PORT)..."
  sleep 3
done

echo "Postgres Database Started at ($POSTGRES_HOST:$POSTGRES_PORT)"

python manage.py collectstatic --noinput
python manage.py migrate
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3