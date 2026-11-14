"""models/lectura.py - Una medición de nivel de agua enviada por un emisor."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Lectura:
    id_modulo: str
    fecha_hora: datetime
    nivel_agua: float          # porcentaje 0 - 100
    calidad_senal: int = 100
