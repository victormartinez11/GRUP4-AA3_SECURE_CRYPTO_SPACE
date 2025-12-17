import customtkinter as ctk

app = ctk.CTk()
app.title("Login System")
app.geometry("400x400")


def show_register():
    login_frame.pack_forget()  # Amaga el menu de Login
    register_frame.pack(fill="both", expand=True, pady=20) # Mostra el menu de Register

def show_login():
    register_frame.pack_forget() # Amaga el menu de Register
    login_frame.pack(fill="both", expand=True, pady=20) # Mostra el menu de Login


# Crea un contenidor transparent per al login
login_frame = ctk.CTkFrame(app, fg_color="transparent")
login_frame.pack(fill="both", expand=True, pady=20) 

label = ctk.CTkLabel(login_frame, text="Login", font=("Arial", 20))
label.pack(pady=10)

entry = ctk.CTkEntry(login_frame, placeholder_text="Username", width=200)
entry.pack(pady=10)

password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=200)
password_entry.pack(pady=10)

button = ctk.CTkButton(login_frame, text="Login", command=lambda: print("Login clicked"))
button.pack(pady=10)

register_label = ctk.CTkLabel(login_frame, text="Don't have an account?", width=200, anchor="center")
register_label.pack(pady=(20,5))

register_button = ctk.CTkButton(login_frame, text="Register", command=show_register)
register_button.pack(pady=5)



# Crea el contenidor per al register 
register_frame = ctk.CTkFrame(app, fg_color="transparent")

label_reg = ctk.CTkLabel(register_frame, text="Create Account", font=("Arial", 20))
label_reg.pack(pady=10)

# Demana el nou nom d'usuari
new_user_entry = ctk.CTkEntry(register_frame, placeholder_text="New Username", width=200)
new_user_entry.pack(pady=10)

# Demana la nova contrasenya
new_pass_entry = ctk.CTkEntry(register_frame, placeholder_text="New Password", show="*", width=200)
new_pass_entry.pack(pady=10)

# Botó per confirmar la creació de compte
btn_confirm = ctk.CTkButton(register_frame, text="Sign Up", fg_color="green", command=lambda: print("Registered!"))
btn_confirm.pack(pady=20)

# Botó per tornar al menu de login
btn_back = ctk.CTkButton(register_frame, text="Back to Login", fg_color="gray", command=show_login)
btn_back.pack(pady=5)

app.mainloop()  