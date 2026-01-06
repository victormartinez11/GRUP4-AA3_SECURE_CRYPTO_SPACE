import customtkinter as ctk
import src.core.authenticate as auth
from src.ui.dashboard import dashboard
import src.config.constants as const
import src.core.file_manager as fm
import os
from tkinter import filedialog

def setup_login_ui(app):
    app.title("Secure Vault Login")
    app.geometry("650x450")

    # Configuració de la graella 
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=3)
    app.grid_rowconfigure(0, weight=1)

    # BARRA LATERAL  
    sidebar_frame = ctk.CTkFrame(app, width=180, corner_radius=0, fg_color=const.COLOR_CARD)
    sidebar_frame.grid(row=0, column=0, sticky="nsew")

    ctk.CTkLabel(sidebar_frame, text="My Secure Vault", font=const.FONT_TITLE, text_color="white").pack(pady=(40, 20))

    # Etiqueta per mostrar la carpeta seleccionada
    label_info_vault = ctk.CTkLabel(sidebar_frame, text="Cap Vault\nSeleccionat", font=const.FONT_SMALL_BOLD, text_color="gray")
    
    def update_vault_label(path):
        nom_vault = os.path.basename(path)
        label_info_vault.configure(text=f"VAULT ACTIU:\n{nom_vault}", text_color=const.COLOR_VISIBLE)

    # Funció per triar carpeta
    def seleccionar_vault_wrapper():
        carpeta = filedialog.askdirectory(title="Selecciona la carpeta del Vault")
        if carpeta:
            os.chdir(carpeta)
            fm.save_config(carpeta)
            update_vault_label(carpeta)

    ctk.CTkButton(sidebar_frame, text="Canviar Carpeta", command=seleccionar_vault_wrapper, 
                  fg_color="#D35400", hover_color="#A04000", width=140).pack(pady=10)
    
    label_info_vault.pack(pady=20)

    # CONTINGUT PRINCIPAL 
    login_frame = ctk.CTkFrame(app, fg_color="transparent")
    register_frame = ctk.CTkFrame(app, fg_color="transparent")

    # Restaurar última carpeta si existeix
    last_vault = fm.load_last_vault()
    if last_vault:
        os.chdir(last_vault)
        update_vault_label(last_vault)

    def switch_to_register():
        login_frame.grid_forget()
        register_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def switch_to_login():
        register_frame.grid_forget()
        login_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def handle_login_click():
        usuari = user_entry.get()
        contra = pass_entry.get()

        try:
            exito, mensaje = auth.login_user(usuari, contra)

            if exito:
                login_status.configure(text=mensaje, text_color="green")
                
                # Transició al dashboard
                def fer_transicio():
                    transition_to_dashboard(app, sidebar_frame, login_frame, register_frame, usuari, contra)
                
                app.after(500, fer_transicio) 
            else:
                login_status.configure(text=mensaje, text_color="red")
        except Exception as e:
            login_status.configure(text=f"Error: {e}", text_color="red")

    def handle_register_click():
        usuari = new_user.get()
        contra = new_pass.get()

        exito, mensaje = auth.register_user(usuari, contra)

        if exito:
            reg_status.configure(text=mensaje, text_color="green")
            new_user.delete(0, 'end')
            new_pass.delete(0, 'end')
        else:
            reg_status.configure(text=mensaje, text_color="red")

    # FORMULARI DE LOGIN
    ctk.CTkLabel(login_frame, text="Inicia Sessió", font=("Arial", 24)).pack(pady=20)
    
    user_entry = ctk.CTkEntry(login_frame, placeholder_text="Usuari", width=220)
    user_entry.pack(pady=10)
    
    pass_entry = ctk.CTkEntry(login_frame, placeholder_text="Contrasenya", show="*", width=220)
    pass_entry.pack(pady=10)
    
    login_status = ctk.CTkLabel(login_frame, text="", font=("Arial", 12))
    login_status.pack(pady=5)
    
    ctk.CTkButton(login_frame, text="Entrar", command=handle_login_click, width=220).pack(pady=10)
                  
    ctk.CTkLabel(login_frame, text="No tens compte?").pack(pady=(20,5))
    ctk.CTkButton(login_frame, text="Crear Compte", command=switch_to_register, 
                  fg_color="transparent", border_width=1, text_color=("black", "blue")).pack(pady=5)

    # FORMULARI DE REGISTRE 
    ctk.CTkLabel(register_frame, text="Nou Usuari", font=("Arial", 24)).pack(pady=20)
    
    new_user = ctk.CTkEntry(register_frame, placeholder_text="Nou Nom d'Usuari", width=220)
    new_user.pack(pady=10)
    
    new_pass = ctk.CTkEntry(register_frame, placeholder_text="Nova Contrasenya", show="*", width=220)
    new_pass.pack(pady=10)
    
    reg_status = ctk.CTkLabel(register_frame, text="", font=("Arial", 12))
    reg_status.pack(pady=5)
    
    ctk.CTkButton(register_frame, text="Registrar-se", fg_color="green", command=handle_register_click, width=220).pack(pady=20)
                  
    ctk.CTkButton(register_frame, text="Tornar al Login", fg_color="transparent", border_width=1, 
                  text_color=("black", "blue"), command=switch_to_login).pack(pady=5)

    # Mostrar login inicialment
    login_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)


def transition_to_dashboard(app, sidebar_frame, login_frame, register_frame, username, password):
    # Netejar finestres anteriors
    sidebar_frame.destroy()
    login_frame.destroy()
    register_frame.destroy()
    
    app.geometry("950x650")
    app.title(f"Secure Vault - {username}")
    
    # Reset del grid
    app.grid_columnconfigure(0, weight=0)
    app.grid_columnconfigure(1, weight=0)
    app.grid_rowconfigure(0, weight=0)
    
    dashboard(app, username, password)
