"""models/bomba.py - Electrobomba que llena un reservorio."""
from dataclasses import dataclass

import config


@dataclass
class SistemaBombeo:
    id_bomba: int
    id_reservorio: int
    nombre: str
    modelo: str
    caudal_l_s: float
    consumo_kw: float
    estado: bool                 # True = ACTIVO, False = INACTIVO (columna BIT)
    horas_iniciales: float = 0
    # Datos calculados que llenan los repositorios / controladores
    horas_operacion: float = 0
    ciclos_ultima_hora: int = 0
    nombre_reservorio: str = ""
    ubicacion: str = ""

    def vida_util_restante_pct(self):
        """Porcentaje de vida útil que le queda a la bomba."""
        usado = self.horas_operacion / config.HORAS_VIDA_UTIL * 100
        return max(0, round(100 - usado, 1))

    def necesita_mantenimiento(self):
        """Devuelve el texto del mantenimiento que toca (o '' si no toca ninguno)."""
        if self.horas_operacion >= config.HORAS_MTTO_MAYOR:
            return "MTTO MAYOR"
        if self.horas_operacion >= config.HORAS_MTTO_MENOR:
            return "MTTO MENOR"
        return ""
