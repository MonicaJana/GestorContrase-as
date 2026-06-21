import string
import secrets
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

def generar_password_aleatorio(longitud=16):
    # Genera una contraseña aleatoria usando 'secrets' para máxima entropía
    # Utiliza letras, dígitos y caracteres especiales para máxima seguridad
    
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def derivar_llave_maestra(password_maestra: str, sal: bytes) -> bytes:
    # Deriva la llave maestra usando PBKDF2 con SHA256
    # Transforma la contraseña del usuario en una llave AES de 32 bytes
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=sal,
        iterations=600000  # Iteraciones PBKDF2 para resistencia contra ataques de fuerza bruta
    )
    return base64.urlsafe_b64encode(kdf.derive(password_maestra.encode()))

def encriptar_dato(texto_plano: str, llave_aes: bytes) -> bytes:
    # Encripta texto plano usando Fernet (AES-256) con la llave proporcionada
    
    f = Fernet(llave_aes)
    return f.encrypt(texto_plano.encode())

def desencriptar_dato(datos_cifrados: bytes, llave_aes: bytes) -> str:
    # Desencripta datos cifrados usando Fernet (AES-256) y retorna texto plano
    f = Fernet(llave_aes)
    return f.decrypt(datos_cifrados).decode()