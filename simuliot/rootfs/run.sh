#!/usr/bin/with-contenv bashio


MQTT_BROKER_HOST=$(bashio::services mqtt "host")
MQTT_USER=$(bashio::services mqtt "username")
MQTT_PWD=$(bashio::services mqtt "password")
MQTT_BROKER_PORT=$(bashio::services mqtt "port")
DJANGO_LOG_LEVEL=DEBUG

export DJANGO_LOG_LEVEL
export MQTT_BROKER_HOST
export MQTT_USER
export MQTT_PWD
export MQTT_BROKER_PORT

echo "Starting Simulator..."
echo "Starting Simulator Backend..."
python3 ./simuliot_backend/app.py >> /simuliot.log &
sleep 1
echo "Starting Simulator Frontend..."
#gunicorn --bind 0.0.0.0:8087 simuliot_frontend.wsgi:application &

nginx -g "daemon off;error_log /simuliot_nginx_error.log debug;"