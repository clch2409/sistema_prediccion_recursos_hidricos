from datetime import datetime

from database.conexion import ErrorIntegridad
from models.bomba import SistemaBombeo
from repositories.bomba_repository import BombaRepository
from repositories.reservorio_repository import ReservorioRepository


class BombeoController:
    def __init__(self):
        self.bomba_repo = BombaRepository()
        self.reservorio_repo = ReservorioRepository()

    def listar_bombas(self):
        ahora = datetime.now()
        bombas = self.bomba_repo.listar()
        for bomba in bombas:
            bomba.horas_operacion = self.bomba_repo.horas_operacion(
                bomba.id_bomba, bomba.horas_iniciales, ahora)
            bomba.ciclos_ultima_hora = self.bomba_repo.contar_ciclos_ultima_hora(
                bomba.id_bomba, ahora)
        return bombas

    def listar_reservorios(self):
        return [(r.id_reservorio, r.nombre) for r in self.reservorio_repo.listar()]

    def obtener_bomba(self, id_bomba):
        bomba = self.bomba_repo.obtener_por_id(id_bomba)
        if bomba is None:
            raise ValueError("El sistema de bombeo ya no existe")
        return bomba

    def _validar_reservorio_libre(self, id_reservorio, id_bomba=None):
        # El sistema trabaja con una bomba por reservorio (ver MensajeController)
        existente = self.bomba_repo.obtener_por_reservorio(id_reservorio)
        if existente is not None and existente.id_bomba != id_bomba:
            raise ValueError("Ese reservorio ya tiene un sistema de bombeo registrado")

    def crear_bomba(self, id_reservorio, nombre, modelo, caudal_l_s, consumo_kw, estado,
                    horas_iniciales):
        bomba = SistemaBombeo(None, id_reservorio, nombre, modelo, caudal_l_s, consumo_kw,
                              estado, horas_iniciales)
        self._validar_reservorio_libre(bomba.id_reservorio)
        self.bomba_repo.insertar(bomba)

    def actualizar_bomba(self, id_bomba, id_reservorio, nombre, modelo, caudal_l_s, consumo_kw,
                         estado, horas_iniciales):
        bomba = self.obtener_bomba(id_bomba)
        bomba.id_reservorio = id_reservorio
        bomba.nombre = nombre
        bomba.modelo = modelo
        bomba.caudal_l_s = caudal_l_s
        bomba.consumo_kw = consumo_kw
        bomba.estado = estado
        bomba.horas_iniciales = horas_iniciales
        self._validar_reservorio_libre(bomba.id_reservorio, bomba.id_bomba)
        self.bomba_repo.actualizar(bomba)

    def eliminar_bomba(self, id_bomba):
        try:
            self.bomba_repo.eliminar(id_bomba)
        except ErrorIntegridad:
            raise ValueError("No se puede eliminar el sistema de bombeo porque tiene historial de "
                             "bombeo o mantenimientos registrados.\n"
                             "Elimine primero esos registros.")
