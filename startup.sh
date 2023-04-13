#!/bin/sh

gunicorn --bind :8000 --workers 1 skieasy.wsgi
