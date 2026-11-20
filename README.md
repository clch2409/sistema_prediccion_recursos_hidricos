# Sistema de Gestión y Predicción de Reservas Hídricas

Proyecto en Python con arquitectura **MVC** (Tkinter + SQL Server + MQTT).

## Cómo ejecutarlo

1. Instala las librerías: `pip install -r requirements.txt`
2. Instala el *ODBC Driver 17 for SQL Server* (o cambia `DRIVER_SQL` en `config.py`).
3. Ejecuta `database/script_bd.sql` en SSMS: crea la base `SISTEMA_RECURSOS_HIDRICOS` y sus tablas (`id_modulo` es VARCHAR). Solo crea la estructura; tendrás que insertar tus datos.
4. Edita `config.py`: pon el nombre de tu servidor SQL en `SERVIDOR_SQL`.
5. Registra en `Modulo` tus dispositivos con su código como `id_modulo` (ej: `EMI-B4F53904A7AC`, `REC-066CFF5748755750`).
6. Crea tu primer usuario en `Usuarios` (y los registros de `Tipo_Usuario` / `Tipo_Modulo` que uses). Para guardar la contraseña ya encriptada:
   `python -c "from services.seguridad import encriptar_contrasena as e; print(e('tu_clave'))"` y pega el resultado en la columna `contrasena`.
   (Si insertas una contraseña en texto plano, se convierte a hash automáticamente la primera vez que ese usuario inicia sesión.)
7. Ejecuta: `python main.py`.
8. Sin hardware: edita y ejecuta `python simulador_emisor.py`.

## Estructura (MVC)

```
main.py                     -> arma el sistema y abre la ventana
config.py                   -> broker, base de datos y reglas de negocio
database/                   -> conexion.py (pyodbc) y script_bd.sql
models/                     -> clases con atributos privados, properties y validaciones (Reservorio, Modulo, Lectura, ...)   [M]
repositories/               -> consultas SQL, devuelven objetos de models/
services/                   -> mqtt_service.py, bombeo_service.py, prediccion_service.py, seguridad.py (hash de contraseñas)
controllers/                -> reciben datos (MQTT o ventana), aplican reglas, usan repositories [C]
views/                      -> ventanas Tkinter, solo muestran datos y llaman controllers       [V]
simulador_emisor.py         -> herramienta de prueba (publica JSON falsos)
```

## Pantallas con CRUD (botones Nuevo / Editar / Eliminar)

- **Reservorios**, **Estado módulos**, **Sistemas de bombeo**, **Mantenimientos** y **Usuarios**.
- Los formularios validan los datos (modelos en `models/`) y avisan si un registro no se puede eliminar por tener datos asociados (lecturas, alertas, historial, mantenimientos).
- Un reservorio admite un solo sistema de bombeo (así lo asume el procesamiento MQTT).
- **Usuarios**: la contraseña se guarda con PBKDF2-HMAC-SHA256 + sal aleatoria (`services/seguridad.py`); nunca en texto plano. Al editar, dejar la contraseña vacía conserva la actual. No se puede eliminar el usuario con sesión iniciada ni el último usuario.

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
