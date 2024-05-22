import paho.mqtt.client as mqtt
import mqtt_config as mqtt_cfg
import simuliot
import json

def client():
    Client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="SimulIoT Session Client", clean_session=False)
    Client.username_pw_set(mqtt_cfg.mqtt_credentials["user"], mqtt_cfg.mqtt_credentials["pwd"])
    Client.connect(host=mqtt_cfg.mqtt_broker["host"], port=mqtt_cfg.mqtt_broker["port"])
    return Client