import paho.mqtt.client as mqtt
import mqtt_config as mqtt_cfg
import simuliot
import json


def on_connect(client, userdata, flags, rc):
    simuliot.logger.info('connected ({})'.format(client._client_id))
    client.subscribe(topic=mqtt_cfg.TOPIC, qos=2)

def on_message(client, userdata, message):
    simuliot.logger.info('------------------------------')
    decoded = json.loads(message.payload.decode())
    simuliot.logger.info("topic: {}, msg: {}".format(
        message.topic, decoded))

def client():
    Client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="SimulIoT Session Client", clean_session=False)
    Client.on_connect = on_connect
    Client.on_message = on_message
    Client.username_pw_set(mqtt_cfg.mqtt_credentials["user"], mqtt_cfg.mqtt_credentials["pwd"])
    Client.connect(host=mqtt_cfg.mqtt_broker["host"], port=mqtt_cfg.mqtt_broker["port"])
    return Client