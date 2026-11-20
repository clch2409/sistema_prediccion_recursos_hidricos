from database import conexion
from models.mantenimiento import Mantenimiento

_SQL_BASE = """
SELECT mt.id_mantenimiento, mt.id_bomba, mt.costo, mt.descripcion, mt.fecha_intervencion,
       b.nombre AS nombre_bomba, r.nombre AS nombre_reservorio
FROM Mantenimiento mt
INNER JOIN Sistema_Bombeo b ON b.id_bomba = mt.id_bomba
INNER JOIN Reservorio r ON r.id_reservorio = b.id_reservorio
"""


def _fila_a_mantenimiento(f):
    return Mantenimiento(
        id_mantenimiento=f.id_mantenimiento,
        id_bomba=f.id_bomba,
        costo=float(f.costo or 0),
        descripcion=f.descripcion,
        fecha_intervencion=f.fecha_intervencion,
        nombre_bomba=f.nombre_bomba,
        nombre_reservorio=f.nombre_reservorio,
    )


class MantenimientoRepository:
    def listar(self):
        filas = conexion.consultar(
            _SQL_BASE + " ORDER BY mt.fecha_intervencion DESC, mt.id_mantenimiento DESC")
        return [_fila_a_mantenimiento(f) for f in filas]

    def obtener_por_id(self, id_mantenimiento):
        filas = conexion.consultar(_SQL_BASE + " WHERE mt.id_mantenimiento = ?", (id_mantenimiento,))
        if not filas:
            return None
        return _fila_a_mantenimiento(filas[0])

    def insertar(self, mantenimiento):
        conexion.ejecutar(
            "INSERT INTO Mantenimiento (id_bomba, costo, descripcion, fecha_intervencion) "
            "VALUES (?, ?, ?, ?)",
            (mantenimiento.id_bomba, mantenimiento.costo, mantenimiento.descripcion,
             mantenimiento.fecha_intervencion),
        )

    def actualizar(self, mantenimiento):
        conexion.ejecutar(
            "UPDATE Mantenimiento SET id_bomba = ?, costo = ?, descripcion = ?, "
            "fecha_intervencion = ? WHERE id_mantenimiento = ?",
            (mantenimiento.id_bomba, mantenimiento.costo, mantenimiento.descripcion,
             mantenimiento.fecha_intervencion, mantenimiento.id_mantenimiento),
        )

    def eliminar(self, id_mantenimiento):
        conexion.ejecutar("DELETE FROM Mantenimiento WHERE id_mantenimiento = ?", (id_mantenimiento,))
