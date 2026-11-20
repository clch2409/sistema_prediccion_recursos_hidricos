from models.mantenimiento import Mantenimiento
from repositories.bomba_repository import BombaRepository
from repositories.mantenimiento_repository import MantenimientoRepository


class MantenimientoController:
    def __init__(self):
        self.mantenimiento_repo = MantenimientoRepository()
        self.bomba_repo = BombaRepository()

    def listar_mantenimientos(self):
        return self.mantenimiento_repo.listar()

    def listar_bombas(self):
        return [(b.id_bomba, f"{b.nombre} - {b.nombre_reservorio}")
                for b in self.bomba_repo.listar()]

    def obtener_mantenimiento(self, id_mantenimiento):
        mantenimiento = self.mantenimiento_repo.obtener_por_id(id_mantenimiento)
        if mantenimiento is None:
            raise ValueError("El mantenimiento ya no existe")
        return mantenimiento

    def crear_mantenimiento(self, id_bomba, costo, descripcion, fecha_intervencion):
        mantenimiento = Mantenimiento(None, id_bomba, costo, descripcion, fecha_intervencion)
        self.mantenimiento_repo.insertar(mantenimiento)

    def actualizar_mantenimiento(self, id_mantenimiento, id_bomba, costo, descripcion,
                                 fecha_intervencion):
        mantenimiento = self.obtener_mantenimiento(id_mantenimiento)
        mantenimiento.id_bomba = id_bomba
        mantenimiento.costo = costo
        mantenimiento.descripcion = descripcion
        mantenimiento.fecha_intervencion = fecha_intervencion
        self.mantenimiento_repo.actualizar(mantenimiento)

    def eliminar_mantenimiento(self, id_mantenimiento):
        self.mantenimiento_repo.eliminar(id_mantenimiento)
