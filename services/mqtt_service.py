import json

import paho.mqtt.client as mqtt

import config


class MqttService:
    def __init__(self, al_recibir_datos):
        self.al_recibir_datos = al_recibir_datos

        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(config.MQTT_USER, config.MQTT_PASS)
        self.client.tls_set()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            print("Conectado exitosamente a la pasarela MQTT de HiveMQ")
            client.subscribe(config.MQTT_TOPIC_DATOS)
        else:
            print(f"Error de conexión MQTT. Código: {reason_code}")

    def _on_message(self, client, userdata, msg):
        try:
            datos = json.loads(msg.payload.decode())
            id_topic = msg.topic.split("/")[1]
            self.al_recibir_datos(id_topic, datos)
        except Exception as error:
            print(f"Error procesando mensaje MQTT: {error}")

    def iniciar(self):
        print("Conectando al broker...")
        self.client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
        self.client.loop_start()

    def detener(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publicar_comando(self, id_reservorio, comando):
        topic = config.MQTT_TOPIC_COMANDO.format(id=id_reservorio)
        self.client.publish(topic, json.dumps(comando))
