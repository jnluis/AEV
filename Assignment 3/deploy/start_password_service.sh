#!/bin/bash

cd /password-service

python -m venv venv
source venv/bin/activate

echo "============================================================================================"
echo
echo
echo
echo $PASS_SERVICE_ADDR:$PASS_SERVICE_PORT
echo
echo
echo
echo "============================================================================================"

# Prod mode
fastapi run --host $PASS_SERVICE_ADDR --port $PASS_SERVICE_PORT