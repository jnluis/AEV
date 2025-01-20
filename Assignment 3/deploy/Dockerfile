FROM python:3.11

RUN apt update

RUN apt-get install libmagic1

RUN apt install nginx -y
COPY deploy/nginx/default /etc/nginx/sites-enabled/


WORKDIR /app
COPY app/ .

RUN python3 -m venv venv
RUN venv/bin/pip install --no-cache-dir uvicorn
RUN venv/bin/pip install --no-cache-dir -r requirements.txt

WORKDIR /deploy

COPY deploy/set_env.sh .
COPY deploy/entry.sh .
COPY deploy/start_web.sh .
COPY deploy/start_password_service.sh .

RUN chmod u+x set_env.sh
RUN chmod u+x entry.sh
RUN chmod u+x start_web.sh
RUN chmod u+x start_password_service.sh

WORKDIR /password-service
COPY password-service/ .

RUN python3 -m venv venv
RUN venv/bin/pip install --no-cache-dir -r requirements.txt

WORKDIR /deploy

EXPOSE 80

CMD ["/bin/bash", "/deploy/entry.sh"]
