"""models/usuario.py - Persona que puede entrar al sistema."""
from dataclasses import dataclass


@dataclass
class Usuario:
    id_usuario: int
    id_tipo_usuario: int
    usuario: str
    tipo: str = ""
