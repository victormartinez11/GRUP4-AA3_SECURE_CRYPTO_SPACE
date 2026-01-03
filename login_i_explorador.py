import customtkinter as ctk
import os
from src.dashboard import dashboard 
import src.core.authenticate as auth
app = ctk.CTk()
app.title("Secure Vault Login")
app.geometry("400x400") 


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
    login_correcte = False

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
        etiqueta_login.configure(text=f"Error al llegir: {e}", text_color="red")
def show_register():
    login_frame.pack_forget()
    register_frame.pack(fill="both", expand=True, pady=20)

def show_login():
    register_frame.pack_forget()
    login_frame.pack(fill="both", expand=True, pady=20)


login_frame = ctk.CTkFrame(app, fg_color="transparent")
register_frame = ctk.CTkFrame(app, fg_color="transparent")


ctk.CTkLabel(login_frame, text="Login", font=("Arial", 20)).pack(pady=10)

entry = ctk.CTkEntry(login_frame, placeholder_text="Username", width=200)
entry.pack(pady=10)

password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=200)
password_entry.pack(pady=10)

etiqueta_login = ctk.CTkLabel(login_frame, text="", font=("Arial", 12))
etiqueta_login.pack(pady=5)

ctk.CTkButton(login_frame, text="Login", command=verificar_usuari).pack(pady=10)
ctk.CTkLabel(login_frame, text="Don't have an account?", width=200).pack(pady=(20,5))
ctk.CTkButton(login_frame, text="Register", command=show_register).pack(pady=5)

ctk.CTkLabel(register_frame, text="Create Account", font=("Arial", 20)).pack(pady=10)

new_user_entry = ctk.CTkEntry(register_frame, placeholder_text="New Username", width=200)
new_user_entry.pack(pady=10)

new_pass_entry = ctk.CTkEntry(register_frame, placeholder_text="New Password", show="*", width=200)
new_pass_entry.pack(pady=10)

etiqueta_missatge = ctk.CTkLabel(register_frame, text="", font=("Arial", 12))
etiqueta_missatge.pack(pady=5)

ctk.CTkButton(register_frame, text="Sign Up", fg_color="green", command=guardar_usuari).pack(pady=20)
ctk.CTkButton(register_frame, text="Back to Login", fg_color="gray", command=show_login).pack(pady=5)


login_frame.pack(fill="both", expand=True, pady=20)


def carregar_dashboard():
    login_frame.destroy()
    register_frame.destroy()
    
    app.geometry("950x650")
    app.title(f"Secure Vault-{usuari_auth}")
    dashboard(app, usuari_auth, pass_auth)

app.mainloop()