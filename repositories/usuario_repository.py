from database import conexion
from models.usuario import Usuario

_SQL_BASE = (
    "SELECT u.id_usuario, u.id_tipo_usuario, u.usuario, t.nombre_tipo "
    "FROM Usuarios u INNER JOIN Tipo_Usuario t ON t.id_tipo_usuario = u.id_tipo_usuario"
)


def _fila_a_usuario(f):
    return Usuario(f.id_usuario, f.id_tipo_usuario, f.usuario, f.nombre_tipo)


class UsuarioRepository:
    def obtener_con_contrasena(self, usuario):
        """Devuelve (Usuario, contraseña guardada) o None. La verificación la hace el controller."""
        filas = conexion.consultar(
            "SELECT u.id_usuario, u.id_tipo_usuario, u.usuario, u.contrasena, t.nombre_tipo "
            "FROM Usuarios u INNER JOIN Tipo_Usuario t ON t.id_tipo_usuario = u.id_tipo_usuario "
            "WHERE u.usuario = ?",
            (usuario,),
        )
        if not filas:
            return None
        return _fila_a_usuario(filas[0]), filas[0].contrasena

    def listar(self):
        filas = conexion.consultar(_SQL_BASE + " ORDER BY u.id_usuario")
        return [_fila_a_usuario(f) for f in filas]

    def obtener_por_id(self, id_usuario):
        filas = conexion.consultar(_SQL_BASE + " WHERE u.id_usuario = ?", (id_usuario,))
        if not filas:
            return None
        return _fila_a_usuario(filas[0])

    def existe_usuario(self, usuario, excepto_id=None):
        filas = conexion.consultar(
            "SELECT COUNT(*) AS total FROM Usuarios WHERE usuario = ? AND id_usuario <> ?",
            (usuario, excepto_id if excepto_id is not None else -1),
        )
        return filas[0].total > 0

    def listar_tipos(self):
        filas = conexion.consultar(
            "SELECT id_tipo_usuario, nombre_tipo FROM Tipo_Usuario ORDER BY id_tipo_usuario")
        return [(f.id_tipo_usuario, f.nombre_tipo) for f in filas]

    def insertar(self, usuario, contrasena_encriptada):
        conexion.ejecutar(
            "INSERT INTO Usuarios (id_tipo_usuario, usuario, contrasena) VALUES (?, ?, ?)",
            (usuario.id_tipo_usuario, usuario.usuario, contrasena_encriptada),
        )

    def actualizar(self, usuario):
        conexion.ejecutar(
            "UPDATE Usuarios SET id_tipo_usuario = ?, usuario = ? WHERE id_usuario = ?",
            (usuario.id_tipo_usuario, usuario.usuario, usuario.id_usuario),
        )

    def actualizar_contrasena(self, id_usuario, contrasena_encriptada):
        conexion.ejecutar(
            "UPDATE Usuarios SET contrasena = ? WHERE id_usuario = ?",
            (contrasena_encriptada, id_usuario),
        )

    def eliminar(self, id_usuario):
        conexion.ejecutar("DELETE FROM Usuarios WHERE id_usuario = ?", (id_usuario,))
