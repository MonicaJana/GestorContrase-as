import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import encriptacion
import base_datos

# Configura la apariencia moderna de la interfaz con customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AplicacionGestor:
    def __init__(self):
        base_datos.inicializar_db()
        self.llave_aes = None  # Se almacenará la llave en RAM durante la sesión
        self.sal = base_datos.obtener_sal()
        
        # Muestra la ventana de login/registro al iniciar
        self.mostrar_ventana_login()

    def mostrar_ventana_login(self):
        self.ventana_login = ctk.CTk()
        self.ventana_login.title("Bóveda - Acceso")
        self.ventana_login.geometry("400x250")
        self.ventana_login.resizable(False, False)

        # Si no existe Sal en la DB, es el primer acceso a la aplicación
        if self.sal is None:
            lbl_titulo = ctk.CTkLabel(self.ventana_login, text="Configura tu Contraseña Maestra", font=("Arial", 16, "bold"))
            lbl_titulo.pack(pady=20)
            btn_texto = "Registrar Clave"
        else:
            lbl_titulo = ctk.CTkLabel(self.ventana_login, text="Introduce tu Contraseña Maestra", font=("Arial", 16, "bold"))
            lbl_titulo.pack(pady=20)
            btn_texto = "Desbloquear"

        self.txt_maestra = ctk.CTkEntry(self.ventana_login, show="*", width=250, placeholder_text="Contraseña Maestra")
        self.txt_maestra.pack(pady=10)

        btn_accion = ctk.CTkButton(self.ventana_login, text=btn_texto, command=self.procesar_autenticacion)
        btn_accion.pack(pady=20)

        self.ventana_login.mainloop()

    def procesar_autenticacion(self):
        password_ingresada = self.txt_maestra.get()
        if not password_ingresada:
            messagebox.showerror("Error", "El campo no puede estar vacío.")
            return

        if self.sal is None:
            # Flujo de registro: crear nueva Sal para la contraseña maestra
            self.sal = encriptacion.secrets.token_bytes(16)
            base_datos.guardar_sal(self.sal)
            self.llave_aes = encriptacion.derivar_llave_maestra(password_ingresada, self.sal)
            messagebox.showinfo("Éxito", "Contraseña Maestra configurada correctamente.")
            self.ventana_login.destroy()
            self.mostrar_ventana_principal()
        else:
            # Flujo de acceso: validar contraseña maestra existente
            llave_prueba = encriptacion.derivar_llave_maestra(password_ingresada, self.sal)
            # Valida la contraseña intentando cifrar/descifrar un dato de prueba
            try:
                prueba_crypto = encriptacion.encriptar_dato("test", llave_prueba)
                encriptacion.desencriptar_dato(prueba_crypto, llave_prueba)
                self.llave_aes = llave_prueba
                self.ventana_login.destroy()
                self.mostrar_ventana_principal()
            except Exception:
                messagebox.showerror("Error", "Contraseña Maestra incorrecta.")

    def mostrar_ventana_principal(self):
        self.ventana_principal = ctk.CTk()
        self.ventana_principal.title("Gestor de Contraseñas Seguro")
        self.ventana_principal.geometry("650x500")

        # === SECCIÓN SUPERIOR: Generador de contraseñas ===
        marco_gen = ctk.CTkFrame(self.ventana_principal)
        marco_gen.pack(pady=15, padx=20, fill="x")

        # El campo de texto de salida y los botones de control
        self.txt_password_generada = ctk.CTkEntry(marco_gen, placeholder_text="Contraseña Generada", width=300)
        self.txt_password_generada.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        btn_generar = ctk.CTkButton(marco_gen, text="Generar", width=100, command=self.evento_generar)
        btn_generar.grid(row=0, column=2, padx=10, pady=10)

        btn_copiar = ctk.CTkButton(marco_gen, text="Copiar", width=80, command=self.evento_copiar)
        btn_copiar.grid(row=0, column=3, padx=10, pady=10)

        # Fila 1 - [FUNCIONALIDAD: Elegir Longitud]: Menú desplegable
        lbl_longitud = ctk.CTkLabel(marco_gen, text="Longitud:", font=("Arial", 12))
        lbl_longitud.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.cmb_longitud = ctk.CTkComboBox(marco_gen, values=["8", "12", "16", "20", "24"], width=80)
        self.cmb_longitud.set("16") # Valor por defecto seguro
        self.cmb_longitud.grid(row=1, column=0, padx=80, pady=5, sticky="w")

        # [FUNCIONALIDAD: Incluir/Excluir Símbolos]: Interruptor (Switch)
        self.switch_simbolos = ctk.CTkSwitch(marco_gen, text="¿Incluir Símbolos especiales?", font=("Arial", 12))
        self.switch_simbolos.select() # Activado por defecto
        self.switch_simbolos.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # [FUNCIONALIDAD: Muestra Nivel de Seguridad]: Etiqueta dinámica
        lbl_seg_titulo = ctk.CTkLabel(marco_gen, text="Seguridad de la clave:", font=("Arial", 12, "bold"))
        lbl_seg_titulo.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.lbl_nivel_seguridad = ctk.CTkLabel(marco_gen, text="Esperando contraseña...", font=("Arial", 12, "italic"), text_color="gray")
        self.lbl_nivel_seguridad.grid(row=2, column=1, padx=10, pady=5, sticky="w", columnspan=2)

        self.ventana_principal.mainloop()

    def evento_generar(self):
        
        # 1. Captura la longitud seleccionada en el menú y convertirla a número entero
        longitud_elegida = int(self.cmb_longitud.get())
        
        # 2. Captura si el switch de símbolos está encendido (True) o apagado (False)
        incluye_especiales = bool(self.switch_simbolos.get())
        
        # 3. Invoca la lógica de encriptacion
        clave_nueva = encriptacion.generar_password_aleatorio(longitud_elegida, incluye_especiales)
        
        # 4. Muestra el texto generado en la pantalla
        self.txt_password_generada.delete(0, tk.END)
        self.txt_password_generada.insert(0, clave_nueva)
        
        # 5. [FUNCIONALIDAD: Muestra Nivel de Seguridad]
        texto_seguridad, color_visual = encriptacion.evaluar_nivel_seguridad(clave_nueva)
        self.lbl_nivel_seguridad.configure(text=texto_seguridad, text_color=color_visual)

    def evento_copiar(self):
        # Copia la contraseña generada al portapapeles del sistema
        clave = self.txt_password_generada.get()
        if clave:
            self.ventana_principal.clipboard_clear()
            self.ventana_principal.clipboard_append(clave)
            messagebox.showinfo("Portapapeles", "Contraseña copiada al portapapeles.")

