from tkinter import ttk

from views import componentes as c


class UsuariosView(ttk.Frame):
    def __init__(self, padre, usuario_controller):
        super().__init__(padre)
        self.controller = usuario_controller

        ttk.Label(self, text="Usuarios", font=("Arial", 14, "bold")).pack(anchor="w", padx=8, pady=8)
        c.crear_barra_crud(self, self.nuevo, self.editar, self.eliminar).pack(anchor="w", padx=8)
        marco, self.tabla = c.crear_tabla(self, ["ID", "USUARIO", "TIPO DE USUARIO"], [60, 250, 200])
        marco.pack(fill="both", expand=True, padx=8, pady=8)

    def actualizar(self):
        filas = [((u.id_usuario, u.usuario, u.tipo), "", u.id_usuario)
                 for u in self.controller.listar_usuarios()]
        c.llenar_tabla(self.tabla, filas)

    def _campos(self, usuario=None):
        tipos = self.controller.listar_tipos()
        if not tipos:
            raise ValueError("Primero debe haber al menos un tipo de usuario registrado.")
        campos = [
            {"clave": "usuario", "etiqueta": "Usuario", "tipo": "texto",
             "valor": usuario.usuario if usuario else ""},
            {"clave": "id_tipo", "etiqueta": "Tipo de usuario", "tipo": "combo",
             "opciones": tipos, "valor": usuario.id_tipo_usuario if usuario else None},
            {"clave": "contrasena",
             "etiqueta": "Nueva contraseña" if usuario else "Contraseña", "tipo": "clave"},
            {"clave": "confirmacion", "etiqueta": "Confirmar contraseña", "tipo": "clave"},
        ]
        if usuario:
            campos.append({"clave": "_ayuda", "etiqueta": "", "tipo": "texto", "editable": False,
                           "valor": "Deje la contraseña vacía para conservar la actual"})
        return campos

    def nuevo(self):
        campos = c.consultar_con_aviso(self._campos)
        if campos is None:
            return

        def guardar(v):
            self.controller.crear_usuario(v["usuario"], v["id_tipo"], v["contrasena"], v["confirmacion"])
            self.actualizar()
        c.FormularioDialogo(self, "Nuevo usuario", campos, guardar)

    def editar(self):
        iid = c.id_seleccionado(self.tabla, "un usuario")
        if iid is None:
            return
        usuario = c.consultar_con_aviso(lambda: self.controller.obtener_usuario(int(iid)))
        if usuario is None:
            return
        campos = c.consultar_con_aviso(lambda: self._campos(usuario))
        if campos is None:
            return

        def guardar(v):
            self.controller.actualizar_usuario(usuario.id_usuario, v["usuario"], v["id_tipo"],
                                               v["contrasena"], v["confirmacion"])
            self.actualizar()
        c.FormularioDialogo(self, "Editar usuario", campos, guardar)

    def eliminar(self):
        iid = c.id_seleccionado(self.tabla, "un usuario")
        if iid is None:
            return
        nombre = self.tabla.item(iid, "values")[1]
        if not c.confirmar_eliminar(f"el usuario «{nombre}»"):
            return
        if c.ejecutar_con_aviso(lambda: self.controller.eliminar_usuario(int(iid))):
            self.actualizar()
