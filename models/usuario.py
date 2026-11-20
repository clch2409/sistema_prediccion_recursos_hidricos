class Usuario:
    def __init__(self, id_usuario, id_tipo_usuario, usuario, tipo=""):
        self.__id_usuario = id_usuario
        self.id_tipo_usuario = id_tipo_usuario
        self.usuario = usuario
        self.tipo = tipo

    @property
    def id_usuario(self):
        return self.__id_usuario

    @property
    def id_tipo_usuario(self):
        return self.__id_tipo_usuario

    @id_tipo_usuario.setter
    def id_tipo_usuario(self, valor):
        if valor is None:
            raise ValueError("Seleccione el tipo de usuario")
        self.__id_tipo_usuario = int(valor)

    @property
    def usuario(self):
        return self.__usuario

    @usuario.setter
    def usuario(self, valor):
        if valor is None or not str(valor).strip():
            raise ValueError("El nombre de usuario no puede estar vacío")
        valor = str(valor).strip()
        if len(valor) > 50:
            raise ValueError("El nombre de usuario no puede superar los 50 caracteres")
        self.__usuario = valor

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, valor):
        self.__tipo = valor
