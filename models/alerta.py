"""models/alerta.py - Evento crítico detectado por el sistema."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# Tipos de alerta que maneja el sistema (se guardan como texto en la tabla Alertas)
TIPO_NIVEL_BAJO = "NIVEL_BAJO"
TIPO_NIVEL_ALTO = "NIVEL_ALTO"
TIPO_TIEMPO_EXCEDIDO = "TIEMPO_EXCEDIDO"
TIPO_RECEPTOR_OFFLINE = "RECEPTOR_OFFLINE"
TIPO_SIN_SENAL = "SIN_SENAL"
TIPO_CICLOS_EXCESIVOS = "CICLOS_EXCESIVOS"


@dataclass
class Alerta:
    id_modulo: str
    tipo_alerta: str
    fecha_hora: datetime
    resuelta: bool = False
    id_alertas: Optional[int] = None
    id_reservorio: Optional[int] = None
    nombre_reservorio: str = ""
    ubicacion: str = ""
    tipo_modulo: str = ""
