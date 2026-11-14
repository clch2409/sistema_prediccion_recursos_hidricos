"""models/reservorio.py - Clase que representa un reservorio (tanque o cisterna)."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Reservorio:
    id_reservorio: int
    nombre: str
    capacidad_maxima: int                       # litros
    ubicacion: str
    fecha_construccion: Optional[datetime] = None
    # Datos de la última lectura (se llenan al consultar con JOIN)
    porcentaje: Optional[float] = None
    ultima_lectura: Optional[datetime] = None

    def litros_actuales(self):
        """Convierte el porcentaje actual en litros."""
        if self.porcentaje is None:
            return 0
        return self.capacidad_maxima * float(self.porcentaje) / 100
