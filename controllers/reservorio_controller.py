"""controllers/reservorio_controller.py - Datos para las pantallas Reservorios y Estado módulos."""
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
