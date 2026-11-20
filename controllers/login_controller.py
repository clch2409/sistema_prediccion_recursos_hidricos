from repositories.usuario_repository import UsuarioRepository


class LoginController:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
        self.usuario_actual = None

    def iniciar_sesion(self, usuario, contrasena):
        if not usuario or not contrasena:
            return False
        self.usuario_actual = self.usuario_repo.buscar_por_credenciales(usuario, contrasena)
        return self.usuario_actual is not None
