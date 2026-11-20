from datetime import datetime

from database.conexion import ErrorIntegridad
from models.modulo import Modulo
from repositories.modulo_repository import ModuloRepository
from repositories.reservorio_repository import ReservorioRepository


class ModuloController:
    def __init__(self):
        self.modulo_repo = ModuloRepository()
        self.reservorio_repo = ReservorioRepository()

    def listar_modulos(self):
        return self.modulo_repo.listar()

    def listar_reservorios(self):
        return [(r.id_reservorio, r.nombre) for r in self.reservorio_repo.listar()]

    def listar_tipos(self):
        return self.modulo_repo.listar_tipos()

    def obtener_modulo(self, id_modulo):
        modulo = self.modulo_repo.obtener_por_id(id_modulo)
        if modulo is None:
            raise ValueError("El módulo ya no existe")
        return modulo

    def crear_modulo(self, id_modulo, id_reservorio, id_tipo_modulo, nombre_modulo,
                     altura_instalacion, estado):
        modulo = Modulo(id_modulo, id_reservorio, id_tipo_modulo, nombre_modulo,
                        altura_instalacion, estado)
        if self.modulo_repo.obtener_por_id(modulo.id_modulo) is not None:
            raise ValueError(f"Ya existe un módulo con el código {modulo.id_modulo}")
        self.modulo_repo.insertar(modulo, datetime.now())

    def actualizar_modulo(self, id_modulo, id_reservorio, id_tipo_modulo, nombre_modulo,
                          altura_instalacion, estado):
        modulo = self.obtener_modulo(id_modulo)
        modulo.id_reservorio = id_reservorio
        modulo.id_tipo_modulo = id_tipo_modulo
        modulo.nombre_modulo = nombre_modulo
        modulo.altura_instalacion = altura_instalacion
        modulo.estado = estado
        self.modulo_repo.actualizar(modulo, datetime.now())

    def eliminar_modulo(self, id_modulo):
        try:
            self.modulo_repo.eliminar(id_modulo)
        except ErrorIntegridad:
            raise ValueError("No se puede eliminar el módulo porque tiene lecturas o alertas "
                             "registradas.\nPuede marcarlo como inactivo desde Editar.")
