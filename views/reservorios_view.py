"""views/reservorios_view.py - Tabla con todos los reservorios y su último nivel."""
from tkinter import ttk

from views import componentes as c


class ReservoriosView(ttk.Frame):

    def __init__(self, padre, reservorio_controller):
        super().__init__(padre)
        self.controller = reservorio_controller

        ttk.Label(self, text="Reservorios", font=("Arial", 14, "bold")).pack(anchor="w", padx=8, pady=8)
        marco, self.tabla = c.crear_tabla(
            self,
            ["DESCRIPCIÓN", "CAPACIDAD (L)", "UBICACIÓN", "% LLENADO", "ÚLTIMA LECTURA"],
            [110, 110, 450, 90, 140],
        )
        marco.pack(fill="both", expand=True, padx=8, pady=8)

    def actualizar(self):
        filas = []
        for r in self.controller.listar_reservorios():
            if r.porcentaje is None:
                texto_pct, etiqueta = "-", ""
            else:
                texto_pct = f"{r.porcentaje:.0f}%"
                etiqueta = "malo" if r.porcentaje < 10 else "ok"
            valores = (r.nombre, f"{r.capacidad_maxima:,.0f}", r.ubicacion,
                       texto_pct, c.formatear_fecha(r.ultima_lectura))
            filas.append((valores, etiqueta))
        c.llenar_tabla(self.tabla, filas)
