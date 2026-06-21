import string
import secrets
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

def generar_password_aleatorio(longitud=16, incluir_simbolos=True):

    # Siempre usamos letras y números obligatoriamente
    caracteres = string.ascii_letters + string.digits
    
    # [FUNCIONALIDAD: Incluir/Excluir Símbolos]
    if incluir_simbolos:
        caracteres += string.punctuation
        
    # [FUNCIONALIDAD: Elegir Longitud]
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def evaluar_nivel_seguridad(password: str) -> tuple:
    
    # Analiza la contraseña generada según su longitud y variedad de caracteres, 
    # devolviendo un texto descriptivo y un color para la interfaz gráfica 
    
    longitud = len(password)
    tiene_numeros = any(c.isdigit() for c in password)
    tiene_simbolos = any(c in string.punctuation for c in password)
    
    if longitud < 10:
        return "🔴 Débil (Muy corta)", "red"
    elif longitud >= 10 and longitud < 14:
        if tiene_numeros or tiene_simbolos:
            return "🟡 Media (Aceptable)", "orange"
        return "🔴 Débil (Faltan caracteres variados)", "red"
    else: # 14 o más caracteres
        if tiene_numeros and tiene_simbolos:
            return "🟢 Fuerte (Excelente seguridad)", "green"
        return "🟡 Media (Agrega símbolos para mejorar)", "orange"

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