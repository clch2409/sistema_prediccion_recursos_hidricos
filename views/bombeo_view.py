"""views/bombeo_view.py - Horas de operación y ciclos de las bombas."""
from tkinter import ttk

import config
from views import componentes as c


class BombeoView(ttk.Frame):

    def __init__(self, padre, bombeo_controller):
        super().__init__(padre)
        self.controller = bombeo_controller

        ttk.Label(self, text="Sistemas de bombeo", font=("Arial", 14, "bold")).pack(anchor="w", padx=8, pady=8)
        ttk.Label(self, text=(f"Mtto menor: {config.HORAS_MTTO_MENOR} h   |   "
                              f"Mtto mayor: {config.HORAS_MTTO_MAYOR} h   |   "
                              f"Vida útil: {config.HORAS_VIDA_UTIL:,} h")).pack(anchor="w", padx=8)

        marco, self.tabla = c.crear_tabla(
            self,
            ["DESCRIPCIÓN", "HORAS OPERACIÓN", "CICLOS (ÚLTIMOS 60 MIN)", "VIDA ÚTIL", "MANTENIMIENTO", "ESTADO"],
            [120, 130, 170, 100, 130, 100],
        )
        marco.pack(fill="both", expand=True, padx=8, pady=8)

    def actualizar(self):
        filas = []
        for b in self.controller.listar_bombas():
            riesgo = b.ciclos_ultima_hora > config.MAX_CICLOS_HORA
            mtto = b.necesita_mantenimiento() or "-"
            valores = (b.nombre_reservorio, f"{b.horas_operacion:,.0f}", b.ciclos_ultima_hora,
                       f"{b.vida_util_restante_pct():.0f}%", mtto, "ACTIVO" if b.estado else "INACTIVO")
            filas.append((valores, "malo" if riesgo else "ok"))
        c.llenar_tabla(self.tabla, filas)
