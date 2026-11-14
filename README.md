# Sistema de Gestión y Predicción de Reservas Hídricas

Proyecto en Python con arquitectura **MVC** (Tkinter + SQL Server + MQTT).

## Cómo ejecutarlo

1. Instala las librerías: `pip install -r requirements.txt`
2. Instala el *ODBC Driver 17 for SQL Server* (o cambia `DRIVER_SQL` en `config.py`).
3. Base de datos `SISTEMA_RECURSOS_HIDRICOS`:
   - Nueva: ejecuta `database/script_bd.sql` (solo crea las tablas; tendrás que insertar tus datos).
   - Ya creada con `id_modulo` numérico: ejecuta `database/migracion_id_modulo.sql`.
4. Edita `config.py`: pon el nombre de tu servidor SQL en `SERVIDOR_SQL`.
5. Registra en `Modulo` tus dispositivos con su código como `id_modulo` (ej: `EMI-B4F53904A7AC`, `REC-066CFF5748755750`).
6. Ejecuta: `python main.py` (necesitas un usuario en la tabla `Usuarios`).
7. Sin hardware: edita y ejecuta `python simulador_emisor.py`.

## Estructura (MVC)

```
main.py                     -> arma el sistema y abre la ventana
config.py                   -> broker, base de datos y reglas de negocio
database/                   -> conexion.py (pyodbc) y script_bd.sql
models/                     -> clases con los datos (Reservorio, Modulo, Lectura, ...)   [M]
repositories/               -> consultas SQL, devuelven objetos de models/
services/                   -> mqtt_service.py, bombeo_service.py, prediccion_service.py
controllers/                -> reciben datos (MQTT o ventana), aplican reglas, usan repositories [C]
views/                      -> ventanas Tkinter, solo muestran datos y llaman controllers       [V]
simulador_emisor.py         -> herramienta de prueba (publica JSON falsos)
```

Flujo de los datos:
`Emisor -> HiveMQ -> MqttService -> MensajeController -> repositories -> SQL Server -> controllers -> views`

## JSON esperado (igual que demo1.py)

```json
{"emisor_id": "EMI-B4F53904A7AC", "receptor_id": "REC-066CFF5748755750", "porcentaje": 54.3,
 "litros_agua": 380100, "bomba_estado": "ON", "tiempo_max_llenado_min": 15, "receptor_online": true}
```
`emisor_id` y `receptor_id` deben existir en `Modulo.id_modulo` (VARCHAR) y pertenecer al mismo reservorio.

## Reglas de negocio (config.py)

- Bomba encendida con nivel <= 10 %, >= 90 % o más de 15 min seguidos -> se envía orden de apagado y se crea alerta.
- Más de 10 encendidos en 60 min -> alerta de riesgo de daño.
- Reservorio sin datos por 5 min -> módulos INACTIVO y alerta.
- Predicción: regresión lineal (numpy) sobre el último tramo en que el nivel viene bajando.
