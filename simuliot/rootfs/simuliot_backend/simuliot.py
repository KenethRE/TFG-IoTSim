#!/usr/bin/python3
from time import sleep
import tempDevice as temp
import configurableSwitchDevice as switch_config
import switchDevice as switch
import flowDevice as flow
import tempSwitchDevice as temp_switch
import presenceDevice as presence
import soundSensorDevice as sound
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

def signal_handler(sig, frame):
    logger.info('Shutting down Simulated IoT Device')
    sys.exit(0)

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
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
        else:
            logger.critical("Failed to connect, return code %d\n", rc)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("localhost", 1883)
    return client

def getTempDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe):
    tempDevice = temp.tempDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe)
    return tempDevice

def getSwitchConfigurableDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe):
    switchConfigurableDevice = switch_config.configurableSwitchDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe)
    return switchConfigurableDevice

def getSwitchDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe):
    switchDevice = switch.switchDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe)
    return switchDevice

def getFlowDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe):
    flowDevice = flow.flowDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe)
    return flowDevice

def getTempSwitchDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe):
    tempSwitchDevice = temp_switch.tempSwitchDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe)
    return tempSwitchDevice

def getPresenceDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe):
    presenceDevice = presence.presenceDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe)
    return presenceDevice

def getSoundSensorDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe):
    soundSensorDevice = sound.soundSensorDevice(deviceID, deviceName, deviceClass, deviceModel, deviceManufacturer, isContactProbe)
    return soundSensorDevice

def start(devicesCurrentSession):
    client = connect_mqtt()
    client.loop_start()

    while True:
        for device in devicesCurrentSession:
            if device['type'] == 'TEMP':
                tempDevice = getTempDevice( device['id'], device['name'], device['type'], 'T1', device['manufacturer'], False)
                tempDevice.publish(client)
            elif device['type'] == 'SWITCH_CONFIGURABLE':
                switchConfigurableDevice = getSwitchConfigurableDevice(device['id'], device['name'], device['type'], 'S1', device['manufacturer'], False)
                switchConfigurableDevice.publish(client)
            elif device['type'] == 'SWITCH':
                switchDevice = getSwitchDevice(device['id'], device['name'], device['type'], 'S2', device['manufacturer'], False)
                switchDevice.publish(client)
            elif device['type'] == 'FLOW':
                flowDevice = getFlowDevice(device['id'], device['name'], device['type'], 'F1', device['manufacturer'], False)
                flowDevice.publish(client)
            elif device['type'] == 'TEMP_SWITCH':
                tempSwitchDevice = getTempSwitchDevice(device['id'], device['name'], device['type'], 'TS1', device['manufacturer'], False)
                tempSwitchDevice.publish(client)
            elif device['type'] == 'PRESENCE':
                presenceDevice = getPresenceDevice(device['id'], device['name'], device['type'], 'P1', device['manufacturer'], False)
                presenceDevice.publish(client)
            elif device['type'] == 'SOUND_SENSOR':
                soundSensorDevice = getSoundSensorDevice(device['id'], device['name'], device['type'], 'SS1', device['manufacturer'], False)
                soundSensorDevice.publish(client)
        sleep(5)