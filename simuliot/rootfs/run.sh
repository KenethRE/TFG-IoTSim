#!/usr/bin/with-contenv bashio

MQTT_BROKER_HOST=$(bashio::services "host")
MQTT_USER=$(bashio::services "username")
MQTT_PWD=$(bashio::services "password")
DJANGO_LOG_LEVEL=DEBUG

export DJANGO_LOG_LEVEL
export MQTT_BROKER_HOST
export MQTT_USER
export MQTT_PWD

{ echo "MQTT_BROKER_HOST: $MQTT_BROKER_HOST"; echo "MQTT_USER: $MQTT_USER"; echo "MQTT_PWD: $MQTT_PWD"; } >> /simuliot.log

echo "Starting Simulator..."
echo "Starting Simulator Backend..."
python3 ./simuliot_backend/app.py >> /simuliot_run.log &
sleep 1
echo "Starting Simulator Frontend..."
gunicorn --bind 0.0.0.0:8087 simuliot_frontend.wsgi:application &
#python3 ./manage.py runserver 8087 >> /simuliot_run.log &

nginx -g "daemon off;error_log /simuliot_nginx.log debug;"