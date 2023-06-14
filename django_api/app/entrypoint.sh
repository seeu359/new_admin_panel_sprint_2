#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done

echo "PostgreSQL started"

python3 manage.py collectstatic --no-input -v 2
python3 manage.py migrate
python3 sqlite_to_postgres/load_data.py

uwsgi --ini uwsgi.ini