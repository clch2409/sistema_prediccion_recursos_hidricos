from tkinter import ttk

from views import componentes as c


class ReservoriosView(ttk.Frame):
    def __init__(self, padre, reservorio_controller):
        super().__init__(padre)
        self.controller = reservorio_controller

        ttk.Label(self, text="Reservorios", font=("Arial", 14, "bold")).pack(anchor="w", padx=8, pady=8)
        c.crear_barra_crud(self, self.nuevo, self.editar, self.eliminar).pack(anchor="w", padx=8)
        marco, self.tabla = c.crear_tabla(
            self,
            ["DESCRIPCIÓN", "CAPACIDAD (L)", "UBICACIÓN", "CONSTRUCCIÓN", "% LLENADO", "ÚLTIMA LECTURA"],
            [110, 110, 330, 100, 90, 140],
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
            valores = (r.nombre, f"{r.capacidad_maxima:,.0f}", r.ubicacion or "-",
                       c.formatear_fecha_corta(r.fecha_construccion),
                       texto_pct, c.formatear_fecha(r.ultima_lectura))
            filas.append((valores, etiqueta, r.id_reservorio))
        c.llenar_tabla(self.tabla, filas)

    def _campos(self, reservorio=None):
        fecha = reservorio.fecha_construccion if reservorio else None
        return [
            {"clave": "nombre", "etiqueta": "Nombre", "tipo": "texto",
             "valor": reservorio.nombre if reservorio else ""},
            {"clave": "capacidad", "etiqueta": "Capacidad máxima (L)", "tipo": "numero",
             "valor": f"{reservorio.capacidad_maxima:g}" if reservorio else ""},
            {"clave": "ubicacion", "etiqueta": "Ubicación", "tipo": "texto",
             "valor": (reservorio.ubicacion or "") if reservorio else ""},
            {"clave": "fecha", "etiqueta": "Fecha construcción (AAAA-MM-DD)", "tipo": "fecha",
             "valor": fecha.strftime("%Y-%m-%d") if fecha else ""},
        ]

    def nuevo(self):
        def guardar(v):
            self.controller.crear_reservorio(v["nombre"], v["capacidad"], v["ubicacion"], v["fecha"])
            self.actualizar()
        c.FormularioDialogo(self, "Nuevo reservorio", self._campos(), guardar)

    def editar(self):
        iid = c.id_seleccionado(self.tabla, "un reservorio")
        if iid is None:
            return
        reservorio = c.consultar_con_aviso(lambda: self.controller.obtener_reservorio(int(iid)))
        if reservorio is None:
            return

        def guardar(v):
            self.controller.actualizar_reservorio(
                reservorio.id_reservorio, v["nombre"], v["capacidad"], v["ubicacion"], v["fecha"])
            self.actualizar()
        c.FormularioDialogo(self, "Editar reservorio", self._campos(reservorio), guardar)

    def eliminar(self):
        iid = c.id_seleccionado(self.tabla, "un reservorio")
        if iid is None:
            return
        nombre = self.tabla.item(iid, "values")[0]
        if not c.confirmar_eliminar(f"el reservorio «{nombre}»"):
            return
        if c.ejecutar_con_aviso(lambda: self.controller.eliminar_reservorio(int(iid))):
            self.actualizar()
