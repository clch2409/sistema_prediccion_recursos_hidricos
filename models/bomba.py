import config


class SistemaBombeo:
    def __init__(self, id_bomba, id_reservorio, nombre, modelo, caudal_l_s, consumo_kw, estado,
                 horas_iniciales=0, horas_operacion=0, ciclos_ultima_hora=0,
                 nombre_reservorio="", ubicacion=""):
        self.__id_bomba = id_bomba
        self.id_reservorio = id_reservorio
        self.nombre = nombre
        self.modelo = modelo
        self.caudal_l_s = caudal_l_s
        self.consumo_kw = consumo_kw
        self.estado = estado
        self.horas_iniciales = horas_iniciales
        self.horas_operacion = horas_operacion
        self.ciclos_ultima_hora = ciclos_ultima_hora
        self.nombre_reservorio = nombre_reservorio
        self.ubicacion = ubicacion

    @property
    def id_bomba(self):
        return self.__id_bomba

    @property
    def id_reservorio(self):
        return self.__id_reservorio

    @id_reservorio.setter
    def id_reservorio(self, valor):
        if valor is None:
            raise ValueError("Seleccione el reservorio")
        self.__id_reservorio = int(valor)

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or not str(valor).strip():
            raise ValueError("El nombre de la bomba no puede estar vacío")
        if len(str(valor).strip()) > 100:
            raise ValueError("El nombre de la bomba no puede superar los 100 caracteres")
        self.__nombre = str(valor).strip()

    @property
    def modelo(self):
        return self.__modelo

    @modelo.setter
    def modelo(self, valor):
        if valor is None or not str(valor).strip():
            raise ValueError("El modelo de la bomba no puede estar vacío")
        if len(str(valor).strip()) > 100:
            raise ValueError("El modelo de la bomba no puede superar los 100 caracteres")
        self.__modelo = str(valor).strip()

    @property
    def caudal_l_s(self):
        return self.__caudal_l_s

    @caudal_l_s.setter
    def caudal_l_s(self, valor):
        if valor is not None and float(valor) < 0:
            raise ValueError("El caudal no puede ser negativo")
        self.__caudal_l_s = float(valor or 0)

    @property
    def consumo_kw(self):
        return self.__consumo_kw

    @consumo_kw.setter
    def consumo_kw(self, valor):
        if valor is not None and float(valor) < 0:
            raise ValueError("El consumo no puede ser negativo")
        self.__consumo_kw = float(valor or 0)

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        self.__estado = bool(valor)

    @property
    def horas_iniciales(self):
        return self.__horas_iniciales

    @horas_iniciales.setter
    def horas_iniciales(self, valor):
        if valor is not None and float(valor) < 0:
            raise ValueError("Las horas iniciales no pueden ser negativas")
        self.__horas_iniciales = float(valor or 0)

    @property
    def horas_operacion(self):
        return self.__horas_operacion

    @horas_operacion.setter
    def horas_operacion(self, valor):
        self.__horas_operacion = float(valor or 0)

    @property
    def ciclos_ultima_hora(self):
        return self.__ciclos_ultima_hora

    @ciclos_ultima_hora.setter
    def ciclos_ultima_hora(self, valor):
        self.__ciclos_ultima_hora = int(valor or 0)

    @property
    def nombre_reservorio(self):
        return self.__nombre_reservorio

    @nombre_reservorio.setter
    def nombre_reservorio(self, valor):
        self.__nombre_reservorio = valor

    @property
    def ubicacion(self):
        return self.__ubicacion

    @ubicacion.setter
    def ubicacion(self, valor):
        self.__ubicacion = valor

    def vida_util_restante_pct(self):
        usado = self.__horas_operacion / config.HORAS_VIDA_UTIL * 100
        return max(0, round(100 - usado, 1))

    def necesita_mantenimiento(self):
        if self.__horas_operacion >= config.HORAS_MTTO_MAYOR:
            return "MTTO MAYOR"
        if self.__horas_operacion >= config.HORAS_MTTO_MENOR:
            return "MTTO MENOR"
        return ""
