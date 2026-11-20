from datetime import timedelta

import numpy as np
import pandas as pd

TOLERANCIA = 0.5


def obtener_tramo_descendente(lecturas):
    if not lecturas:
        return []
    tramo = [lecturas[-1]]
    for lectura in reversed(lecturas[:-1]):
        if lectura.nivel_agua >= float(tramo[0].nivel_agua) - TOLERANCIA:
            tramo.insert(0, lectura)
        else:
            break
    return tramo


def calcular_prediccion(lecturas, capacidad_maxima):
    tramo = obtener_tramo_descendente(lecturas)
    if len(tramo) < 2:
        return None

    tabla = pd.DataFrame({
        "fecha": [l.fecha_hora for l in tramo],
        "nivel": [float(l.nivel_agua) for l in tramo],
    })
    tabla["horas"] = (tabla["fecha"] - tabla["fecha"].iloc[0]).dt.total_seconds() / 3600

    if tabla["horas"].iloc[-1] <= 0:
        return None

    pendiente, _ordenada = np.polyfit(tabla["horas"], tabla["nivel"], 1)
    if pendiente >= 0:
        return None

    consumo_pct_hora = -pendiente
    nivel_actual = tabla["nivel"].iloc[-1]
    horas_restantes = nivel_actual / consumo_pct_hora
    fecha_ultima = tabla["fecha"].iloc[-1].to_pydatetime()

    return {
        "tabla": tabla,
        "nivel_actual": nivel_actual,
        "consumo_pct_hora": consumo_pct_hora,
        "consumo_litros_hora": consumo_pct_hora / 100 * capacidad_maxima,
        "horas_restantes": horas_restantes,
        "dias_restantes": horas_restantes / 24,
        "fecha_ultima": fecha_ultima,
        "fecha_limite": fecha_ultima + timedelta(hours=horas_restantes),
    }
