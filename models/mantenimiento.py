class Mantenimiento:
    def __init__(self, id_mantenimiento, id_bomba, costo, descripcion, fecha_intervencion,
                 nombre_bomba="", nombre_reservorio=""):
        self.__id_mantenimiento = id_mantenimiento
        self.id_bomba = id_bomba
        self.costo = costo
        self.descripcion = descripcion
        self.fecha_intervencion = fecha_intervencion
        self.nombre_bomba = nombre_bomba
        self.nombre_reservorio = nombre_reservorio

    @property
    def id_mantenimiento(self):
        return self.__id_mantenimiento

    @property
    def id_bomba(self):
        return self.__id_bomba

    @id_bomba.setter
    def id_bomba(self, valor):
        if valor is None:
            raise ValueError("Seleccione el sistema de bombeo")
        self.__id_bomba = int(valor)

    @property
    def costo(self):
        return self.__costo

    @costo.setter
    def costo(self, valor):
        if valor is not None and float(valor) < 0:
            raise ValueError("El costo no puede ser negativo")
        self.__costo = 0.0 if valor is None else float(valor)

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor):
        if valor is None or not str(valor).strip():
            raise ValueError("La descripción del mantenimiento no puede estar vacía")
        self.__descripcion = str(valor).strip()

    @property
    def fecha_intervencion(self):
        return self.__fecha_intervencion

    @fecha_intervencion.setter
    def fecha_intervencion(self, valor):
        if valor is None:
            raise ValueError("Indique la fecha de intervención")
        self.__fecha_intervencion = valor

    @property
    def nombre_bomba(self):
        return self.__nombre_bomba

    @nombre_bomba.setter
    def nombre_bomba(self, valor):
        self.__nombre_bomba = valor

    @property
    def nombre_reservorio(self):
        return self.__nombre_reservorio

    @nombre_reservorio.setter
    def nombre_reservorio(self, valor):
        self.__nombre_reservorio = valor
