import customtkinter as ctk

app = ctk.CTk()
app.title("Login")
app.geometry("400x200")

def show_register():
    login_frame.pack_forget()    # Ocultar el login
    register_frame.pack(fill = "both", expand=True, pady=20)

def show_login():
    register_frame.pack_forget()   # Ocultar menu de registre
    login_frame.pack(fill="both", expand=True, pady=20)

login_frame = ctk.CTkFrame(app, fg_color="transparent")
login_frame.pack(fill="both", expand=True, pady=20)


label = ctk.CTkLabel(app, text="Login")
label.pack(pady=20)


entry = ctk.CTkEntry(app, placeholder_text="Username", width=200)
entry.pack(pady=20)

password_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=200)
password_entry.pack(pady=20)

login_button = ctk.CTkButton(app, text="Login", command=lambda: print("Login"))
login_button.pack(pady=20)


register = ctk.CTkLabel(app, text="Don't have an account?", width=200, anchor="center")
register.pack(pady=20)

register_button = ctk.CTkButton(login_frame, text="Register", command=show_register)
register_button.pack(pady=20)

# registrarse
register_frame = ctk.CTkFrame(app, fg_color="blue")

label_register = ctk.CTkLabel(register_frame, text="Create Account")
label_register.pack(pady=10)

new_user = ctk.CTkEntry(register_frame, placeholder_text="New Username", width=200)
new_user.pack(pady=10)

new_password = ctk.CTkEntry(register_frame, placeholder_text="New Password", show="*", width=200)
new_password.pack(pady=10)

app.mainloop()