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
        Client = mqtt.Client(client_id="SimulIoT Session Client", clean_session=False)
        Client.on_connect = on_connect
        Client.on_message = on_message
        Client.username_pw_set(mqtt_cfg.mqtt_credentials["user"], mqtt_cfg.mqtt_credentials["pwd"])
        Client.connect(host=mqtt_cfg.mqtt_broker["host"], port=mqtt_cfg.mqtt_broker["port"])
        return Client
    except Exception as e:
        logger.critical('Error: ' + str(e))

def getTempDevice(deviceID, deviceName, isContactProbe, client):
    tempDevice = temp.tempDevice(deviceID, deviceName, isContactProbe, client)
    return tempDevice

def getSwitchConfigurableDevice(deviceID, deviceName, isContactProbe, client):
    switchConfigurableDevice = switch_config.configurableSwitchDevice(deviceID, deviceName, isContactProbe, client)
    return switchConfigurableDevice

def getSwitchDevice(deviceID, deviceName, isContactProbe, client):
    switchDevice = switch.switchDevice(deviceID, deviceName, isContactProbe, client)
    return switchDevice

def getFlowDevice(deviceID, deviceName, isContactProbe, client):
    flowDevice = flow.flowDevice(deviceID, deviceName, isContactProbe, client)
    return flowDevice

def getTempSwitchDevice(deviceID, deviceName, isContactProbe, client):
    tempSwitchDevice = temp_switch.tempSwitchDevice(deviceID, deviceName, isContactProbe, client)
    return tempSwitchDevice

def getPresenceDevice(deviceID, deviceName, isContactProbe, client):
    presenceDevice = presence.presenceDevice(deviceID, deviceName, isContactProbe, client)
    return presenceDevice

def getSoundSensorDevice(deviceID, deviceName, isContactProbe, client):
    soundSensorDevice = sound.soundSensorDevice(deviceID, deviceName, isContactProbe, client)
    return soundSensorDevice

def start(devicesCurrentSession):
    client = connect_mqtt()

    while True:
        for device in devicesCurrentSession:
            if device['type'] == 'temperature':
                tempDevice = getTempDevice(device['id'], device['name'], device['isContactProbe'], client)
                device['reading'] = tempDevice.reading()
                device['publish'] = tempDevice.publish()
            elif device['type'] == 'switch_configurable':
                switchConfigurableDevice = getSwitchConfigurableDevice(device['id'], device['name'], device['isContactProbe'], client)
                device['reading'] = switchConfigurableDevice.reading()
                device['publish'] = switchConfigurableDevice.publish()
            elif device['type'] == 'switch':
                switchDevice = getSwitchDevice(device['id'], device['name'], device['isContactProbe'], client)
                device['reading'] = switchDevice.reading()
                device['publish'] = switchDevice.publish()
            elif device['type'] == 'flow':
                flowDevice = getFlowDevice(device['id'], device['name'], device['isContactProbe'], client)
                device['reading'] = flowDevice.reading()
                device['publish'] = flowDevice.publish()
            elif device['type'] == 'temp_switch':
                tempSwitchDevice = getTempSwitchDevice(device['id'], device['name'], device['isContactProbe'], client)
                device['reading'] = tempSwitchDevice.reading()
                device['publish'] = tempSwitchDevice.publish()
            elif device['type'] == 'presence':
                presenceDevice = getPresenceDevice(device['id'], device['name'], device['isContactProbe'], client)
                device['reading'] = presenceDevice.reading()
                device['publish'] = presenceDevice.publish()
            elif device['type'] == 'sound_sensor':
                soundSensorDevice = getSoundSensorDevice(device['id'], device['name'], device['isContactProbe'], client)
                device['reading'] = soundSensorDevice.reading()
                device['publish'] = soundSensorDevice.publish()
        sleep(5)