import uuid

# This class simulates all contant and non contact temperature probes. This is measured against the absolute zero (0 Kelvin) which is -273.15 degrees Celsius. The maximum temperature that can be recorded by this device is 300 degrees Celsius.
# For non contact sensors (ie. sensors that use infrared or metal devices) the temperature range is -20 to 60 degrees Celsius.

class switchDevice:
    def __init__(self, deviceID, deviceName, client):
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.UUID = str(uuid.uuid4())
        self.switchState = False
        self.client = client

    def reading(self):
        return {
            "state_topic": "homeassistant/sensor/" + self.UUID + "/state",
            "value": self.switchState
        }
    
    def switch(self):
        self.switchState = not self.switchState
        return self.switchState
    
    def publish(self):
        self.client.publish("homeassistant/sensor/" + self.UUID + "/state", self.reading()["value"])