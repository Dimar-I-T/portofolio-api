#!/usr/bin/env bash

python manage.py collectstatic --noinput
python manage.py migrate --noinput
exec gunicorn portofolio.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3