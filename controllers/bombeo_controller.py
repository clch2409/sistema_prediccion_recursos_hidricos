"""controllers/bombeo_controller.py - Datos para la pantalla Sistemas de bombeo."""
from datetime import datetime

from repositories.bomba_repository import BombaRepository


class BombeoController:

    def __init__(self):
        self.bomba_repo = BombaRepository()

    def listar_bombas(self):
        """Devuelve las bombas con sus horas de operación y ciclos de la última hora ya calculados."""
        ahora = datetime.now()
        bombas = self.bomba_repo.listar()
        for bomba in bombas:
            bomba.horas_operacion = self.bomba_repo.horas_operacion(
                bomba.id_bomba, bomba.horas_iniciales, ahora)
            bomba.ciclos_ultima_hora = self.bomba_repo.contar_ciclos_ultima_hora(
                bomba.id_bomba, ahora)
        return bombas
