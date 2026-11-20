import json
import random
import time

import paho.mqtt.client as mqtt

import config

ID_RESERVORIO = 1
EMISOR_ID = "EMI-B4F53904A7AC"
RECEPTOR_ID = "REC-066CFF5748755750"
CAPACIDAD_LITROS = 700000

nivel = 60.0
bomba_encendida = False

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(config.MQTT_USER, config.MQTT_PASS)
client.tls_set()
client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
client.loop_start()

print("Simulando... (Ctrl+C para detener)")
while True:
    if bomba_encendida:
        nivel = min(100, nivel + random.uniform(0.5, 1.5))
    else:
        nivel = max(0, nivel - random.uniform(0.2, 0.8))

    if nivel < 30:
        bomba_encendida = True
    if nivel > 85:
        bomba_encendida = False

    mensaje = {
        "emisor_id": EMISOR_ID,
        "receptor_id": RECEPTOR_ID,
        "porcentaje": round(nivel, 1),
        "litros_agua": round(CAPACIDAD_LITROS * nivel / 100),
        "bomba_estado": "ON" if bomba_encendida else "OFF",
        "tiempo_max_llenado_min": 15,
        "receptor_online": True,
    }
    client.publish(f"reservorio/{ID_RESERVORIO}/datos", json.dumps(mensaje))
    print("Publicado:", mensaje)
    time.sleep(10)
