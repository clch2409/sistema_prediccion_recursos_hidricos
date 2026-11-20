class Lectura:
    def __init__(self, id_modulo, fecha_hora, nivel_agua, calidad_senal=100):
        self.__id_modulo = id_modulo
        self.__fecha_hora = fecha_hora
        self.nivel_agua = nivel_agua
        self.calidad_senal = calidad_senal

    @property
    def id_modulo(self):
        return self.__id_modulo

    @property
    def fecha_hora(self):
        return self.__fecha_hora

    @property
    def nivel_agua(self):
        return self.__nivel_agua

    @nivel_agua.setter
    def nivel_agua(self, valor):
        if valor is None or not (0 <= float(valor) <= 100):
            raise ValueError("El nivel de agua debe estar entre 0 y 100")
        self.__nivel_agua = float(valor)

    @property
    def calidad_senal(self):
        return self.__calidad_senal

    @calidad_senal.setter
    def calidad_senal(self, valor):
        self.__calidad_senal = valor
