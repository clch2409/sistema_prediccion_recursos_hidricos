class Modulo:
    def __init__(self, id_modulo, id_reservorio, id_tipo_modulo, nombre_modulo,
                 altura_instalacion, estado, fecha_estado=None, tipo="", nombre_reservorio=""):
        self.__id_modulo = id_modulo
        self.__id_reservorio = id_reservorio
        self.__id_tipo_modulo = id_tipo_modulo
        self.nombre_modulo = nombre_modulo
        self.altura_instalacion = altura_instalacion
        self.estado = estado
        self.fecha_estado = fecha_estado
        self.tipo = tipo
        self.nombre_reservorio = nombre_reservorio

    @property
    def id_modulo(self):
        return self.__id_modulo

    @property
    def id_reservorio(self):
        return self.__id_reservorio

    @property
    def id_tipo_modulo(self):
        return self.__id_tipo_modulo

    @property
    def nombre_modulo(self):
        return self.__nombre_modulo

    @nombre_modulo.setter
    def nombre_modulo(self, valor):
        if valor is None or not str(valor).strip():
            raise ValueError("El nombre del módulo no puede estar vacío")
        self.__nombre_modulo = valor

    @property
    def altura_instalacion(self):
        return self.__altura_instalacion

    @altura_instalacion.setter
    def altura_instalacion(self, valor):
        if valor is not None and float(valor) < 0:
            raise ValueError("La altura de instalación no puede ser negativa")
        self.__altura_instalacion = 0.0 if valor is None else float(valor)

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        self.__estado = bool(valor)

    @property
    def fecha_estado(self):
        return self.__fecha_estado

    @fecha_estado.setter
    def fecha_estado(self, valor):
        self.__fecha_estado = valor

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, valor):
        self.__tipo = valor

    @property
    def nombre_reservorio(self):
        return self.__nombre_reservorio

    @nombre_reservorio.setter
    def nombre_reservorio(self, valor):
        self.__nombre_reservorio = valor
