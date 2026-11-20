from datetime import datetime, timedelta

import config
from models.alerta import (Alerta, TIPO_CICLOS_EXCESIVOS, TIPO_RECEPTOR_OFFLINE,
                           TIPO_SIN_SENAL)
from models.lectura import Lectura
from repositories.alerta_repository import AlertaRepository
from repositories.bomba_repository import BombaRepository
from repositories.lectura_repository import LecturaRepository
from repositories.modulo_repository import ModuloRepository
from repositories.reservorio_repository import ReservorioRepository
from services import bombeo_service


class MensajeController:
    def __init__(self):
        self.reservorio_repo = ReservorioRepository()
        self.modulo_repo = ModuloRepository()
        self.lectura_repo = LecturaRepository()
        self.alerta_repo = AlertaRepository()
        self.bomba_repo = BombaRepository()
        self.publicar_comando = None

    def set_publicador(self, funcion):
        self.publicar_comando = funcion

    def procesar_mensaje(self, id_topic, datos):
        try:
            self._procesar(id_topic, datos)
        except Exception as error:
            print(f"[MensajeController] Error: {error}")

    def _procesar(self, id_topic, datos):
        ahora = datetime.now()

        porcentaje = datos.get("porcentaje")
        if porcentaje is None or not (0 <= float(porcentaje) <= 100):
            print(f"JSON descartado (porcentaje inválido): {datos}")
            return
        porcentaje = float(porcentaje)

        emisor = self.modulo_repo.obtener_por_id(datos.get("emisor_id"))
        receptor = self.modulo_repo.obtener_por_id(datos.get("receptor_id"))
        if emisor is None or receptor is None:
            print(f"JSON descartado: no existe en la tabla Modulo el emisor "
                  f"'{datos.get('emisor_id')}' y/o el receptor '{datos.get('receptor_id')}'. "
                  f"Regístralos con ese código como id_modulo.")
            return

        reservorio = self.reservorio_repo.obtener_por_id(emisor.id_reservorio)
        receptor_online = bool(datos.get("receptor_online"))

        lectura_anterior = self.lectura_repo.obtener_ultima_de_reservorio(reservorio.id_reservorio)
        calidad = 100 if receptor_online else 0
        self.lectura_repo.insertar(Lectura(emisor.id_modulo, ahora, porcentaje, calidad))

        bomba = self.bomba_repo.obtener_por_reservorio(reservorio.id_reservorio)
        bomba_encendida = bombeo_service.bomba_esta_encendida(datos.get("bomba_estado"))
        self._registrar_consumo(reservorio, lectura_anterior, porcentaje, ahora, bomba_encendida)

        self.modulo_repo.actualizar_estado(emisor.id_modulo, True, ahora)
        self.modulo_repo.actualizar_estado(receptor.id_modulo, receptor_online, ahora)
        self._gestionar_alerta(receptor.id_modulo, TIPO_RECEPTOR_OFFLINE, not receptor_online, ahora)
        self._gestionar_alerta(emisor.id_modulo, TIPO_SIN_SENAL, False, ahora)

        if bomba is not None:
            self._controlar_bomba(bomba, reservorio, emisor, receptor,
                                  porcentaje, bomba_encendida, lectura_anterior, ahora)

        print(f"[{ahora:%H:%M:%S}] {reservorio.nombre}: {porcentaje}% | bomba "
              f"{'ENCENDIDA' if bomba_encendida else 'apagada'} | receptor "
              f"{'online' if receptor_online else 'OFFLINE'}")


    def _registrar_consumo(self, reservorio, lectura_anterior, porcentaje, ahora, bomba_encendida):
        if lectura_anterior is None or bomba_encendida:
            return
        segundos = (ahora - lectura_anterior.fecha_hora).total_seconds()
        bajada_pct = float(lectura_anterior.nivel_agua) - porcentaje
        if segundos <= 0 or bajada_pct <= 0:
            return
        litros = bajada_pct / 100 * reservorio.capacidad_maxima
        self.lectura_repo.insertar_consumo(reservorio.id_reservorio, ahora, litros / segundos)

    def _controlar_bomba(self, bomba, reservorio, emisor, receptor,
                         porcentaje, bomba_encendida, lectura_anterior, ahora):
        ciclo = self.bomba_repo.obtener_ciclo_abierto(bomba.id_bomba)

        if bomba_encendida and ciclo is None:
            self.bomba_repo.abrir_ciclo(bomba.id_bomba, ahora)
            ciclo = self.bomba_repo.obtener_ciclo_abierto(bomba.id_bomba)
        elif not bomba_encendida and ciclo is not None:
            id_historial, _fecha_encendido = ciclo
            nivel_inicio = float(lectura_anterior.nivel_agua) if lectura_anterior else porcentaje
            volumen = bombeo_service.calcular_volumen_inyectado(
                nivel_inicio, porcentaje, reservorio.capacidad_maxima)
            self.bomba_repo.cerrar_ciclo(id_historial, ahora, volumen)
            ciclo = None

        minutos = 0
        if ciclo is not None:
            minutos = (ahora - ciclo[1]).total_seconds() / 60
        motivo = bombeo_service.decidir_apagado(porcentaje, bomba_encendida, minutos)

        for tipo in ("NIVEL_BAJO", "NIVEL_ALTO", "TIEMPO_EXCEDIDO"):
            self._gestionar_alerta(emisor.id_modulo, tipo, motivo == tipo, ahora)

        if motivo is not None and self.publicar_comando is not None:
            print(f"   >>> APAGANDO BOMBA de {reservorio.nombre}. Motivo: {motivo}")
            self.publicar_comando(reservorio.id_reservorio, {"bomba": "OFF", "motivo": motivo})

        ciclos = self.bomba_repo.contar_ciclos_ultima_hora(bomba.id_bomba, ahora)
        self._gestionar_alerta(receptor.id_modulo, TIPO_CICLOS_EXCESIVOS,
                               ciclos > config.MAX_CICLOS_HORA, ahora)

    def _gestionar_alerta(self, id_modulo, tipo, hay_problema, ahora):
        pendiente = self.alerta_repo.existe_pendiente(id_modulo, tipo)
        if hay_problema and not pendiente:
            self.alerta_repo.insertar(Alerta(id_modulo, tipo, ahora))
        elif not hay_problema and pendiente:
            self.alerta_repo.resolver(id_modulo, tipo)

    def revisar_latidos(self):
        ahora = datetime.now()
        limite = timedelta(minutes=config.MINUTOS_SIN_SENAL)

        for reservorio in self.reservorio_repo.listar():
            if reservorio.ultima_lectura is None:
                continue
            sin_senal = (ahora - reservorio.ultima_lectura) > limite
            if not sin_senal:
                continue
            for modulo in self.modulo_repo.listar():
                if modulo.id_reservorio != reservorio.id_reservorio:
                    continue
                self.modulo_repo.actualizar_estado(modulo.id_modulo, False, ahora)
                self._gestionar_alerta(modulo.id_modulo, TIPO_SIN_SENAL, True, ahora)
