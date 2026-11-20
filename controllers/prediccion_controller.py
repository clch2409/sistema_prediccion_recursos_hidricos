from repositories.lectura_repository import LecturaRepository
from repositories.reservorio_repository import ReservorioRepository
from services import prediccion_service


class PrediccionController:
    def __init__(self):
        self.reservorio_repo = ReservorioRepository()
        self.lectura_repo = LecturaRepository()

    def listar_reservorios(self):
        return self.reservorio_repo.listar()

    def predecir(self, id_reservorio):
        reservorio = self.reservorio_repo.obtener_por_id(id_reservorio)
        lecturas = self.lectura_repo.listar_recientes(id_reservorio, 200)
        prediccion = prediccion_service.calcular_prediccion(lecturas, reservorio.capacidad_maxima)
        return reservorio, prediccion
