import customtkinter as ctk
import os
from tkinter import ttk #MODUL PER CREAR ARBRE DE DIRECTORIS
def accio_encriptar():
    print(f"Cifrando: {arxiu_seleccionat}")

def accio_desencriptar():
    print(f"Descifrando: {arxiu_seleccionat}")##PROVANT
def sel_element(nom_arxiu):
    global arxiu_seleccionat
    # Gruta completa per evitar errors si no estàs a la mateixa carpeta
    arxiu_seleccionat = os.path.join(os.getcwd(), nom_arxiu)
    print(f"Seleccionat: {arxiu_seleccionat}")
    # Actualitzem el títol visual
    cami_directori.configure(text=f"Seleccionat: {nom_arxiu}")
    # Activem els botons
    botons_xifrar.configure(state="normal", fg_color="#2ecc71")   
    botons_desxifrar.configure(state="normal", fg_color="#e74c3c")
COLOR_BG = "#0f111a"
COLOR_SIDEBAR = "#161925"
COLOR_CARD = "#212533"
COLOR_ACCENT = "#5c55e6"
app = ctk.CTk()
app.title("Explorador de Fitxers")
app.geometry("950x650")

# Grid principal
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# barra lateral
barra_lateral = ctk.CTkFrame(app, width=200, corner_radius=0, fg_color=COLOR_SIDEBAR)
barra_lateral.grid(row=0, column=0, sticky="nsew")

titol_lateral = ctk.CTkLabel(barra_lateral, text="Accessos ràpids", font=("Arial", 16, "bold"), text_color="white")
titol_lateral.pack(pady=20)

for item in ["Escriptori", "Descargues", "Documents", "Imatges"]:
    colors_botons = ctk.CTkButton(barra_lateral, text=item, fg_color="transparent", text_color="white", hover_color="grey", anchor="w")
    colors_botons.pack(fill="x", padx=10, pady=2)


area_principal = ctk.CTkFrame(app, fg_color=COLOR_BG, corner_radius=0)
area_principal.grid(row=0, column=1, sticky="nsew") # Configuració de la mida de la finestra

# Títol amb el camí del directori
cami_directori = ctk.CTkLabel(area_principal, text=f"Directori: {os.getcwd()}", text_color="white", font=("Arial", 11))
cami_directori.pack(anchor="w", padx=20, pady=10)

#Botons per xifrar i desxifrar
botons_desxifrar = ctk.CTkButton(area_principal, text="Desencriptar", fg_color="#e74c3c", state="disabled", text_color="white", hover_color="red", anchor="w", command=accio_desencriptar)
botons_desxifrar.pack(side="right", padx=20, pady=15)

botons_xifrar = ctk.CTkButton(area_principal, text="Encriptar", fg_color="#2ecc71", state="disabled", text_color="white", hover_color="green", anchor="w", command=accio_encriptar)
botons_xifrar.pack( side="right", padx=0, pady=15)
# El ScrollableFrame es la barra per baixar on aniran els arxius
files_grid = ctk.CTkScrollableFrame(area_principal, fg_color=COLOR_CARD, label_text_color="white")
files_grid.pack(fill="both", expand=True, padx=10, pady=10)

# Configurem 5 columnes per a les icones
for i in range(5):
    files_grid.grid_columnconfigure(i, weight=1)

def llistar_directori():
    
    try:
        items = os.listdir(".")
    except Exception as e:
        items = [f"Error: {e}"]

    row, col = 0, 0

    for name in items:
        es_carpeta = os.path.isdir(name)
        icona = "📁" if es_carpeta else "📄"
        
        # Creem un marc individual per a cada arxiu per controlar el text
        file_container = ctk.CTkFrame(files_grid, fg_color=COLOR_CARD, width=120, height=120)
        file_container.grid(row=row, column=col, padx=5, pady=5)
        
        # Botó amb la icona i el text a sota
        button = ctk.CTkButton(
            file_container,
            text=f"{icona}\n{name}",
            text_color="white",
            font=("Arial", 11),
            fg_color="transparent",
            hover_color="#e5f1fb", # Color blau claret
            width=110,
            height=100,
            compound="top",
            command = lambda n = name: sel_element(n)
        )
        button.pack()

        col += 1
        if col > 4: # 5 icones per fila
            col = 0
            row += 1

llistar_directori()

app.mainloop()