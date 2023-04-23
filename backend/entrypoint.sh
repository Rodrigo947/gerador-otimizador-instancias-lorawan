#!/bin/sh

python manage.py migrate
python manage.py createsuperuser --no-input --username admin
python manage.py runserver 0.0.0.0:$DJANGO_PORT