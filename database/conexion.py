import pyodbc

import config

# Error que lanza SQL Server al violar una llave foránea o un UNIQUE
ErrorIntegridad = pyodbc.IntegrityError


def obtener_conexion():
    return pyodbc.connect(config.CADENA_CONEXION)


def consultar(sql, parametros=()):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        return cursor.fetchall()
    finally:
        conexion.close()


def ejecutar(sql, parametros=()):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        conexion.commit()
        return cursor.rowcount
    finally:
        conexion.close()
