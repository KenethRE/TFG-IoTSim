from random import uniform
import uuid

# This class simulates all contant and non contact temperature probes. This is measured against the absolute zero (0 Kelvin) which is -273.15 degrees Celsius. The maximum temperature that can be recorded by this device is 300 degrees Celsius.
# For non contact sensors (ie. sensors that use infrared or metal devices) the temperature range is -20 to 60 degrees Celsius.

class soundSensorDevice:
    def __init__(self, deviceID, deviceName, location, type, client):
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.UUID = str(uuid.uuid4())
        self.location = location
        self.type = type
        self.client = client

    def reading(self):
        return {
            "state_topic": "homeassistant/sensor/" + self.UUID + "/state",
            "value": round(uniform(0, 100), 2)
        }
    def publish(self):
        self.client.publish("homeassistant/sensor/" + self.UUID + "/state", self.reading()["value"])