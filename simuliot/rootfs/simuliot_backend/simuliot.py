#!/usr/bin/python3
from time import sleep
import tempDevice as temp
import configurableSwitchDevice as switch_config
import switchDevice as switch
import flowDevice as flow
import tempSwitchDevice as temp_switch
import presenceDevice as presence
import soundSensorDevice as sound
import hubDevice as hub
import paho.mqtt.client as mqtt
import mqtt_config as mqtt_cfg
import sqlite3
import logging
import os, sys
import json

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
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



def signal_handler(sig, frame):
    logger.info('Shutting down Simulated IoT Device')
    sys.exit(0)

def on_connect(client, userdata, flags, rc):
    logger.info('connected ({})'.format(client._client_id))
    client.subscribe(topic=mqtt_cfg.TOPIC, qos=2)

def on_message(client, userdata, message):
    logger.info('------------------------------')
    decoded = json.loads(message.payload.decode())
    logger.info("topic: {}, msg: {}".format(
        message.topic, decoded))

def connect_db():
    conn = None
    if (os.path.isfile('../tfg-test.db')):
        try:
            conn = sqlite3.connect('../tfg-test.db')
            logger.info("Connected to SQLite DB")
        except sqlite3.Error as e:
            logger.critical('Failure to open DB. Please reinstall addon: ' + str(e))
    else: 
        logger.critical('Database file not found. Please reinstall addon.')
    return conn

def connect_mqtt():
    try:
        Client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="SimulIoT Session Client", clean_session=False)
        Client.on_connect = on_connect
        Client.on_message = on_message
        Client.username_pw_set(mqtt_cfg.mqtt_credentials["user"], mqtt_cfg.mqtt_credentials["pwd"])
        Client.connect(host=mqtt_cfg.mqtt_broker["host"], port=mqtt_cfg.mqtt_broker["port"])
        return Client
    except Exception as e:
        logger.critical('Error: ' + str(e))

client = connect_mqtt()

def getTempDevice(deviceID, deviceName, location, type, isContactProbe):
    tempDevice = temp.tempDevice(deviceID, deviceName, location, type, client, isContactProbe)
    return tempDevice

def getSwitchConfigurableDevice(deviceID, deviceName, location, type, config):
    ## All configs will be empty for now
    switchConfigurableDevice = switch_config.configurableSwitchDevice(deviceID, deviceName, location, type, client, config)
    return switchConfigurableDevice

def getSwitchDevice(deviceID, deviceName, location, type):
    switchDevice = switch.switchDevice(deviceID, deviceName, location, type, client)
    return switchDevice

def getFlowDevice(deviceID, deviceName, location, type, kind):
    flowDevice = flow.flowDevice(deviceID, deviceName, location, type, client, kind)
    return flowDevice

def getTempSwitchDevice(deviceID, deviceName, location, type):
    tempSwitchDevice = temp_switch.tempSwitchDevice(deviceID, deviceName, location, type, client)
    return tempSwitchDevice

def getPresenceDevice(deviceID, deviceName, location, type):
    presenceDevice = presence.presenceDevice(deviceID, deviceName, location, type, client)
    return presenceDevice

def getSoundSensorDevice(deviceID, deviceName, location, type):
    soundSensorDevice = sound.soundSensorDevice(deviceID, deviceName, location, type, client)
    return soundSensorDevice

def getHubDevice(deviceID, deviceName, location, type):
    hubDevice = hub.hubDevice(deviceID, deviceName, location, type, client)
    return hubDevice

def start(devicesCurrentSession):
    while True:
        for device in devicesCurrentSession:
            device.publish()
        sleep(5)