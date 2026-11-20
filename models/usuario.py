class Usuario:
    def __init__(self, id_usuario, id_tipo_usuario, usuario, tipo=""):
        self.__id_usuario = id_usuario
        self.__id_tipo_usuario = id_tipo_usuario
        self.__usuario = usuario
        self.tipo = tipo

    @property
    def id_usuario(self):
        return self.__id_usuario

    @property
    def id_tipo_usuario(self):
        return self.__id_tipo_usuario

    @property
    def usuario(self):
        return self.__usuario

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, valor):
        self.__tipo = valor
