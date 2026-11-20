import tkinter as tk
from tkinter import ttk

COLOR_FONDO_TITULO = "#1d3f66"
COLOR_BOTON = "#1d3a5c"
COLOR_BOTON_ACTIVO = "#059669"
COLOR_PANEL = "#667790"
COLOR_OK = "#059669"
COLOR_MALO = "#dc2626"
COLOR_ALERTA_FONDO = "#2a1a1a"


def crear_tabla(padre, columnas, anchos):
    marco = ttk.Frame(padre)
    tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=12)
    for columna, ancho in zip(columnas, anchos):
        tabla.heading(columna, text=columna)
        tabla.column(columna, width=ancho, anchor="center")
    barra = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=barra.set)
    tabla.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    tabla.tag_configure("ok", foreground=COLOR_OK)
    tabla.tag_configure("malo", foreground=COLOR_MALO)
    return marco, tabla


def llenar_tabla(tabla, filas):
    for item in tabla.get_children():
        tabla.delete(item)
    for valores, etiqueta in filas:
        tabla.insert("", "end", values=valores, tags=(etiqueta,))


def formatear_fecha(fecha):
    if fecha is None:
        return "-"
    return fecha.strftime("%d/%m/%Y %H:%M")
