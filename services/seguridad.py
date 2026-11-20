"""Encriptación de contraseñas (PBKDF2-HMAC-SHA256 con sal aleatoria, solo librería estándar).

Formato guardado en Usuarios.contrasena (cabe de sobra en VARCHAR(255)):
    pbkdf2_sha256$<iteraciones>$<sal en hex>$<hash en hex>
"""
import hashlib
import hmac
import secrets

ALGORITMO = "pbkdf2_sha256"
ITERACIONES = 600_000
TAMANO_SAL = 16


def encriptar_contrasena(contrasena):
    if not contrasena:
        raise ValueError("La contraseña no puede estar vacía")
    sal = secrets.token_bytes(TAMANO_SAL)
    derivada = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), sal, ITERACIONES)
    return f"{ALGORITMO}${ITERACIONES}${sal.hex()}${derivada.hex()}"


def esta_encriptada(valor):
    return bool(valor) and valor.startswith(ALGORITMO + "$")


def verificar_contrasena(contrasena, almacenada):
    """True si la contraseña coincide con la almacenada.

    Si la almacenada aún está en texto plano (usuarios creados antes de este cambio)
    se compara directamente; el login la reemplaza por su hash al entrar.
    """
    if not almacenada:
        return False
    if not esta_encriptada(almacenada):
        return hmac.compare_digest(contrasena.encode("utf-8"), almacenada.strip().encode("utf-8"))
    try:
        _, iteraciones, sal, esperado = almacenada.split("$")
        derivada = hashlib.pbkdf2_hmac(
            "sha256", contrasena.encode("utf-8"), bytes.fromhex(sal), int(iteraciones))
    except ValueError:
        return False
    return hmac.compare_digest(derivada.hex(), esperado)
