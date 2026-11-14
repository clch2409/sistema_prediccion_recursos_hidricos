"""controllers/dashboard_controller.py - Prepara los datos de la pantalla Dashboard."""
from models.alerta import (TIPO_CICLOS_EXCESIVOS, TIPO_NIVEL_BAJO, TIPO_RECEPTOR_OFFLINE,
                           TIPO_SIN_SENAL)
from repositories.alerta_repository import AlertaRepository
from repositories.bomba_repository import BombaRepository
from repositories.reservorio_repository import ReservorioRepository
from datetime import datetime


class DashboardController:

    def __init__(self):
        self.alerta_repo = AlertaRepository()
        self.reservorio_repo = ReservorioRepository()
        self.bomba_repo = BombaRepository()

    def obtener_textos_alertas(self):
        """Devuelve 3 textos (uno por cuadro de alerta del Dashboard)."""
        alertas = self.alerta_repo.listar_pendientes()

        # Cuadro 1: módulos que requieren atención
        modulos = [a for a in alertas if a.tipo_alerta in (TIPO_SIN_SENAL, TIPO_RECEPTOR_OFFLINE)]
        lineas = [f"{a.nombre_reservorio} - {a.tipo_modulo}" for a in modulos]
        texto_modulos = (f"EXISTEN {len(modulos)} MÓDULOS QUE REQUIEREN SU ATENCIÓN\n"
                         + "\n".join(lineas)) if modulos else "TODOS LOS MÓDULOS FUNCIONAN CORRECTAMENTE"

        # Cuadro 2: reservorios con nivel bajo
        bajos = [a for a in alertas if a.tipo_alerta == TIPO_NIVEL_BAJO]
        lineas = [f"{a.nombre_reservorio} - {a.ubicacion.split('/')[-1].strip()}" for a in bajos]
        texto_niveles = (f"EXISTEN {len(bajos)} RESERVORIOS CON UN NIVEL DE RESERVAS < AL 10%\n"
                         + "\n".join(lineas)) if bajos else "NINGÚN RESERVORIO CON NIVEL CRÍTICO"

        # Cuadro 3: riesgo de daño en bombas
        ciclos = [a for a in alertas if a.tipo_alerta == TIPO_CICLOS_EXCESIVOS]
        lineas = [f"{a.nombre_reservorio} - {a.ubicacion.split('/')[-1].strip()}" for a in ciclos]
        texto_bombas = ("RIESGO DE DAÑO\n>10 CICLOS DE ENCENDIDO EN LA ÚLTIMA HORA\n"
                        + "\n".join(lineas)) if ciclos else "SIN RIESGO DE DAÑO EN BOMBAS"

        return texto_modulos, texto_niveles, texto_bombas

    def obtener_reservas(self):
        """Devuelve (mayor, promedio, menor): cada uno es (texto, porcentaje)."""
        reservorios = [r for r in self.reservorio_repo.listar() if r.porcentaje is not None]
        if not reservorios:
            return None
        mayor = max(reservorios, key=lambda r: r.porcentaje)
        menor = min(reservorios, key=lambda r: r.porcentaje)
        promedio = sum(r.porcentaje for r in reservorios) / len(reservorios)
        return ((mayor.nombre, mayor.porcentaje), ("PROMEDIO", promedio), (menor.nombre, menor.porcentaje))

    def obtener_vida_util(self):
        """Devuelve la bomba con más y la de menos vida útil: [(nombre, porcentaje), ...]."""
        ahora = datetime.now()
        bombas = self.bomba_repo.listar()
        for bomba in bombas:
            bomba.horas_operacion = self.bomba_repo.horas_operacion(
                bomba.id_bomba, bomba.horas_iniciales, ahora)
        if not bombas:
            return []
        mayor = max(bombas, key=lambda b: b.vida_util_restante_pct())
        menor = min(bombas, key=lambda b: b.vida_util_restante_pct())
        return [(mayor.nombre_reservorio, mayor.vida_util_restante_pct()),
                (menor.nombre_reservorio, menor.vida_util_restante_pct())]
