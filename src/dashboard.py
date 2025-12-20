import customtkinter as ctk
import os
from PIL import Image   
from src.sidebar import create_sidebar

# COLORS
COLOR_BG = "#0f111a"
COLOR_SIDEBAR = "#161925"
COLOR_CARD = "#212533"
COLOR_ACCENT = "#5c55e6"

# IMATGES
try:
    IMG_FOLDER = ctk.CTkImage(light_image=Image.open("assets/folder.png"), dark_image=Image.open("assets/folder.png"), size=(50, 50))
    IMG_FILE = ctk.CTkImage(light_image=Image.open("assets/file.png"), dark_image=Image.open("assets/file.png"), size=(50, 50))
except Exception as e:
    print(f"Error loading images: {e}")

def dashboard(app):
    # Grid conf
    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    # Sidebar
    create_sidebar(app, COLOR_SIDEBAR)

    # Main 
    area_principal = ctk.CTkFrame(app, fg_color=COLOR_BG, corner_radius=0)
    area_principal.grid(row=0, column=1, sticky="nsew")

    # Directory Path Label
    current_dir_text = f"Directori: {os.getcwd()}"
    cami_directori = ctk.CTkLabel(area_principal, text=current_dir_text, text_color="white", font=("Arial", 11))
    cami_directori.pack(anchor="w", padx=20, pady=10)

    # Actions TEMPORAL DESPRES DE LA IMPLEMENTACIO
    def accio_encriptar():
        print("Cifrando...") # Placeholder
    
    def accio_desencriptar():
        print("Descifrando...") # Placeholder

    # Buttons
    botons_desxifrar = ctk.CTkButton(area_principal, text="Desencriptar", fg_color="#e74c3c", state="disabled", text_color="white", hover_color="red", anchor="w", command=accio_desencriptar)
    botons_desxifrar.pack(side="right", padx=20, pady=15)

    botons_xifrar = ctk.CTkButton(area_principal, text="Encriptar", fg_color="#2ecc71", state="disabled", text_color="white", hover_color="green", anchor="w", command=accio_encriptar)
    botons_xifrar.pack(side="right", padx=0, pady=15)

    # Files Grid
    files_grid = ctk.CTkScrollableFrame(area_principal, fg_color=COLOR_CARD, label_text_color="white")
    files_grid.pack(fill="both", expand=True, padx=10, pady=10)
    
    for i in range(5):
        files_grid.grid_columnconfigure(i, weight=1)

    # Selection Logic
    def sel_element(nom_arxiu):
        arxiu_seleccionat = os.path.join(os.getcwd(), nom_arxiu)
        print(f"Seleccionat: {arxiu_seleccionat}")
        cami_directori.configure(text=f"Seleccionat: {nom_arxiu}")
        
        if nom_arxiu.endswith(".enc"):
            botons_xifrar.configure(state="disabled", fg_color="#2ecc71")   
            botons_desxifrar.configure(state="normal", fg_color="#e74c3c")
        else:
            botons_xifrar.configure(state="normal", fg_color="#2ecc71")   
            botons_desxifrar.configure(state="disabled", fg_color="#e74c3c")

    # List Directory
    def llistar_directori():
        try:
            items = os.listdir(".")
        except Exception as e:
            items = [f"Error: {e}"]

        row, col = 0, 0
        for name in items:
            es_carpeta = os.path.isdir(name)
            
            # Select icon
            if IMG_FOLDER and IMG_FILE:
                icon_image = IMG_FOLDER if es_carpeta else IMG_FILE
                text_content = name
            else:
                # Fallback if images fail
                icon_char = "📁" if es_carpeta else "📄"
                icon_image = None
                text_content = f"{icon_char}\n{name}"
            
            file_container = ctk.CTkFrame(files_grid, fg_color=COLOR_CARD, width=120, height=120)
            file_container.grid(row=row, column=col, padx=5, pady=5)
            
            button = ctk.CTkButton(
                file_container,
                text=text_content,
                image=icon_image,
                text_color="white",
                font=("Arial", 11),
                fg_color="transparent",
                hover_color="#e5f1fb",
                width=110,
                height=100,
                compound="top",
                command=lambda n=name: sel_element(n)
            )
            button.pack()

            col += 1
            if col > 4:
                col = 0
                row += 1

    llistar_directori()
