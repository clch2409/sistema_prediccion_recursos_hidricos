from repositories.usuario_repository import UsuarioRepository
from services.seguridad import encriptar_contrasena, esta_encriptada, verificar_contrasena


class LoginController:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
        self.usuario_actual = None

    def iniciar_sesion(self, usuario, contrasena):
        if not usuario or not contrasena:
            return False
        registro = self.usuario_repo.obtener_con_contrasena(usuario)
        if registro is None:
            return False
        encontrado, guardada = registro
        if not verificar_contrasena(contrasena, guardada):
            return False
        if not esta_encriptada(guardada):
            # usuario antiguo con contraseña en texto plano: se migra a hash al ingresar
            self.usuario_repo.actualizar_contrasena(
                encontrado.id_usuario, encriptar_contrasena(contrasena))
        self.usuario_actual = encontrado
        return True
