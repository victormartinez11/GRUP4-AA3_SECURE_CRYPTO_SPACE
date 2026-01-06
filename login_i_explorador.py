import customtkinter as ctk
import os
from tkinter import filedialog
from src.dashboard import dashboard 
import src.core.authenticate as auth


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "last_vault.txt")

# Configuració inicial de l'App
app = ctk.CTk()
app.title("Secure Vault Login")
app.geometry("650x450") 

# Grid per fer la finestra dinàmica
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=3)
app.grid_rowconfigure(0, weight=1)

# Variables globals per a la sessió
usuari_auth = None
pass_auth = None

def carregar_dashboard():
    # Elimina la interfície de login 
    sidebar_frame.destroy()
    login_frame.destroy()
    register_frame.destroy()
    
    app.geometry("950x650")
    app.title(f"Secure Vault - {usuari_auth}")
    
    app.grid_columnconfigure(0, weight=1)
    
    dashboard(app, usuari_auth, pass_auth)

def guardar_configuracio(ruta):
    """Guarda la ruta del vault en un fitxer de text"""
    try:
        with open(CONFIG_FILE, "w") as f:
            f.write(ruta)
    except Exception as e:
        print(f"Error guardant configuració: {e}")

def carregar_ultim_vault():
    """Llegeix l'últim vault obert i l'intenta carregar"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                ruta = f.read().strip()
            
            if os.path.exists(ruta):
                os.chdir(ruta)
                nom_vault = os.path.basename(ruta)
                
               
                label_info_vault.configure(text=f"VAULT ACTIU:\n{nom_vault}", text_color="#2ecc71")
                etiqueta_login.configure(text=f"Sessió restaurada: {nom_vault}", text_color="green")
                print(f"Restaurat vault anterior: {ruta}")
            else:
                label_info_vault.configure(text="L'últim Vault\nja no existeix", text_color="orange")
        except Exception as e:
            print(f"Error carregant config: {e}")

def seleccionar_vault():
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta del Vault")
    if not carpeta:
        return

    try:
        os.chdir(carpeta) 
        nom_vault = os.path.basename(carpeta)
        
        # Guarda la ruta
        guardar_configuracio(carpeta)
        
        # Actualitza la informació a la barra lateral i al login
        label_info_vault.configure(text=f"VAULT ACTIU:\n{nom_vault}", text_color="#2ecc71")
        etiqueta_login.configure(text=f"Carpeta oberta: {nom_vault}", text_color="green")
        print(f"Directori canviat a: {carpeta}")
        
    except Exception as e:
        etiqueta_login.configure(text=f"Error accedint: {e}", text_color="red")

def guardar_usuari():
    usuari = new_user_entry.get()
    contra = new_pass_entry.get()

    exito, mensaje = auth.register_user(usuari, contra)

    if exito:
        etiqueta_missatge.configure(text=mensaje, text_color="green")
        new_user_entry.delete(0, 'end')
        new_pass_entry.delete(0, 'end')
    else:
        etiqueta_missatge.configure(text=mensaje, text_color="red")

def verificar_usuari():
    global usuari_auth
    global pass_auth
    usuari = entry.get()
    contra = password_entry.get()

    try:
        exito, mensaje = auth.login_user(usuari, contra)

        if exito:
            usuari_auth = usuari
            pass_auth = contra
            etiqueta_login.configure(text=mensaje, text_color="green")
            print("Login acceptat. Carregant dashboard...")
            app.after(500, carregar_dashboard) 
        else:
            etiqueta_login.configure(text=mensaje, text_color="red")

    except Exception as e:
        etiqueta_login.configure(text=f"Error al login: {e}", text_color="red")

def show_register():
    login_frame.grid_forget()
    register_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

def show_login():
    register_frame.grid_forget()
    login_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)




# BARRA LATERAL 
sidebar_frame = ctk.CTkFrame(app, width=180, corner_radius=0, fg_color="#212533")
sidebar_frame.grid(row=0, column=0, sticky="nsew")

ctk.CTkLabel(sidebar_frame, text="My Secure Vault", font=("Arial", 20, "bold"), text_color="white").pack(pady=(40, 20))

ctk.CTkButton(sidebar_frame, text="Canviar Carpeta", command=seleccionar_vault, fg_color="#D35400", hover_color="#A04000",width=140).pack(pady=10)

# Etiqueta per mostrar el vault actual a la barra lateral
label_info_vault = ctk.CTkLabel(sidebar_frame, text="Cap Vault\nSeleccionat", font=("Arial", 12, "bold"), text_color="gray")
label_info_vault.pack(pady=20)



login_frame = ctk.CTkFrame(app, fg_color="transparent")
register_frame = ctk.CTkFrame(app, fg_color="transparent")

# login
ctk.CTkLabel(login_frame, text="Inicia Sessió", font=("Arial", 24)).pack(pady=20)

entry = ctk.CTkEntry(login_frame, placeholder_text="Usuari", width=220)
entry.pack(pady=10)

password_entry = ctk.CTkEntry(login_frame, placeholder_text="Contrasenya", show="*", width=220)
password_entry.pack(pady=10)

etiqueta_login = ctk.CTkLabel(login_frame, text="", font=("Arial", 12))
etiqueta_login.pack(pady=5)

ctk.CTkButton(login_frame, text="Entrar", command=verificar_usuari, width=220).pack(pady=10)
ctk.CTkLabel(login_frame, text="No tens compte?").pack(pady=(20,5))
ctk.CTkButton(login_frame, text="Crear Compte", command=show_register, fg_color="transparent", border_width=1, text_color=("black", "blue")).pack(pady=5)

# register
ctk.CTkLabel(register_frame, text="Nou Usuari", font=("Arial", 24)).pack(pady=20)

new_user_entry = ctk.CTkEntry(register_frame, placeholder_text="Nou Nom d'Usuari", width=220)
new_user_entry.pack(pady=10)

new_pass_entry = ctk.CTkEntry(register_frame, placeholder_text="Nova Contrasenya", show="*", width=220)
new_pass_entry.pack(pady=10)

etiqueta_missatge = ctk.CTkLabel(register_frame, text="", font=("Arial", 12))
etiqueta_missatge.pack(pady=5)

ctk.CTkButton(register_frame, text="Registrar-se", fg_color="green", command=guardar_usuari, width=220).pack(pady=20)
ctk.CTkButton(register_frame, text="Tornar al Login", fg_color="transparent", border_width=1, text_color=("black", "blue"), command=show_login).pack(pady=5)

login_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

# Carreguem l'últim vault 
carregar_ultim_vault()

app.mainloop()