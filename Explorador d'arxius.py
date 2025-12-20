import customtkinter as ctk
from src.dashboard import dashboard

# VARIABLE DE ESTAT 
GLOBAL_APP_WINDOW = None

app = ctk.CTk()
app.title("Explorador de Fitxers")
app.geometry("950x650")

dashboard(app)

app.mainloop()