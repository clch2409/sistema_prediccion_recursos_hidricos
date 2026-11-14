"""
services/bombeo_service.py
Reglas de negocio de la bomba. Son funciones simples (sin base de datos),
así es fácil probarlas y entenderlas.
"""
import config
from models.alerta import TIPO_NIVEL_ALTO, TIPO_NIVEL_BAJO, TIPO_TIEMPO_EXCEDIDO


def bomba_esta_encendida(valor):
    """
    El JSON trae 'bomba_estado'. No sabemos si viene como "ON", "ENCENDIDA", true o 1,
    así que aceptamos varias formas.
    """
    if isinstance(valor, bool):
        return valor
    return str(valor).strip().upper() in ("ON", "1", "TRUE", "ENCENDIDA", "ENCENDIDO", "ACTIVA")


def decidir_apagado(porcentaje, bomba_encendida, minutos_encendida):
    """
    Devuelve el tipo de alerta que obliga a apagar la bomba,
    o None si la bomba puede seguir como está.

    Reglas del proyecto:
      - 10 % o menos        -> corte por trabajo en seco
      - 90 % o más          -> corte por riesgo de desborde
      - 15 min continuos    -> apagado forzado preventivo
    """
    if not bomba_encendida:
        return None
    if porcentaje <= config.NIVEL_MINIMO:
        return TIPO_NIVEL_BAJO
    if porcentaje >= config.NIVEL_MAXIMO:
        return TIPO_NIVEL_ALTO
    if minutos_encendida >= config.TIEMPO_MAX_BOMBEO_MIN:
        return TIPO_TIEMPO_EXCEDIDO
    return None


def calcular_volumen_inyectado(porcentaje_inicial, porcentaje_final, capacidad_maxima):
    """Litros que subió el reservorio durante un ciclo de bombeo (nunca negativo)."""
    diferencia = porcentaje_final - porcentaje_inicial
    return max(0, diferencia / 100 * capacidad_maxima)
