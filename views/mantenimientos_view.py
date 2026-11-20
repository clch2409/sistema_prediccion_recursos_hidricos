from datetime import date
from tkinter import ttk

from views import componentes as c


class MantenimientosView(ttk.Frame):
    def __init__(self, padre, mantenimiento_controller):
        super().__init__(padre)
        self.controller = mantenimiento_controller

        ttk.Label(self, text="Mantenimientos", font=("Arial", 14, "bold")).pack(anchor="w", padx=8, pady=8)
        c.crear_barra_crud(self, self.nuevo, self.editar, self.eliminar).pack(anchor="w", padx=8)
        marco, self.tabla = c.crear_tabla(
            self,
            ["FECHA", "RESERVORIO", "BOMBA", "COSTO", "DESCRIPCIÓN"],
            [100, 110, 110, 100, 420],
        )
        self.tabla.column("DESCRIPCIÓN", anchor="w")
        marco.pack(fill="both", expand=True, padx=8, pady=8)

    def actualizar(self):
        filas = []
        for m in self.controller.listar_mantenimientos():
            resumen = " ".join(m.descripcion.split())
            if len(resumen) > 80:
                resumen = resumen[:77] + "..."
            valores = (c.formatear_fecha_corta(m.fecha_intervencion), m.nombre_reservorio,
                       m.nombre_bomba, f"{m.costo:,.2f}", resumen)
            filas.append((valores, "", m.id_mantenimiento))
        c.llenar_tabla(self.tabla, filas)

    def _campos(self, mantenimiento=None):
        bombas = self.controller.listar_bombas()
        if not bombas:
            raise ValueError("Primero debe registrar al menos un sistema de bombeo.")
        fecha = mantenimiento.fecha_intervencion if mantenimiento else date.today()
        return [
            {"clave": "id_bomba", "etiqueta": "Sistema de bombeo", "tipo": "combo",
             "opciones": bombas, "valor": mantenimiento.id_bomba if mantenimiento else None},
            {"clave": "fecha", "etiqueta": "Fecha intervención (AAAA-MM-DD)", "tipo": "fecha",
             "valor": fecha.strftime("%Y-%m-%d") if fecha else ""},
            {"clave": "costo", "etiqueta": "Costo", "tipo": "numero",
             "valor": f"{mantenimiento.costo:g}" if mantenimiento else "0"},
            {"clave": "descripcion", "etiqueta": "Descripción", "tipo": "texto_largo",
             "valor": mantenimiento.descripcion if mantenimiento else ""},
        ]

    def nuevo(self):
        campos = c.consultar_con_aviso(self._campos)
        if campos is None:
            return

        def guardar(v):
            self.controller.crear_mantenimiento(v["id_bomba"], v["costo"], v["descripcion"], v["fecha"])
            self.actualizar()
        c.FormularioDialogo(self, "Nuevo mantenimiento", campos, guardar)

    def editar(self):
        iid = c.id_seleccionado(self.tabla, "un mantenimiento")
        if iid is None:
            return
        mantenimiento = c.consultar_con_aviso(
            lambda: self.controller.obtener_mantenimiento(int(iid)))
        if mantenimiento is None:
            return
        campos = c.consultar_con_aviso(lambda: self._campos(mantenimiento))
        if campos is None:
            return

        def guardar(v):
            self.controller.actualizar_mantenimiento(
                mantenimiento.id_mantenimiento, v["id_bomba"], v["costo"], v["descripcion"], v["fecha"])
            self.actualizar()
        c.FormularioDialogo(self, "Editar mantenimiento", campos, guardar)

    def eliminar(self):
        iid = c.id_seleccionado(self.tabla, "un mantenimiento")
        if iid is None:
            return
        fecha = self.tabla.item(iid, "values")[0]
        if not c.confirmar_eliminar(f"el mantenimiento del {fecha}"):
            return
        if c.ejecutar_con_aviso(lambda: self.controller.eliminar_mantenimiento(int(iid))):
            self.actualizar()
