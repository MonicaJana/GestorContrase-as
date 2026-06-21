# 🔐 Gestor de Contraseñas

## 📖 Descripción

Su objetivo es proporcionar una bóveda digital segura para almacenar credenciales de acceso mediante técnicas modernas de cifrado.

La aplicación está protegida por una **contraseña maestra única**, la cual es utilizada para autenticar al usuario al iniciar el sistema. Esta contraseña nunca se almacena en el disco duro; en su lugar, se utiliza temporalmente para generar una clave de cifrado en memoria (RAM).

Una vez autenticado, el usuario puede:

- Generar contraseñas aleatorias seguras utilizando funciones criptográficas nativas de Python.
- Almacenar credenciales de diferentes servicios.
- Gestionar de forma segura sitios web, nombres de usuario y contraseñas.
- Proteger toda la información mediante cifrado **AES-256** antes de guardarla en una base de datos local.

---

# 📊 Diagramas del Proyecto

## 1. Diagrama de Casos de Uso (UML)

Este diagrama muestra las interacciones entre el usuario y las funcionalidades principales del sistema.

<p align="center">
  <img src="https://github.com/user-attachments/assets/e8ddd182-8761-4003-ac01-6d206708ba9a" alt="Diagrama de Casos de Uso" width="900">
</p>

---

## 2. Diagrama de Secuencia (UML)

Representa el flujo de interacción entre los componentes del sistema durante la ejecución de las operaciones principales.

<p align="center">
  <img src="https://github.com/user-attachments/assets/7b309df1-0810-4e1b-a28d-a336de2b62bd" alt="Diagrama de Secuencia" width="900">
</p>

---

# 🏗️ Diagramas de Arquitectura

## 1. Diagrama en Capas

Describe la organización de la aplicación en diferentes capas y la relación entre ellas.

<p align="center">
  <img src="https://github.com/user-attachments/assets/48f0f126-7915-41a2-acad-27276e114f44" alt="Diagrama en Capas" width="700">
</p>

---

## 2. Diagrama de Despliegue

Muestra la infraestructura necesaria para ejecutar el sistema y la distribución de sus componentes.

<p align="center">
  <img src="https://github.com/user-attachments/assets/bea54c8e-2a5e-4a5a-bd24-06a344b156c9" alt="Diagrama de Despliegue" width="900">
</p>

---

## 🛠️ Tecnologías Utilizadas

- Python
- AES-256
- Base de datos local SQLite
- Tkinter (Interfaz gráfica)
- Biblioteca Cryptography
- Funciones criptográficas nativas de Python
