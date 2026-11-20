from database import conexion
from models.bomba import SistemaBombeo


def _fila_a_bomba(fila):
    return SistemaBombeo(
        id_bomba=fila.id_bomba,
        id_reservorio=fila.id_reservorio,
        nombre=fila.nombre,
        modelo=fila.modelo,
        caudal_l_s=float(fila.caudal_l_s or 0),
        consumo_kw=float(fila.consumo_kw or 0),
        estado=bool(fila.estado),
        horas_iniciales=float(fila.horas_iniciales or 0),
    )


_COLUMNAS_BOMBA = ("b.id_bomba, b.id_reservorio, b.nombre, b.modelo, "
                   "b.caudal_L_s AS caudal_l_s, b.consumo_kw, b.estado, b.horas_iniciales")


class BombaRepository:
    def listar(self):
        filas = conexion.consultar(
            f"SELECT {_COLUMNAS_BOMBA}, r.nombre AS nombre_reservorio, r.ubicacion "
            "FROM Sistema_Bombeo b INNER JOIN Reservorio r ON r.id_reservorio = b.id_reservorio "
            "ORDER BY b.id_bomba"
        )
        bombas = []
        for f in filas:
            bomba = _fila_a_bomba(f)
            bomba.nombre_reservorio = f.nombre_reservorio
            bomba.ubicacion = f.ubicacion
            bombas.append(bomba)
        return bombas

    def obtener_por_reservorio(self, id_reservorio):
        filas = conexion.consultar(
            f"SELECT {_COLUMNAS_BOMBA} FROM Sistema_Bombeo b WHERE b.id_reservorio = ?",
            (id_reservorio,)
        )
        if not filas:
            return None
        return _fila_a_bomba(filas[0])

    def obtener_ciclo_abierto(self, id_bomba):
        filas = conexion.consultar(
            "SELECT TOP 1 id_historial, fecha_hora_encendido FROM Historia_Bombeo "
            "WHERE id_bomba = ? AND fecha_hora_apagado IS NULL "
            "ORDER BY fecha_hora_encendido DESC",
            (id_bomba,),
        )
        if not filas:
            return None
        return filas[0].id_historial, filas[0].fecha_hora_encendido

    def abrir_ciclo(self, id_bomba, ahora):
        conexion.ejecutar(
            "INSERT INTO Historia_Bombeo (id_bomba, fecha_hora_encendido) VALUES (?, ?)",
            (id_bomba, ahora),
        )

    def cerrar_ciclo(self, id_historial, ahora, volumen_inyectado):
        conexion.ejecutar(
            "UPDATE Historia_Bombeo SET fecha_hora_apagado = ?, volumen_inyectado_estimado = ? "
            "WHERE id_historial = ?",
            (ahora, volumen_inyectado, id_historial),
        )

    def contar_ciclos_ultima_hora(self, id_bomba, ahora):
        filas = conexion.consultar(
            "SELECT COUNT(*) AS total FROM Historia_Bombeo "
            "WHERE id_bomba = ? AND fecha_hora_encendido >= DATEADD(MINUTE, -60, ?)",
            (id_bomba, ahora),
        )
        return filas[0].total

    def horas_operacion(self, id_bomba, horas_iniciales, ahora):
        filas = conexion.consultar(
            "SELECT ISNULL(SUM(DATEDIFF(SECOND, fecha_hora_encendido, "
            "                           ISNULL(fecha_hora_apagado, ?))), 0) AS segundos "
            "FROM Historia_Bombeo WHERE id_bomba = ?",
            (ahora, id_bomba),
        )
        return horas_iniciales + filas[0].segundos / 3600
