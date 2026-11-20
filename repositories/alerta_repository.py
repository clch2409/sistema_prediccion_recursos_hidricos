from database import conexion
from models.alerta import Alerta


class AlertaRepository:
    def existe_pendiente(self, id_modulo, tipo_alerta):
        filas = conexion.consultar(
            "SELECT COUNT(*) AS total FROM Alertas "
            "WHERE id_modulo = ? AND tipo_alerta = ? AND resuelta = 0",
            (id_modulo, tipo_alerta),
        )
        return filas[0].total > 0

    def insertar(self, alerta):
        conexion.ejecutar(
            "INSERT INTO Alertas (id_modulo, tipo_alerta, fecha_hora, resuelta) VALUES (?, ?, ?, 0)",
            (alerta.id_modulo, alerta.tipo_alerta, alerta.fecha_hora),
        )

    def resolver(self, id_modulo, tipo_alerta):
        conexion.ejecutar(
            "UPDATE Alertas SET resuelta = 1 "
            "WHERE id_modulo = ? AND tipo_alerta = ? AND resuelta = 0",
            (id_modulo, tipo_alerta),
        )

    def listar_pendientes(self):
        filas = conexion.consultar(
            "SELECT a.id_alertas, a.id_modulo, a.tipo_alerta, a.fecha_hora, a.resuelta, "
            "       r.id_reservorio, r.nombre AS nombre_reservorio, r.ubicacion, "
            "       t.nombre_modulo AS tipo_modulo "
            "FROM Alertas a "
            "INNER JOIN Modulo m ON m.id_modulo = a.id_modulo "
            "INNER JOIN Reservorio r ON r.id_reservorio = m.id_reservorio "
            "INNER JOIN Tipo_Modulo t ON t.id_tipo_modulo = m.id_tipo_modulo "
            "WHERE a.resuelta = 0 ORDER BY a.fecha_hora DESC"
        )
        return [
            Alerta(
                id_modulo=f.id_modulo, tipo_alerta=f.tipo_alerta, fecha_hora=f.fecha_hora,
                resuelta=bool(f.resuelta), id_alertas=f.id_alertas,
                id_reservorio=f.id_reservorio, nombre_reservorio=f.nombre_reservorio,
                ubicacion=f.ubicacion, tipo_modulo=f.tipo_modulo,
            )
            for f in filas
        ]
