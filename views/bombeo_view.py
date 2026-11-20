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
        c.crear_barra_crud(self, self.nuevo, self.editar, self.eliminar).pack(anchor="w", padx=8, pady=(8, 0))

        marco, self.tabla = c.crear_tabla(
            self,
            ["RESERVORIO", "BOMBA", "MODELO", "HORAS OPERACIÓN", "CICLOS (ÚLTIMOS 60 MIN)",
             "VIDA ÚTIL", "MANTENIMIENTO", "ESTADO"],
            [100, 100, 100, 110, 150, 80, 110, 80],
        )
        marco.pack(fill="both", expand=True, padx=8, pady=8)

    def actualizar(self):
        filas = []
        for b in self.controller.listar_bombas():
            riesgo = b.ciclos_ultima_hora > config.MAX_CICLOS_HORA
            mtto = b.necesita_mantenimiento() or "-"
            valores = (b.nombre_reservorio, b.nombre, b.modelo, f"{b.horas_operacion:,.0f}",
                       b.ciclos_ultima_hora, f"{b.vida_util_restante_pct():.0f}%", mtto,
                       "ACTIVO" if b.estado else "INACTIVO")
            filas.append((valores, "malo" if riesgo else "ok", b.id_bomba))
        c.llenar_tabla(self.tabla, filas)

    def _campos(self, bomba=None):
        reservorios = self.controller.listar_reservorios()
        if not reservorios:
            raise ValueError("Primero debe registrar al menos un reservorio.")
        return [
            {"clave": "id_reservorio", "etiqueta": "Reservorio", "tipo": "combo",
             "opciones": reservorios, "valor": bomba.id_reservorio if bomba else None},
            {"clave": "nombre", "etiqueta": "Nombre", "tipo": "texto",
             "valor": bomba.nombre if bomba else ""},
            {"clave": "modelo", "etiqueta": "Modelo", "tipo": "texto",
             "valor": bomba.modelo if bomba else ""},
            {"clave": "caudal", "etiqueta": "Caudal (L/s)", "tipo": "numero",
             "valor": f"{bomba.caudal_l_s:g}" if bomba else ""},
            {"clave": "consumo", "etiqueta": "Consumo (kW)", "tipo": "numero",
             "valor": f"{bomba.consumo_kw:g}" if bomba else ""},
            {"clave": "horas", "etiqueta": "Horas iniciales", "tipo": "numero",
             "valor": f"{bomba.horas_iniciales:g}" if bomba else "0"},
            {"clave": "estado", "etiqueta": "Activa", "tipo": "bool",
             "valor": bomba.estado if bomba else True},
        ]

    def nuevo(self):
        campos = c.consultar_con_aviso(self._campos)
        if campos is None:
            return

        def guardar(v):
            self.controller.crear_bomba(v["id_reservorio"], v["nombre"], v["modelo"], v["caudal"],
                                        v["consumo"], v["estado"], v["horas"])
            self.actualizar()
        c.FormularioDialogo(self, "Nuevo sistema de bombeo", campos, guardar)

    def editar(self):
        iid = c.id_seleccionado(self.tabla, "un sistema de bombeo")
        if iid is None:
            return
        bomba = c.consultar_con_aviso(lambda: self.controller.obtener_bomba(int(iid)))
        if bomba is None:
            return
        campos = c.consultar_con_aviso(lambda: self._campos(bomba))
        if campos is None:
            return

        def guardar(v):
            self.controller.actualizar_bomba(bomba.id_bomba, v["id_reservorio"], v["nombre"],
                                             v["modelo"], v["caudal"], v["consumo"], v["estado"],
                                             v["horas"])
            self.actualizar()
        c.FormularioDialogo(self, "Editar sistema de bombeo", campos, guardar)

    def eliminar(self):
        iid = c.id_seleccionado(self.tabla, "un sistema de bombeo")
        if iid is None:
            return
        nombre = self.tabla.item(iid, "values")[1]
        if not c.confirmar_eliminar(f"el sistema de bombeo «{nombre}»"):
            return
        if c.ejecutar_con_aviso(lambda: self.controller.eliminar_bomba(int(iid))):
            self.actualizar()
