#!/bin/bash

pythona manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput