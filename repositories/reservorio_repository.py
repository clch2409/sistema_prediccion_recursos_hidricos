from database import conexion
from models.reservorio import Reservorio

_SQL_BASE = """
SELECT r.id_reservorio, r.nombre, r.capacidad_maxima, r.ubicacion, r.fecha_construccion,
       (SELECT TOP 1 l.nivel_agua FROM Lecturas l
          INNER JOIN Modulo m ON m.id_modulo = l.id_modulo
          WHERE m.id_reservorio = r.id_reservorio
          ORDER BY l.fecha_hora DESC) AS porcentaje,
       (SELECT TOP 1 l.fecha_hora FROM Lecturas l
          INNER JOIN Modulo m ON m.id_modulo = l.id_modulo
          WHERE m.id_reservorio = r.id_reservorio
          ORDER BY l.fecha_hora DESC) AS ultima_lectura
FROM Reservorio r
"""


def _fila_a_reservorio(fila):
    porcentaje = float(fila.porcentaje) if fila.porcentaje is not None else None
    return Reservorio(
        id_reservorio=fila.id_reservorio,
        nombre=fila.nombre,
        capacidad_maxima=float(fila.capacidad_maxima),
        ubicacion=fila.ubicacion,
        fecha_construccion=fila.fecha_construccion,
        porcentaje=porcentaje,
        ultima_lectura=fila.ultima_lectura,
    )


class ReservorioRepository:
    def listar(self):
        filas = conexion.consultar(_SQL_BASE + " ORDER BY r.id_reservorio")
        return [_fila_a_reservorio(f) for f in filas]

    def obtener_por_id(self, id_reservorio):
        filas = conexion.consultar(_SQL_BASE + " WHERE r.id_reservorio = ?", (id_reservorio,))
        if not filas:
            return None
        return _fila_a_reservorio(filas[0])
