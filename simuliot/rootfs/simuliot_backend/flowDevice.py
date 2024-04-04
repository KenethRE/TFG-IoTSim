from random import uniform, randint
import uuid

# This class simulates all contant and non contact temperature probes. This is measured against the absolute zero (0 Kelvin) which is -273.15 degrees Celsius. The maximum temperature that can be recorded by this device is 300 degrees Celsius.
# For non contact sensors (ie. sensors that use infrared or metal devices) the temperature range is -20 to 60 degrees Celsius.

class flowDevice:
    def __init__(self, deviceID, deviceName, location, type, client, kind):
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.location = location
        self.type = type
        self.UUID = str(uuid.uuid4())
        self.kind = kind
        self.client = client

    def airFlow(self):
        return round(uniform(0, 11), 2)
    
    def waterFlow(self):
        return round(randint(2, 1500))

    def createValue(self):
        if self.kind == 'Air_Flow':
            return self.airFlow()
        elif self.kind == 'Water_Flow':
            return self.waterFlow()
        else:
            return 0

    def reading(self):
        return {
            "state_topic": "homeassistant/sensor/" + self.UUID + "/state",
            "value": self.createValue()
        }
    def publish(self):
        self.client.publish("homeassistant/sensor/" + self.UUID + "/state", self.reading()["value"])

    def _publish (self, topic, payload):
        self.client.publish(topic, payload)