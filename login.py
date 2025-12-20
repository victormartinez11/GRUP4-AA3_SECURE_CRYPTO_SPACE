import customtkinter as ctk
import os 

app = ctk.CTk()
app.title("Login System")
app.geometry("400x400")

def guardar_usuari():
    usuari = new_user_entry.get()
    contra = new_pass_entry.get()

    if usuari == "" or contra == "":
        etiqueta_missatge.configure(text="Has de omplir tots els camps!", text_color="red")
        return

    try:
        with open("registre.txt", "w") as fitxer:
            fitxer.write(f"{usuari},{contra}\n")
        
        print(f"S'ha guardat l'usuari: {usuari}")

        etiqueta_missatge.configure(text="Saved successfully!", text_color="green")
    except Exception as e:
        etiqueta_missatge.configure(text=f"Error: {e}", text_color="red")


def verificar_usuari():
    usuari = entry.get()
    contra = password_entry.get()

    login_correcte = False

    try:
        with open("registre.txt","r") as fitxer:
            for linia in fitxer:
                dades = linia.strip().split(",")

                if len(dades) == 2:
                    usuari_guardat = dades[0]
                    contra_guardada = dades[1]

                    if usuari_guardat == usuari and contra_guardada == contra:
                        login_correcte = True
                        break 

        if login_correcte:
            etiqueta_login.configure(text="Login Correcte!", text_color="green")
            print("Login acceptat")
           
        else:
            etiqueta_login.configure(text="Usuari o contrasenya incorrectes", text_color="red")

    except FileNotFoundError:
        etiqueta_login.configure(text="Encara no hi ha usuaris registrats", text_color="orange")


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

etiqueta_login = ctk.CTkLabel(login_frame, text="", font=("Arial", 12))
etiqueta_login.pack(pady=5)

button = ctk.CTkButton(login_frame, text="Login", command=verificar_usuari)
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

etiqueta_missatge = ctk.CTkLabel(register_frame, text="", font=("Arial", 12))
etiqueta_missatge.pack(pady=5)

# Botó per confirmar la creació de compte
btn_confirm = ctk.CTkButton(register_frame, text="Sign Up", fg_color="green", command=guardar_usuari)
btn_confirm.pack(pady=20)

# Botó per tornar al menu de login
btn_back = ctk.CTkButton(register_frame, text="Back to Login", fg_color="gray", command=show_login)
btn_back.pack(pady=5)

app.mainloop()