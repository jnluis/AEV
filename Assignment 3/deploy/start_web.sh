#!/bin/bash

cd /app

python -m venv venv
source venv/bin/activate

mkdir -p /app/database
chown -R root:root /app/database

python manage.py makemigrations
python manage.py migrate

/usr/sbin/nginx
python3 -m uvicorn project.asgi:application --host 127.0.0.1 --port 8080