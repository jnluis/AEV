#!/bin/bash

/usr/sbin/nginx

python3 manage.py makemigrations
python3 manage.py migrate

python3 -m uvicorn project.asgi:application --host 127.0.0.1 --port 8080 --reload --reload-include "*.html"
