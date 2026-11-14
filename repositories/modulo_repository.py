"""repositories/modulo_repository.py - Consultas SQL de la tabla Modulo."""
from database import conexion
from models.modulo import Modulo

_SQL_BASE = """
SELECT m.id_modulo, m.id_reservorio, m.id_tipo_modulo, m.nombre_modulo,
       m.altura_instalacion, m.estado, m.fecha_estado,
       t.nombre_modulo AS tipo, r.nombre AS nombre_reservorio
FROM Modulo m
INNER JOIN Tipo_Modulo t ON t.id_tipo_modulo = m.id_tipo_modulo
INNER JOIN Reservorio r  ON r.id_reservorio = m.id_reservorio
"""


def _fila_a_modulo(fila):
    return Modulo(
        id_modulo=fila.id_modulo,
        id_reservorio=fila.id_reservorio,
        id_tipo_modulo=fila.id_tipo_modulo,
        nombre_modulo=fila.nombre_modulo,
        altura_instalacion=float(fila.altura_instalacion or 0),
        estado=bool(fila.estado),
        fecha_estado=fila.fecha_estado,
        tipo=fila.tipo,
        nombre_reservorio=fila.nombre_reservorio,
    )


class ModuloRepository:

    def listar(self):
        filas = conexion.consultar(_SQL_BASE + " ORDER BY r.id_reservorio, t.id_tipo_modulo")
        return [_fila_a_modulo(f) for f in filas]

    def obtener_por_id(self, id_modulo):
        """id_modulo es el código de texto, ej: 'EMI-B4F53904A7AC'."""
        filas = conexion.consultar(_SQL_BASE + " WHERE m.id_modulo = ?", (str(id_modulo),))
        if not filas:
            return None
        return _fila_a_modulo(filas[0])

    def actualizar_estado(self, id_modulo, activo, ahora):
        """activo: True/False. Cambia el estado solo si es distinto y guarda cuándo cambió."""
        valor = 1 if activo else 0
        conexion.ejecutar(
            "UPDATE Modulo SET estado = ?, fecha_estado = ? "
            "WHERE id_modulo = ? AND estado <> ?",
            (valor, ahora, id_modulo, valor),
        )
