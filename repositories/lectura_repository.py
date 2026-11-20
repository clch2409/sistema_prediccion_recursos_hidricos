from database import conexion
from models.lectura import Lectura


class LecturaRepository:
    def insertar(self, lectura):
        conexion.ejecutar(
            "INSERT INTO Lecturas (id_modulo, fecha_hora, nivel_agua, calidad_senal) "
            "VALUES (?, ?, ?, ?)",
            (lectura.id_modulo, lectura.fecha_hora, lectura.nivel_agua, lectura.calidad_senal),
        )

    def obtener_ultima_de_reservorio(self, id_reservorio):
        filas = conexion.consultar(
            "SELECT TOP 1 l.id_modulo, l.fecha_hora, l.nivel_agua, l.calidad_senal "
            "FROM Lecturas l INNER JOIN Modulo m ON m.id_modulo = l.id_modulo "
            "WHERE m.id_reservorio = ? ORDER BY l.fecha_hora DESC",
            (id_reservorio,),
        )
        if not filas:
            return None
        f = filas[0]
        return Lectura(f.id_modulo, f.fecha_hora, float(f.nivel_agua), f.calidad_senal)

    def listar_recientes(self, id_reservorio, cantidad=200):
        filas = conexion.consultar(
            "SELECT TOP (?) l.id_modulo, l.fecha_hora, l.nivel_agua, l.calidad_senal "
            "FROM Lecturas l INNER JOIN Modulo m ON m.id_modulo = l.id_modulo "
            "WHERE m.id_reservorio = ? ORDER BY l.fecha_hora DESC",
            (cantidad, id_reservorio),
        )
        lecturas = [Lectura(f.id_modulo, f.fecha_hora, float(f.nivel_agua), f.calidad_senal)
                    for f in filas]
        lecturas.reverse()
        return lecturas

    def insertar_consumo(self, id_reservorio, fecha_hora, caudal_salida):
        conexion.ejecutar(
            "INSERT INTO Consumo (id_reservorio, hora_fecha, caudal_salida) VALUES (?, ?, ?)",
            (id_reservorio, fecha_hora, caudal_salida),
        )
