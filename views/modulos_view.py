"""views/modulos_view.py - Estado de los módulos emisores y receptores."""
from tkinter import ttk

from views import componentes as c


class ModulosView(ttk.Frame):

    def __init__(self, padre, reservorio_controller):
        super().__init__(padre)
        self.controller = reservorio_controller

        ttk.Label(self, text="Estado de módulos", font=("Arial", 14, "bold")).pack(anchor="w", padx=8, pady=8)
        marco, self.tabla = c.crear_tabla(
            self,
            ["DESCRIPCIÓN", "TIPO", "ESTADO", "TIMESTAMP ESTADO"],
            [160, 160, 120, 200],
        )
        marco.pack(fill="both", expand=True, padx=8, pady=8)

    def actualizar(self):
        filas = []
        for m in self.controller.listar_modulos():
            etiqueta = "ok" if m.estado else "malo"
            texto_estado = "ACTIVO" if m.estado else "INACTIVO"
            valores = (m.nombre_reservorio, m.tipo, texto_estado, c.formatear_fecha(m.fecha_estado))
            filas.append((valores, etiqueta))
        c.llenar_tabla(self.tabla, filas)
