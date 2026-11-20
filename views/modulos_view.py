from tkinter import ttk

from views import componentes as c


class ModulosView(ttk.Frame):
    def __init__(self, padre, modulo_controller):
        super().__init__(padre)
        self.controller = modulo_controller

        ttk.Label(self, text="Estado de módulos", font=("Arial", 14, "bold")).pack(anchor="w", padx=8, pady=8)
        c.crear_barra_crud(self, self.nuevo, self.editar, self.eliminar).pack(anchor="w", padx=8)
        marco, self.tabla = c.crear_tabla(
            self,
            ["CÓDIGO", "NOMBRE", "RESERVORIO", "TIPO", "ALTURA (cm)", "ESTADO", "TIMESTAMP ESTADO"],
            [150, 130, 110, 120, 90, 90, 140],
        )
        marco.pack(fill="both", expand=True, padx=8, pady=8)

    def actualizar(self):
        filas = []
        for m in self.controller.listar_modulos():
            etiqueta = "ok" if m.estado else "malo"
            texto_estado = "ACTIVO" if m.estado else "INACTIVO"
            valores = (m.id_modulo, m.nombre_modulo, m.nombre_reservorio, m.tipo,
                       f"{m.altura_instalacion:g}", texto_estado, c.formatear_fecha(m.fecha_estado))
            filas.append((valores, etiqueta, m.id_modulo))
        c.llenar_tabla(self.tabla, filas)

    def _campos(self, modulo=None):
        reservorios = self.controller.listar_reservorios()
        tipos = self.controller.listar_tipos()
        if not reservorios or not tipos:
            raise ValueError("Primero debe haber al menos un reservorio y un tipo de módulo "
                             "registrados.")
        return [
            {"clave": "id_modulo", "etiqueta": "Código del módulo", "tipo": "texto",
             "valor": modulo.id_modulo if modulo else "", "editable": modulo is None},
            {"clave": "nombre", "etiqueta": "Nombre", "tipo": "texto",
             "valor": modulo.nombre_modulo if modulo else ""},
            {"clave": "id_reservorio", "etiqueta": "Reservorio", "tipo": "combo",
             "opciones": reservorios, "valor": modulo.id_reservorio if modulo else None},
            {"clave": "id_tipo", "etiqueta": "Tipo de módulo", "tipo": "combo",
             "opciones": tipos, "valor": modulo.id_tipo_modulo if modulo else None},
            {"clave": "altura", "etiqueta": "Altura de instalación (cm)", "tipo": "numero",
             "valor": f"{modulo.altura_instalacion:g}" if modulo else ""},
            {"clave": "estado", "etiqueta": "Activo", "tipo": "bool",
             "valor": modulo.estado if modulo else True},
        ]

    def nuevo(self):
        campos = c.consultar_con_aviso(self._campos)
        if campos is None:
            return

        def guardar(v):
            self.controller.crear_modulo(v["id_modulo"], v["id_reservorio"], v["id_tipo"],
                                         v["nombre"], v["altura"], v["estado"])
            self.actualizar()
        c.FormularioDialogo(self, "Nuevo módulo", campos, guardar)

    def editar(self):
        iid = c.id_seleccionado(self.tabla, "un módulo")
        if iid is None:
            return
        modulo = c.consultar_con_aviso(lambda: self.controller.obtener_modulo(iid))
        if modulo is None:
            return
        campos = c.consultar_con_aviso(lambda: self._campos(modulo))
        if campos is None:
            return

        def guardar(v):
            self.controller.actualizar_modulo(modulo.id_modulo, v["id_reservorio"], v["id_tipo"],
                                              v["nombre"], v["altura"], v["estado"])
            self.actualizar()
        c.FormularioDialogo(self, "Editar módulo", campos, guardar)

    def eliminar(self):
        iid = c.id_seleccionado(self.tabla, "un módulo")
        if iid is None:
            return
        if not c.confirmar_eliminar(f"el módulo «{iid}»"):
            return
        if c.ejecutar_con_aviso(lambda: self.controller.eliminar_modulo(iid)):
            self.actualizar()
