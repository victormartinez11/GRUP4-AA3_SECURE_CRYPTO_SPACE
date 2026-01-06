import customtkinter as ctk
import src.core.authenticate as auth
from src.ui.dashboard import dashboard
import src.config.constants as const

def setup_login_ui(app):
    app.title("Secure Vault Login")
    app.geometry("400x400")

    login_frame = ctk.CTkFrame(app, fg_color="transparent")
    register_frame = ctk.CTkFrame(app, fg_color="transparent")
    
    def switch_to_register():
        login_frame.pack_forget()
        register_frame.pack(fill="both", expand=True, pady=20)

    def switch_to_login():
        register_frame.pack_forget()
        login_frame.pack(fill="both", expand=True, pady=20)

    def handle_login_click():
        usuari = user_entry.get()
        contra = pass_entry.get()

        try:
            exito, mensaje = auth.login_user(usuari, contra)

            if exito:
                login_status.configure(text=mensaje, text_color="green")
                print("Login acceptat. Carregant dashboard...")
                
                def fer_transicio():
                    transition_to_dashboard(app, login_frame, register_frame, usuari, contra)
                
                app.after(500, fer_transicio) 
            else:
                login_status.configure(text=mensaje, text_color="red")
        except Exception as e:
            login_status.configure(text=f"Error al llegir: {e}", text_color="red")

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

    ctk.CTkLabel(login_frame, text="Login", font=("Arial", 20)).pack(pady=10)
    
    user_entry = ctk.CTkEntry(login_frame, placeholder_text="Username", width=200)
    user_entry.pack(pady=10)
    
    pass_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=200)
    pass_entry.pack(pady=10)
    
    login_status = ctk.CTkLabel(login_frame, text="", font=("Arial", 12))
    login_status.pack(pady=5)
    
    ctk.CTkButton(login_frame, text="Login", command=handle_login_click).pack(pady=10)
                  
    ctk.CTkLabel(login_frame, text="Don't have an account?", width=200).pack(pady=(20,5))
    ctk.CTkButton(login_frame, text="Register", command=switch_to_register).pack(pady=5)

    ctk.CTkLabel(register_frame, text="Create Account", font=("Arial", 20)).pack(pady=10)
    
    new_user = ctk.CTkEntry(register_frame, placeholder_text="New Username", width=200)
    new_user.pack(pady=10)
    
    new_pass = ctk.CTkEntry(register_frame, placeholder_text="New Password", show="*", width=200)
    new_pass.pack(pady=10)
    
    reg_status = ctk.CTkLabel(register_frame, text="", font=("Arial", 12))
    reg_status.pack(pady=5)
    
    ctk.CTkButton(register_frame, text="Sign Up", fg_color="green", command=handle_register_click).pack(pady=20)
                  
    ctk.CTkButton(register_frame, text="Back to Login", fg_color="gray", command=switch_to_login).pack(pady=5)

    login_frame.pack(fill="both", expand=True, pady=20)


def transition_to_dashboard(app, login_frame, register_frame, username, password):
    login_frame.destroy()
    register_frame.destroy()
    
    app.geometry("950x650")
    app.title(f"Secure Vault - {username}")
    
    dashboard(app, username, password)
