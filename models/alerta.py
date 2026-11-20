TIPO_NIVEL_BAJO = "NIVEL_BAJO"
TIPO_NIVEL_ALTO = "NIVEL_ALTO"
TIPO_TIEMPO_EXCEDIDO = "TIEMPO_EXCEDIDO"
TIPO_RECEPTOR_OFFLINE = "RECEPTOR_OFFLINE"
TIPO_SIN_SENAL = "SIN_SENAL"
TIPO_CICLOS_EXCESIVOS = "CICLOS_EXCESIVOS"


class Alerta:
    def __init__(self, id_modulo, tipo_alerta, fecha_hora, resuelta=False, id_alertas=None,
                 id_reservorio=None, nombre_reservorio="", ubicacion="", tipo_modulo=""):
        self.__id_modulo = id_modulo
        self.__tipo_alerta = tipo_alerta
        self.__fecha_hora = fecha_hora
        self.resuelta = resuelta
        self.__id_alertas = id_alertas
        self.__id_reservorio = id_reservorio
        self.nombre_reservorio = nombre_reservorio
        self.ubicacion = ubicacion
        self.tipo_modulo = tipo_modulo

    @property
    def id_modulo(self):
        return self.__id_modulo

    @property
    def tipo_alerta(self):
        return self.__tipo_alerta

    @property
    def fecha_hora(self):
        return self.__fecha_hora

    @property
    def resuelta(self):
        return self.__resuelta

    @resuelta.setter
    def resuelta(self, valor):
        self.__resuelta = bool(valor)

    @property
    def id_alertas(self):
        return self.__id_alertas

    @property
    def id_reservorio(self):
        return self.__id_reservorio

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

    @property
    def tipo_modulo(self):
        return self.__tipo_modulo

    @tipo_modulo.setter
    def tipo_modulo(self, valor):
        self.__tipo_modulo = valor
