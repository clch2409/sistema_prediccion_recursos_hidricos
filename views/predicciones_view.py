import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from views import componentes as c


class PrediccionesView(ttk.Frame):
    def __init__(self, padre, prediccion_controller):
        super().__init__(padre)
        self.controller = prediccion_controller
        self.reservorios = []

        arriba = ttk.Frame(self)
        arriba.pack(fill="x", padx=8, pady=8)

        ttk.Label(arriba, text="Reservorio:").grid(row=0, column=0, sticky="w")
        self.combo = ttk.Combobox(arriba, state="readonly", width=20)
        self.combo.grid(row=1, column=0, padx=(0, 20))
        self.combo.bind("<<ComboboxSelected>>", lambda evento: self.actualizar())

        self.lbl_capacidad = self._crear_tarjeta(arriba, "CAPACIDAD ACTUAL", 1)
        self.lbl_dias = self._crear_tarjeta(arriba, "DÍAS RESTANTES", 2)
        self.lbl_consumo = self._crear_tarjeta(arriba, "CONSUMO PROMEDIO", 3)

        self.figura = Figure(figsize=(7, 3.6), dpi=100)
        self.eje = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    def _crear_tarjeta(self, padre, titulo, columna):
        marco = ttk.LabelFrame(padre, text=titulo, padding=8)
        marco.grid(row=0, column=columna, rowspan=2, padx=8, sticky="nsew")
        etiqueta = ttk.Label(marco, text="-", font=("Arial", 14, "bold"), foreground=c.COLOR_OK)
        etiqueta.pack()
        return etiqueta

    def _cargar_combo(self):
        if self.reservorios:
            return
        self.reservorios = self.controller.listar_reservorios()
        self.combo["values"] = [r.nombre for r in self.reservorios]
        if self.reservorios:
            self.combo.current(0)

    def actualizar(self):
        self._cargar_combo()
        if not self.reservorios:
            return
        reservorio = self.reservorios[self.combo.current()]
        reservorio, prediccion = self.controller.predecir(reservorio.id_reservorio)

        self.eje.clear()
        self.eje.set_ylabel("% CAPACIDAD")
        self.eje.set_ylim(0, 100)
        self.eje.set_title(reservorio.nombre)

        if prediccion is None:
            self.lbl_capacidad.config(text="-" if reservorio.porcentaje is None
                                      else f"{reservorio.porcentaje:.0f}%")
            self.lbl_dias.config(text="Sin datos suficientes")
            self.lbl_consumo.config(text="-")
        else:
            tabla = prediccion["tabla"]
            self.eje.plot(tabla["fecha"], tabla["nivel"], marker="o", label="Lecturas")
            self.eje.plot([prediccion["fecha_ultima"], prediccion["fecha_limite"]],
                          [prediccion["nivel_actual"], 0], linestyle="--", color="red",
                          label="Proyección")
            self.eje.legend()

            litros = reservorio.litros_actuales()
            self.lbl_capacidad.config(text=f"{prediccion['nivel_actual']:.0f}%  ({litros:,.0f} L)")
            self.lbl_dias.config(
                text=f"{prediccion['dias_restantes']:.1f} días\n"
                     f"Límite: {prediccion['fecha_limite']:%d/%m/%Y %H:%M}")
            self.lbl_consumo.config(text=f"{prediccion['consumo_litros_hora']:,.0f} L/h")

        self.figura.autofmt_xdate()
        self.canvas.draw()
