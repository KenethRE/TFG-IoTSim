#!/usr/bin/with-contenv bashio

echo "Starting Database Server"
sqlite3 /tfg-iot.db
sleep 10
python3 -m http.server 8099