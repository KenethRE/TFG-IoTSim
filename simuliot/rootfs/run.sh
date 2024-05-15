#!/bin/bash
##!/usr/bin/with-contenv bashio

echo "Starting Simulator..."
echo "Starting Simulator Backend..."
python3 ./simuliot_backend/app.py &
sleep 1
echo "Starting Simulator Frontend..."
python3 ./manage.py runserver 8087