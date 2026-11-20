from database import conexion
from models.usuario import Usuario


class UsuarioRepository:
    def buscar_por_credenciales(self, usuario, contrasena):
        filas = conexion.consultar(
            "SELECT u.id_usuario, u.id_tipo_usuario, u.usuario, t.nombre_tipo "
            "FROM Usuarios u INNER JOIN Tipo_Usuario t ON t.id_tipo_usuario = u.id_tipo_usuario "
            "WHERE u.usuario = ? AND u.contrasena = ?",
            (usuario, contrasena),
        )
        if not filas:
            return None
        f = filas[0]
        return Usuario(f.id_usuario, f.id_tipo_usuario, f.usuario, f.nombre_tipo)
