#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import os

mqtt_broker = {
    "host": os.getenv("MQTT_BROKER_HOST", "localhost"),
    "port": int(os.getenv("MQTT_BROKER_PORT", 1883))
}

mqtt_credentials = {
    "user": os.getenv("MQTT_USER", "user"),
    "pwd": os.getenv("MQTT_PWD", "password")
}


TOPIC = "homeassistant/sensor/+"
