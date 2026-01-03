import customtkinter as ctk
import os
from tkinter import filedialog
from src.dashboard import dashboard 
import src.core.authenticate as auth

# Configuració inicial de l'App
app = ctk.CTk()
app.title("Secure Vault Login")
app.geometry("650x450") 

# Configurar Grid principal: 
# Columna 0 = Sidebar, Columna 1 = Contingut 
app.grid_columnconfigure(0, weight=0)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# Variables globals per a la sessió
usuari_auth = None
pass_auth = None


def carregar_dashboard():
    # Netejar tota la interfície de login
    sidebar_frame.destroy()
    login_frame.destroy()
    register_frame.destroy()
    
    # configurar finestra per al dashboard
    app.geometry("950x650")
    app.title(f"Secure Vault - {usuari_auth}")
    
    # Restaurar grid
    app.grid_columnconfigure(0, weight=1)
    
    # Carregar dashboard passant les credencials
    dashboard(app, usuari_auth, pass_auth)

def seleccionar_vault():
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta del Vault")
    if not carpeta:
        return
    
    if os.path.exists(ruta_clau):
        try:
            os.chdir(carpeta) # Canviem el directori de treball al Vault seleccionat
            nom_vault = os.path.basename(carpeta)
            etiqueta_login.configure(text=f"Vault carregat: {nom_vault}", text_color="#3498db")
            print(f"Directori canviat a: {carpeta}")
        except Exception as e:
            etiqueta_login.configure(text=f"Error accedint: {e}", text_color="red")
    else:
        etiqueta_login.configure(text="Error: Aquesta carpeta no és un Vault vàlid", text_color="red")

def guardar_usuari():
    usuari = new_user_entry.get()
    contra = new_pass_entry.get()

    # Registre utilitzant el mòdul d'autenticació
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
        # Login utilitzant el mòdul d'autenticació
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
sidebar_frame = ctk.CTkFrame(app, width=160, corner_radius=0)
sidebar_frame.grid(row=0, column=0, sticky="nsew")

ctk.CTkLabel(sidebar_frame, text="My Secure Vault", font=("Arial", 18, "bold")).pack(pady=30)

# Botó per obrir vault extern
ctk.CTkButton(
    sidebar_frame, 
    text="Obrir Vault Existent", 
    command=seleccionar_vault, 
    fg_color="#D35400", 
    hover_color="#A04000"
).pack(pady=10, padx=15)

ctk.CTkLabel(sidebar_frame, text="Selecciona una carpeta\nque contingui\n'file_salt.key'", font=("Arial", 10), text_color="gray").pack(pady=5)


# FRAMES DE CONTINGUT 
login_frame = ctk.CTkFrame(app, fg_color="transparent")
register_frame = ctk.CTkFrame(app, fg_color="transparent")


ctk.CTkLabel(login_frame, text="Login", font=("Arial", 24)).pack(pady=20)

entry = ctk.CTkEntry(login_frame, placeholder_text="Username", width=220)
entry.pack(pady=10)

password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=220)
password_entry.pack(pady=10)

etiqueta_login = ctk.CTkLabel(login_frame, text="", font=("Arial", 12))
etiqueta_login.pack(pady=5)

ctk.CTkButton(login_frame, text="Login", command=verificar_usuari, width=220).pack(pady=10)
ctk.CTkLabel(login_frame, text="Don't have an account?").pack(pady=(20,5))
ctk.CTkButton(login_frame, text="Create Account", command=show_register, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE")).pack(pady=5)


ctk.CTkLabel(register_frame, text="Create Account", font=("Arial", 24)).pack(pady=20)

new_user_entry = ctk.CTkEntry(register_frame, placeholder_text="New Username", width=220)
new_user_entry.pack(pady=10)

new_pass_entry = ctk.CTkEntry(register_frame, placeholder_text="New Password", show="*", width=220)
new_pass_entry.pack(pady=10)

etiqueta_missatge = ctk.CTkLabel(register_frame, text="", font=("Arial", 12))
etiqueta_missatge.pack(pady=5)

ctk.CTkButton(register_frame, text="Sign Up", fg_color="green", command=guardar_usuari, width=220).pack(pady=20)
ctk.CTkButton(register_frame, text="Back to Login", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=show_login).pack(pady=5)


# Mostrem d'inici el frame de Login
login_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

app.mainloop()