import config
from database.conexion import ErrorIntegridad
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from services.seguridad import encriptar_contrasena


class UsuarioController:
    def __init__(self, login_controller):
        self.usuario_repo = UsuarioRepository()
        self.login_controller = login_controller

    def listar_usuarios(self):
        return self.usuario_repo.listar()

    def listar_tipos(self):
        return self.usuario_repo.listar_tipos()

    def obtener_usuario(self, id_usuario):
        usuario = self.usuario_repo.obtener_por_id(id_usuario)
        if usuario is None:
            raise ValueError("El usuario ya no existe")
        return usuario

    @staticmethod
    def _validar_contrasena(contrasena, confirmacion):
        if len(contrasena) < config.LONGITUD_MIN_CONTRASENA:
            raise ValueError(
                f"La contraseña debe tener al menos {config.LONGITUD_MIN_CONTRASENA} caracteres")
        if contrasena != confirmacion:
            raise ValueError("Las contraseñas no coinciden")

    def crear_usuario(self, usuario, id_tipo_usuario, contrasena, confirmacion):
        nuevo = Usuario(None, id_tipo_usuario, usuario)
        self._validar_contrasena(contrasena or "", confirmacion or "")
        if self.usuario_repo.existe_usuario(nuevo.usuario):
            raise ValueError(f"Ya existe un usuario llamado {nuevo.usuario}")
        # la contraseña nunca se guarda en texto plano
        self.usuario_repo.insertar(nuevo, encriptar_contrasena(contrasena))

    def actualizar_usuario(self, id_usuario, usuario, id_tipo_usuario, contrasena=None,
                           confirmacion=None):
        existente = self.obtener_usuario(id_usuario)
        existente.usuario = usuario
        existente.id_tipo_usuario = id_tipo_usuario
        if contrasena or confirmacion:
            self._validar_contrasena(contrasena or "", confirmacion or "")
        if self.usuario_repo.existe_usuario(existente.usuario, excepto_id=id_usuario):
            raise ValueError(f"Ya existe un usuario llamado {existente.usuario}")
        self.usuario_repo.actualizar(existente)
        if contrasena:
            self.usuario_repo.actualizar_contrasena(id_usuario, encriptar_contrasena(contrasena))

    def eliminar_usuario(self, id_usuario):
        actual = self.login_controller.usuario_actual
        if actual is not None and actual.id_usuario == id_usuario:
            raise ValueError("No puede eliminar el usuario con el que inició sesión")
        if len(self.usuario_repo.listar()) <= 1:
            raise ValueError("No se puede eliminar el último usuario del sistema")
        try:
            self.usuario_repo.eliminar(id_usuario)
        except ErrorIntegridad:
            raise ValueError("No se puede eliminar el usuario porque tiene registros asociados")
