#!/bin/bash

PASS_SERVICE_PORT=8000
PASS_SERVICE_ADDR=127.0.0.1

export PASS_SERVICE_PORT
export PASS_SERVICE_ADDR   

# ./set_env.sh

# Django backend
./start_web.sh &

# Password service
./start_password_service.sh &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?