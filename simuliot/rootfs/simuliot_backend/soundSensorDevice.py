from random import uniform
import uuid
import json
import mqtt_config as mqtt_cfg
import mqtt_client
import simuliot

# This class simulates all contant and non contact temperature probes. This is measured against the absolute zero (0 Kelvin) which is -273.15 degrees Celsius. The maximum temperature that can be recorded by this device is 300 degrees Celsius.
# For non contact sensors (ie. sensors that use infrared or metal devices) the temperature range is -20 to 60 degrees Celsius.

class soundSensorDevice:
    def __init__(self, deviceID, deviceName, location, type):
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.UUID = str(uuid.uuid4())
        self.location = location
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
                            "unit_of_measurement":"dB",
                            "value_template":"{{ value_json.sound_level }}",
                            "device": {
                                "identifiers": self.UUID,
                                "name": self.deviceName,
                                "model": self.type,
                                "manufacturer": "SimulIOT"
                            }
        }))
        self.isSetup = True

    def on_connect(self, client, userdata, flags, rc):
        simuliot.logger.info('connected ({})'.format(client._client_id))
        self.client.subscribe(topic=mqtt_cfg.MQTT_STATUS_TOPIC, qos=0)
        self.client.subscribe(topic=self.topic + self.UUID + "/set", qos=0)

    def on_message(self, client, userdata, message):
        simuliot.logger.info('------------------------------')
        decoded = json.loads(message.payload.decode())
        simuliot.logger.info("topic: {}, msg: {}. MQTT ONLINE".format(
            message.topic, decoded))
        if decoded == 'online':
            self.setup()

    def reading(self):
        return json.dumps({
            "sound_level": round(uniform(0, 100), 2)
        })
    def publish(self):
        if not self.isSetup:
            self.setup()
        self.state = self.reading()
        self.client.publish("homeassistant/sensor/" + self.UUID + "/state", self.state)

    def _publish (self, topic, payload):
        if not self.isSetup:
            self.setup()
        self.client.publish(topic, payload)