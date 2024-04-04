from random import uniform
import uuid

# This class simulates all contant and non contact temperature probes. This is measured against the absolute zero (0 Kelvin) which is -273.15 degrees Celsius. The maximum temperature that can be recorded by this device is 300 degrees Celsius.
# For non contact sensors (ie. sensors that use infrared or metal devices) the temperature range is -20 to 60 degrees Celsius.

class tempDevice:
    def __init__(self, deviceID, deviceName, location, type, client, isContactProbe):
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.location = location
        self.UUID = str(uuid.uuid4())
        self.isContactProbe = isContactProbe
        self.type = type
        self.client = client

    def contactProbe(self):
        return round(uniform(-273.15, 300), 2)
    
    def nonContactProbe(self):
        return round(uniform(-20, 60), 2)

    def reading(self):
        return {
            "state_topic": "homeassistant/sensor/" + self.UUID + "/state",
            "value": self.contactProbe() if self.isContactProbe else self.nonContactProbe()
        }

    def publish(self):
        self.client.publish("homeassistant/sensor/" + self.UUID + "/state", self.reading()["value"])

    def _publish (self, topic, payload):
        self.client.publish(topic, payload)