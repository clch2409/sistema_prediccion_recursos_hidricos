from database.conexion import ErrorIntegridad
from models.reservorio import Reservorio
from repositories.modulo_repository import ModuloRepository
from repositories.reservorio_repository import ReservorioRepository


class ReservorioController:
    def __init__(self):
        self.reservorio_repo = ReservorioRepository()
        self.modulo_repo = ModuloRepository()

    def listar_reservorios(self):
        return self.reservorio_repo.listar()

    def listar_modulos(self):
        return self.modulo_repo.listar()

    def obtener_reservorio(self, id_reservorio):
        reservorio = self.reservorio_repo.obtener_por_id(id_reservorio)
        if reservorio is None:
            raise ValueError("El reservorio ya no existe")
        return reservorio

    def crear_reservorio(self, nombre, capacidad_maxima, ubicacion, fecha_construccion):
        reservorio = Reservorio(None, nombre, capacidad_maxima, _limpiar(ubicacion), fecha_construccion)
        self.reservorio_repo.insertar(reservorio)

    def actualizar_reservorio(self, id_reservorio, nombre, capacidad_maxima, ubicacion,
                              fecha_construccion):
        reservorio = self.obtener_reservorio(id_reservorio)
        reservorio.nombre = nombre
        reservorio.capacidad_maxima = capacidad_maxima
        reservorio.ubicacion = _limpiar(ubicacion)
        reservorio.fecha_construccion = fecha_construccion
        self.reservorio_repo.actualizar(reservorio)

    def eliminar_reservorio(self, id_reservorio):
        try:
            self.reservorio_repo.eliminar(id_reservorio)
        except ErrorIntegridad:
            raise ValueError("No se puede eliminar el reservorio porque tiene módulos, sistemas de "
                             "bombeo o registros de consumo asociados.\n"
                             "Elimine primero esos registros.")


def _limpiar(texto):
    texto = (texto or "").strip()
    return texto or None
