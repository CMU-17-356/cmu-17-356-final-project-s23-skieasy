#!/bin/sh

python manage.py migrate
gunicorn --bind :8000 --workers 1 skieasy.wsgi
