"""
config.py
Todos los valores que el proyecto necesita en un solo lugar.
Si cambias de servidor, de broker o de reglas de negocio, solo editas este archivo.
"""

# ---------------- MQTT (HiveMQ Cloud) ----------------
MQTT_BROKER = "a11d431deae14284a7becfbb2653769f.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "python_user"
MQTT_PASS = "python_user"

# Topic donde los emisores publican sus JSON (el + es un comodín: un topic por reservorio)
MQTT_TOPIC_DATOS = "reservorio/+/datos"
# Topic al que ENVIAMOS órdenes al receptor (apagar bomba). {id} se reemplaza por el reservorio.
# OJO: este topic es una suposición, ajústalo a lo que escuche tu circuito receptor.
MQTT_TOPIC_COMANDO = "reservorio/{id}/comando"

# ---------------- SQL Server ----------------
SERVIDOR_SQL = r"LAPTOP-CVKI77EA\CLCH2409"      # cambia por el nombre de tu servidor
BASE_DATOS = "SISTEMA_RECURSOS_HIDRICOS"
DRIVER_SQL = "ODBC Driver 17 for SQL Server"

CADENA_CONEXION = (
    f"DRIVER={{{DRIVER_SQL}}};"
    f"SERVER={SERVIDOR_SQL};"
    f"DATABASE={BASE_DATOS};"
    "Trusted_Connection=yes;"
)

# ---------------- Reglas de negocio ----------------
NIVEL_MINIMO = 10          # % -> por debajo se corta la bomba (trabajo en seco)
NIVEL_MAXIMO = 90          # % -> por encima se corta la bomba (desborde)
TIEMPO_MAX_BOMBEO_MIN = 15 # minutos continuos de bombeo antes del apagado forzado
MAX_CICLOS_HORA = 10       # más ciclos de encendido en 60 min = riesgo de daño
MINUTOS_SIN_SENAL = 5      # si un reservorio no envía datos en este tiempo, sus módulos pasan a INACTIVO

# Horas de operación de las bombas (pantalla "Sistemas de bombeo")
HORAS_MTTO_MENOR = 3000
HORAS_MTTO_MAYOR = 8000
HORAS_VIDA_UTIL = 100000

# ---------------- Interfaz ----------------
INTERVALO_REFRESCO_MS = 5000   # la pantalla se actualiza cada 5 segundos
