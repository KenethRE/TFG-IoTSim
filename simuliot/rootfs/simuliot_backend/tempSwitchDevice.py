from random import uniform
import uuid
import json
import mqtt_config as mqtt_cfg
import mqtt_client
import simuliot

# This class simulates all contant and non contact temperature probes. This is measured against the absolute zero (0 Kelvin) which is -273.15 degrees Celsius. The maximum temperature that can be recorded by this device is 300 degrees Celsius.
# For non contact sensors (ie. sensors that use infrared or metal devices) the temperature range is -20 to 60 degrees Celsius.

class tempSwitchDevice:
    def __init__(self, deviceID, deviceName, location, type):
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.UUID = str(uuid.uuid4())
        self.location = location
        self.switchState = 'OFF'
        self.type = type
        self.client = mqtt_client.client(self.UUID)
        self.topic = "homeassistant/sensor/"
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.isSetup = False

    def setup(self):
        self.client.publish(self.topic + self.UUID + "/config",
                            json.dumps({
                            "name": self.deviceName,
                            "unique_id": self.UUID,
                            "object_id": self.deviceName.replace(" ", "_").lower(),
                            "state_topic": self.topic + self.UUID + "/state",
                            "command_topic": self.topic + self.UUID + "/set",
                            "device": {
                                "identifiers": self.UUID,
                                "name": self.deviceName,
                                "model": self.type,
                                "manufacturer": "SimulIOT"
                            }
        }))
        self.client.publish(self.topic + self.UUID + "/config",
                            json.dumps({
                            "name": self.deviceName,
                            "unique_id": self.UUID,
                            "object_id": self.deviceName.replace(" ", "_").lower(),
                            "state_topic": self.topic + self.UUID + "/state",
                            "unit_of_measurement":"°C",
                            "value_template":"{{ value_json.temperature }}",
                            "device": {
                                "identifiers": self.UUID,
                                "name": self.deviceName,
                                "model": self.type,
                                "manufacturer": "SimulIOT"
                            }
        }))
        self.isSetup = True

    def nonContactProbe(self):
        return round(uniform(-20, 60), 2)

    def reading(self):
        return json.dumps({
            "temperature": self.nonContactProbe(),
        })
    def switch(self):
        self.switchState = not self.switchState
        return self.switchState

    def publish(self):
        if not self.isSetup:
            self.setup()
        self.state = self.reading()
        self.client.publish("homeassistant/sensor/" + self.UUID + "/state", self.state)

    def _publish (self, topic, payload):
        if not self.isSetup:
            self.setup()
        self.client.publish(topic, payload)