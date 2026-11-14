"""
database/conexion.py
Funciones básicas para hablar con SQL Server usando pyodbc.

Cada función abre una conexión, ejecuta y la cierra. Es simple y evita problemas
porque MQTT trabaja en un hilo distinto al de la ventana (Tkinter).
"""
import pyodbc

import config


def obtener_conexion():
    """Abre una conexión nueva a la base de datos."""
    return pyodbc.connect(config.CADENA_CONEXION)


def consultar(sql, parametros=()):
    """Ejecuta un SELECT y devuelve la lista de filas."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        return cursor.fetchall()
    finally:
        conexion.close()


def ejecutar(sql, parametros=()):
    """Ejecuta un INSERT / UPDATE / DELETE y confirma los cambios (commit)."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        conexion.commit()
        return cursor.rowcount
    finally:
        conexion.close()
