"""
simulador_emisor.py - Herramienta de PRUEBA (no forma parte del sistema).
Publica JSON falsos en HiveMQ imitando a los circuitos emisores, para probar la aplicación
sin tener el hardware. Ejecutar en otra terminal:  python simulador_emisor.py

IMPORTANTE: los códigos de EMISOR_ID / RECEPTOR_ID deben existir en la tabla Modulo
(columna id_modulo) y el módulo debe pertenecer al reservorio indicado.

Nota: el usuario MQTT debe tener permiso de publicar en HiveMQ.
"""
import json
import random
import time

import paho.mqtt.client as mqtt

import config

# --- EDITA ESTOS DATOS con módulos que existan en tu base de datos ---
ID_RESERVORIO = 1                              # número usado en el topic: reservorio/1/datos
EMISOR_ID = "EMI-B4F53904A7AC"
RECEPTOR_ID = "REC-066CFF5748755750"
CAPACIDAD_LITROS = 700000                      # capacidad del reservorio en litros

nivel = 60.0
bomba_encendida = False

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(config.MQTT_USER, config.MQTT_PASS)
client.tls_set()
client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
client.loop_start()

print("Simulando... (Ctrl+C para detener)")
while True:
    # Si la bomba está encendida el nivel sube; si no, baja por el consumo
    if bomba_encendida:
        nivel = min(100, nivel + random.uniform(0.5, 1.5))
    else:
        nivel = max(0, nivel - random.uniform(0.2, 0.8))

    # Reglas simples para encender / apagar la bomba simulada
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
