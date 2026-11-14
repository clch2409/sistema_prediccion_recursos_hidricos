"""models/modulo.py - Dispositivo de hardware (emisor o receptor) instalado en un reservorio."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Modulo:
    id_modulo: str                               # código del hardware: EMI-B4F53904A7AC / REC-066CFF5748755750
    id_reservorio: int
    id_tipo_modulo: int
    nombre_modulo: str
    altura_instalacion: float
    estado: bool                                 # True = ACTIVO, False = INACTIVO (columna BIT)
    fecha_estado: Optional[datetime] = None
    tipo: str = ""                               # EMISOR / RECEPTOR (viene de Tipo_Modulo)
    nombre_reservorio: str = ""
