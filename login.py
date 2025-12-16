import customtkinter as ctk

app = ctk.CTk()
app.title("Login")
app.geometry("400x200")


label = ctk.CTkLabel(app, text="Login")
label.pack(pady=20)


entry = ctk.CTkEntry(app, placeholder_text="Username", width=200)
entry.pack(pady=20)

password_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=200)
password_entry.pack(pady=20)

button = ctk.CTkButton(app, text="Login", command=lambda: print("Login"))
button.pack(pady=20)


register = ctk.CTkLabel(app, text="Don't have an account?", width=200, anchor="center")
register.pack(pady=20)

register_button = ctk.CTkButton(app, text="Register", command=lambda: print("Register"))
register_button.pack(pady=20)

app.mainloop()