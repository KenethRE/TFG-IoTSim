from random import uniform, randint
import uuid
import json
import mqtt_config as mqtt_cfg
import simuliot

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
        self.topic = "homeassistant/sensor/"
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.isSetup = False

    def setup(self):
        self.client.publish(self.topic + self.UUID + "/config",
                            {
                            "name": self.deviceName,
                            "unique_id": self.UUID,
                            "object_id": self.deviceName.replace(" ", "_").lower(),
                            "state_topic": self.topic + self.UUID + "/state",
                            "unit_of_measurement": "L/min" if self.kind == 'Air_Flow' else "m³/min",
                            "value_template":"{{ value_json.reading }}",
                            "device": {
                                "identifiers": self.UUID,
                                "name": self.deviceName,
                                "model": self.type,
                                "manufacturer": "SimulIOT"
                            }
        })
        self.isSetup = True

    def on_connect(self, client, userdata, flags, rc):
        simuliot.logger.info('connected ({})'.format(client._client_id))
        client.subscribe(topic=mqtt_cfg.MQTT_STATUS_TOPIC, qos=0)
        client.subscribe(topic=self.topic + self.UUID + "/set", qos=0)

    def on_message(self, client, userdata, message):
        simuliot.logger.info('------------------------------')
        decoded = json.loads(message.payload.decode())
        simuliot.logger.info("topic: {}, msg: {}. MQTT ONLINE".format(
            message.topic, decoded))
        if decoded == 'online':
            self.setup()

    def createValue(self):
        if self.kind == 'Air_Flow':
            return round(uniform(0, 11), 2)
        elif self.kind == 'Water_Flow':
            return round(randint(2, 1500))
        else:
            return 0

    def reading(self):
        return {
            "reading": self.createValue()
        }
    def publish(self):
        if not self.isSetup:
            self.setup()
        self.client.publish("homeassistant/sensor/" + self.UUID + "/state", self.reading())

    def _publish (self, topic, payload):
        if not self.isSetup:
            self.setup()
        self.client.publish(topic, payload)