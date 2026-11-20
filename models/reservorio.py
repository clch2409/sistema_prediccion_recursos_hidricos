class Reservorio:
    def __init__(self, id_reservorio, nombre, capacidad_maxima, ubicacion,
                 fecha_construccion=None, porcentaje=None, ultima_lectura=None):
        self.__id_reservorio = id_reservorio
        self.nombre = nombre
        self.capacidad_maxima = capacidad_maxima
        self.ubicacion = ubicacion
        self.fecha_construccion = fecha_construccion
        self.porcentaje = porcentaje
        self.ultima_lectura = ultima_lectura

    @property
    def id_reservorio(self):
        return self.__id_reservorio

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or not str(valor).strip():
            raise ValueError("El nombre del reservorio no puede estar vacío")
        self.__nombre = valor

    @property
    def capacidad_maxima(self):
        return self.__capacidad_maxima

    @capacidad_maxima.setter
    def capacidad_maxima(self, valor):
        if valor is None or float(valor) <= 0:
            raise ValueError("La capacidad máxima debe ser mayor que cero")
        self.__capacidad_maxima = float(valor)

    @property
    def ubicacion(self):
        return self.__ubicacion

    @ubicacion.setter
    def ubicacion(self, valor):
        self.__ubicacion = valor

    @property
    def fecha_construccion(self):
        return self.__fecha_construccion

    @fecha_construccion.setter
    def fecha_construccion(self, valor):
        self.__fecha_construccion = valor

    @property
    def porcentaje(self):
        return self.__porcentaje

    @porcentaje.setter
    def porcentaje(self, valor):
        if valor is not None and not (0 <= float(valor) <= 100):
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        self.__porcentaje = None if valor is None else float(valor)

    @property
    def ultima_lectura(self):
        return self.__ultima_lectura

    @ultima_lectura.setter
    def ultima_lectura(self, valor):
        self.__ultima_lectura = valor

    def litros_actuales(self):
        if self.__porcentaje is None:
            return 0
        return self.__capacidad_maxima * self.__porcentaje / 100
