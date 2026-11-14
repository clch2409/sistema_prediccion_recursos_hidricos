"""
views/main_window.py
Ventana principal: menú lateral a la izquierda y la pantalla elegida a la derecha.
También tiene el "reloj" que cada 5 segundos revisa los latidos y refresca la pantalla visible.
"""
import tkinter as tk
from tkinter import ttk

import config
from views import componentes as c
from views.bombeo_view import BombeoView
from views.dashboard_view import DashboardView
from views.modulos_view import ModulosView
from views.predicciones_view import PrediccionesView
from views.reservorios_view import ReservoriosView


class VentanaPrincipal(ttk.Frame):

    def __init__(self, raiz, controladores):
        """'controladores' es un diccionario creado en main.py."""
        super().__init__(raiz)
        self.raiz = raiz
        self.controladores = controladores

        # Título superior
        tk.Label(self, text="Sistema de Gestión y Predicción de Reservas Hídricas",
                 bg=c.COLOR_FONDO_TITULO, fg="white", font=("Arial", 16, "bold"),
                 pady=12).pack(fill="x")

        cuerpo = ttk.Frame(self)
        cuerpo.pack(fill="both", expand=True)

        # Menú lateral
        menu = tk.Frame(cuerpo, bg="white", width=190)
        menu.pack(side="left", fill="y")
        menu.pack_propagate(False)

        # Zona donde se muestran las pantallas
        self.zona = ttk.Frame(cuerpo)
        self.zona.pack(side="left", fill="both", expand=True)

        # Creamos todas las pantallas una sola vez y las apilamos
        self.pantallas = {
            "DASHBOARD": DashboardView(self.zona, controladores["dashboard"]),
            "RESERVORIOS": ReservoriosView(self.zona, controladores["reservorio"]),
            "ESTADO MÓDULOS": ModulosView(self.zona, controladores["reservorio"]),
            "PREDICCIONES": PrediccionesView(self.zona, controladores["prediccion"]),
            "SISTEMAS DE BOMBEO": BombeoView(self.zona, controladores["bombeo"]),
        }
        self.botones = {}
        for nombre, pantalla in self.pantallas.items():
            pantalla.place(relx=0, rely=0, relwidth=1, relheight=1)
            boton = tk.Button(menu, text=nombre, bg=c.COLOR_BOTON, fg="white",
                              font=("Arial", 10, "bold"), relief="flat", pady=10,
                              command=lambda n=nombre: self.mostrar(n))
            boton.pack(fill="x", padx=10, pady=6)
            self.botones[nombre] = boton

        self.pantalla_actual = "DASHBOARD"
        self.mostrar("DASHBOARD")
        self._refrescar()

    def mostrar(self, nombre):
        """Trae al frente la pantalla elegida y pinta de verde su botón."""
        self.pantalla_actual = nombre
        self.pantallas[nombre].tkraise()
        for n, boton in self.botones.items():
            boton.config(bg=c.COLOR_BOTON_ACTIVO if n == nombre else c.COLOR_BOTON)
        self.pantallas[nombre].actualizar()

    def _refrescar(self):
        """Se ejecuta cada INTERVALO_REFRESCO_MS: revisa latidos y actualiza la pantalla."""
        try:
            self.controladores["mensajes"].revisar_latidos()
            self.pantallas[self.pantalla_actual].actualizar()
        except Exception as error:
            print(f"[Ventana] Error al refrescar: {error}")
        self.raiz.after(config.INTERVALO_REFRESCO_MS, self._refrescar)
