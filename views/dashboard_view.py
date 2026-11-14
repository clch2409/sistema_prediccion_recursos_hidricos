"""views/dashboard_view.py - Pantalla Dashboard: alertas, reservas actuales y vida útil de bombas."""
import tkinter as tk
from tkinter import ttk

from views import componentes as c


class DashboardView(ttk.Frame):

    def __init__(self, padre, dashboard_controller):
        super().__init__(padre)
        self.controller = dashboard_controller

        # ---------- Columna izquierda: ALERTAS ----------
        izquierda = ttk.LabelFrame(self, text="ALERTAS", padding=10)
        izquierda.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.cuadros_alerta = []
        for _ in range(3):
            etiqueta = tk.Label(izquierda, text="", bg=c.COLOR_ALERTA_FONDO, fg="white",
                                font=("Arial", 10, "italic"), justify="left",
                                wraplength=330, anchor="w", padx=10, pady=10)
            etiqueta.pack(fill="x", pady=6)
            self.cuadros_alerta.append(etiqueta)

        # ---------- Columna central: RESERVAS ACTUALES ----------
        centro = ttk.LabelFrame(self, text="RESERVAS ACTUALES", padding=10)
        centro.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        self.barras_reservas = [self._crear_barra(centro) for _ in range(3)]

        # ---------- Columna derecha: VIDA ÚTIL DE LAS BOMBAS ----------
        derecha = ttk.LabelFrame(self, text="SISTEMAS DE BOMBEO - VIDA ÚTIL RESTANTE", padding=10)
        derecha.grid(row=0, column=2, sticky="nsew", padx=8, pady=8)
        self.barras_vida = [self._crear_barra(derecha) for _ in range(2)]

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

    def _crear_barra(self, padre):
        """Crea un grupo: texto + barra de progreso + porcentaje. Devuelve los 3 widgets."""
        titulo = ttk.Label(padre, text="-", font=("Arial", 10, "bold"))
        titulo.pack(pady=(10, 2))
        barra = ttk.Progressbar(padre, length=200, maximum=100)
        barra.pack()
        porcentaje = ttk.Label(padre, text="- %", font=("Arial", 14))
        porcentaje.pack(pady=(2, 10))
        return titulo, barra, porcentaje

    def _actualizar_barra(self, grupo, nombre, valor):
        titulo, barra, porcentaje = grupo
        titulo.config(text=nombre)
        barra["value"] = valor
        porcentaje.config(text=f"{valor:.0f} %", foreground=c.COLOR_MALO if valor < 10 else c.COLOR_OK)

    def actualizar(self):
        # Alertas
        textos = self.controller.obtener_textos_alertas()
        for etiqueta, texto in zip(self.cuadros_alerta, textos):
            etiqueta.config(text=texto)

        # Reservas actuales
        reservas = self.controller.obtener_reservas()
        if reservas:
            for grupo, (nombre, valor) in zip(self.barras_reservas, reservas):
                self._actualizar_barra(grupo, nombre, valor)

        # Vida útil de bombas
        for grupo, (nombre, valor) in zip(self.barras_vida, self.controller.obtener_vida_util()):
            self._actualizar_barra(grupo, nombre, valor)
