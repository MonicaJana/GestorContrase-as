import string
import secrets
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

def generar_password_aleatorio(longitud=16, incluir_simbolos=True):

    caracteres_permitidos = string.ascii_letters + string.digits
    if incluir_simbolos:
        caracteres_permitidos += string.punctuation
        
    password_acumulada = ""

    for i in range(longitud):
        # Elegimos un solo carácter al azarpermitida
        caracter_elegido = secrets.choice(caracteres_permitidos)
        # Lo acumulamos en nuestra variable de texto plano
        password_acumulada += caracter_elegido
        
    return password_acumulada

def evaluar_nivel_seguridad(password: str) -> tuple:
    
    # Analiza la contraseña generada según su longitud y variedad de caracteres, 
    # devolviendo un texto descriptivo y un color para la interfaz gráfica 
    
    longitud = len(password)
    
    # Inicializamos contadores
    contador_numeros = 0
    contador_simbolos = 0
    
    # Indicará en qué posición de la palabra estamos parados (0, 1, 2...)
    puntero = 0 
    
    # El ciclo continuará ejecutándose MIENTRAS el puntero no llegue al final de la palabra.
    # No sabemos cuántos caracteres tiene la clave de antemano; el ciclo frena al terminar la cadena.
    while puntero < longitud:
        caracter_actual = password[puntero] # Extraemos la letra actual
        
        # Evaluamos el carácter usando condicionales
        if caracter_actual.isdigit():
            contador_numeros += 1
        elif caracter_actual in string.punctuation:
            contador_simbolos += 1
            
        # Avanzamos el puntero para evitar un bucle infinito
        puntero += 1 

    if longitud < 10:
        return "🔴 Débil (Muy corta)", "red"
    elif longitud >= 10 and longitud < 14:
        if contador_numeros > 0 or contador_simbolos > 0:
            return "🟡 Media (Aceptable)", "orange"
        return "🔴 Débil (Faltan caracteres variados)", "red"
    else: # 14 o más caracteres
        if contador_numeros > 0 and contador_simbolos > 0:
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