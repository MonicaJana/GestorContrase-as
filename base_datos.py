import sqlite3

def conectar_db():
    #Establece conexión con el archivo local de la base de datos
    return sqlite3.connect("boveda.db")

def inicializar_db():
    # Crea las tablas necesarias si no existen en el disco duro
    conexion = conectar_db()
    cursor = conexion.cursor()
    # Tabla 1: Almacena la configuración de la Contraseña Maestra (La Sal)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sal BLOB NOT NULL
        )
    """)
    # Tabla 2: Almacena las credenciales de las cuentas del usuario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credenciales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sitio TEXT NOT NULL,
            usuario TEXT NOT NULL,
            password_cifrada BLOB NOT NULL
        )
    """)
    
    conexion.commit()
    conexion.close()

def guardar_sal(sal: bytes):
    # Guarda la Sal inicial cuando el usuario configura su clave por primera vez
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO configuracion (sal) VALUES (?)", (sal,))
    conexion.commit()
    conexion.close()

def obtener_sal():
    # Recupera la Sal del disco para poder reconstruir la llave de cifrado
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT sal FROM configuracion WHERE id = 1")
    resultado = cursor.fetchone()
    conexion.close()
    return resultado[0] if resultado else None

def guardar_credencial(sitio: str, usuario: str, password_cifrada: bytes):
    # Inserta una nueva credencial protegida en la base de datos
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO credenciales (sitio, usuario, password_cifrada) VALUES (?, ?, ?)",
        (sitio, usuario, password_cifrada)
    )
    conexion.commit()
    conexion.close()

def obtener_todas_credenciales():
    # Trae la lista de todas las cuentas registradas (siguen cifradas).
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, sitio, usuario, password_cifrada FROM credenciales")
    resultados = cursor.fetchall()
    conexion.close()
    return resultados