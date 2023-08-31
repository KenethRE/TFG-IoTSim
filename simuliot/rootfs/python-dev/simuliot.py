#!/usr/bin/python3
from time import sleep
import tempDevice as temp
import paho.mqtt.client as mqtt
import sqlite3
import logging
import os, sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('simuliot.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(file_handler)
logger.info('Starting Simulated IoT Device')

def connect_db():
    conn = None
    if (os.path.isfile('./tfg-test.db')):
        try:
            conn = sqlite3.connect('./tfg-test.db')
            logger.info("Connected to SQLite DB")
        except sqlite3.Error as e:
            logger.critical('Failure to open DB. Please reinstall addon: ' + e)
    else: 
        logger.critical('Database file not found. Please reinstall addon.')
    return conn

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("localhost", 1883)
    return client

def main():
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT * FROM DEVICES")
        rows = cur.fetchall()
    temperature = temp.tempDevice()
    reading1 = temperature.contactProbe()
    print ("Contact Probe Reading: " + str(reading1))
    sleep(1)
    reading2 = temperature.nonContactProbe()
    print ("Non Contact Probe Reading: " + str(reading2))

if __name__ == "__main__":
    main()