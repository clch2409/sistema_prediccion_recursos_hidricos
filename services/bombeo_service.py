import config
from models.alerta import TIPO_NIVEL_ALTO, TIPO_NIVEL_BAJO, TIPO_TIEMPO_EXCEDIDO


def bomba_esta_encendida(valor):
    if isinstance(valor, bool):
        return valor
    return str(valor).strip().upper() in ("ON", "1", "TRUE", "ENCENDIDA", "ENCENDIDO", "ACTIVA")


def decidir_apagado(porcentaje, bomba_encendida, minutos_encendida):
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
    diferencia = porcentaje_final - porcentaje_inicial
    return max(0, diferencia / 100 * capacidad_maxima)
