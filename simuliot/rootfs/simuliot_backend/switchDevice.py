import uuid
import json

# This class simulates all contant and non contact temperature probes. This is measured against the absolute zero (0 Kelvin) which is -273.15 degrees Celsius. The maximum temperature that can be recorded by this device is 300 degrees Celsius.
# For non contact sensors (ie. sensors that use infrared or metal devices) the temperature range is -20 to 60 degrees Celsius.

class switchDevice:
    def __init__(self, deviceID, deviceName, location, type, client):
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.location = location
        self.UUID = str(uuid.uuid4())
        self.switchState = False
        self.type = type
        self.client = client
        self.topic = "homeassistant/switch/"

    def setup(self):
        self.client.publish(self.topic + self.deviceName + "/config",
                            json.dumps({
                            "name": self.deviceName,
                            "unique_id": self.UUID,
                            "state_topic": self.topic + self.UUID + "/state",
                            "command_topic": self.topic + self.UUID + "/set",
                            "device": {
                                "identifiers": self.deviceID,
                                "name": self.deviceName,
                                "model": self.type,
                                "manufacturer": "SimulIOT"
                            },
                            "availability_topic":  self.topic + self.deviceName + "/availability"
        }))

    def reading(self):
        return {
            "state_topic":  self.topic + self.UUID + "/state",
            "value": self.switchState
        }

    def switch(self):
        self.switchState = not self.switchState
        return self.switchState

    def publish(self):
        self.client.publish(self.topic + self.UUID + "/set", self.reading()["value"])

    def _publish (self, topic, payload):
        self.client.publish(topic, payload)