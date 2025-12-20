import customtkinter as ctk
import os
from PIL import Image   
from src.sidebar import create_sidebar
from src.file_encript import encrypt_file, decrypt_file

# COLORS
COLOR_BG = "#0f111a"
COLOR_SIDEBAR = "#161925"
COLOR_CARD = "#212533"
COLOR_ACCENT = "#5c55e6"
GREEN="#2ecc71"
RED="#c0392b"
# IMATGES
try:
    IMG_FOLDER = ctk.CTkImage(light_image=Image.open("assets/folder.png"), dark_image=Image.open("assets/folder.png"), size=(50, 50))
    IMG_FILE = ctk.CTkImage(light_image=Image.open("assets/file.png"), dark_image=Image.open("assets/file.png"), size=(50, 50))
except Exception as e:
    print(f"Error loading images: {e}")

def dashboard(app):

    app_state = [False]
    # Grid conf
    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    # Sidebar
    create_sidebar(app, COLOR_SIDEBAR)

    # Main 
    area_principal = ctk.CTkFrame(app, fg_color=COLOR_BG, corner_radius=0)
    area_principal.grid(row=0, column=1, sticky="nsew")

    # Directory Path 
    path_container = ctk.CTkFrame(area_principal, fg_color="transparent")
    path_container.pack(fill="x", padx=20, pady=(20, 10))
    
    #MODIFICAR PARA QUE SEA FUNCION Y PASE RUTA POR PARAMETRO
    ruta_static = ctk.CTkLabel(path_container, text="Ruta:", text_color="#5c55e6", font=("Consolas", 14, "bold"))
    ruta_static.pack(side="left")
    
    ruta_actual = f" {os.getcwd()}"
    cami_directori = ctk.CTkLabel(path_container, text=ruta_actual, text_color="#a0a0a0", font=("Consolas", 14))
    cami_directori.pack(side="left")
    ########################
    # Action Bar 
    action_bar = ctk.CTkFrame(area_principal, fg_color="#161925", corner_radius=15, height=50)
    action_bar.pack(fill="x", padx=20, pady=10)
    
    # Label for file selection
    label_arxiu_seleccionat = ctk.CTkLabel(action_bar, text="Ningún archivo seleccionado", text_color="gray", font=("Arial", 12))
    label_arxiu_seleccionat.pack(side="left", padx=20, pady=15)

    # Actions
    def accio_encriptar():
        if not app_state[0]:
            return
            
        dialog = ctk.CTkInputDialog(text="Introduce la contraseña para encriptar:", title="Encriptar")
        password = dialog.get_input()
        
        if password:
            # Llamamos a la función de encriptación
            exito, mensaje = encrypt_file(app_state[0], password)
            if exito:
                print(f"Éxito: {mensaje}")
                # Actualizamos la vista
                llistar_directori()
                label_arxiu_seleccionat.configure(text="S'ha encriptat l'arxiu", text_color=GREEN)
                # Reseteamos estado botones
                botons_xifrar.configure(state="disabled")
                botons_desxifrar.configure(state="disabled")
            else:
                print(f"Error: {mensaje}")
                label_arxiu_seleccionat.configure(text=f"Error: {mensaje}", text_color=RED)

    def accio_desencriptar():
        if not app_state[0]:
            return

        dialog = ctk.CTkInputDialog(text="Introduce la contraseña para desencriptar:", title="Desencriptar")
        password = dialog.get_input()
        
        if password:
            # Llamamos a la función de desencriptación
            exito, mensaje = decrypt_file(app_state[0], password)
            if exito:
                print(f"Éxito: {mensaje}")
                llistar_directori()
                label_arxiu_seleccionat.configure(text="S'ha desencriptat l'arxiu", text_color=GREEN)
                botons_xifrar.configure(state="disabled")
                botons_desxifrar.configure(state="disabled")
            else:
                print(f"Error: {mensaje}")
                label_arxiu_seleccionat.configure(text=f"Error: {mensaje}", text_color=RED)

    # Buttons    
    botons_desxifrar = ctk.CTkButton(action_bar, text="DESENCRIPTAR", fg_color="RED", border_width=1, border_color="gray", state="disabled", text_color="gray", hover_color="#e74c3c", width=120, command=accio_desencriptar)
    botons_desxifrar.pack(side="right", padx=(10, 20), pady=10)

    botons_xifrar = ctk.CTkButton(action_bar, text="ENCRIPTAR", fg_color="GREEN", border_width=1, border_color="gray", state="disabled", text_color="gray", hover_color="#2ecc71", width=120, command=accio_encriptar)
    botons_xifrar.pack(side="right", padx=0, pady=10)

    # Selection Logic
    def sel_element(nom_arxiu):
        arxiu_seleccionat = os.path.join(os.getcwd(), nom_arxiu)
        app_state[0] = arxiu_seleccionat
        print(f"Seleccionat: {arxiu_seleccionat}")
        
        # Update selected
        label_arxiu_seleccionat.configure(text=f"{nom_arxiu}", text_color="white")
        
        if nom_arxiu.endswith(".enc"):
            # Encriptar
            botons_xifrar.configure(state="disabled", text_color="gray", border_color="gray")   
            botons_desxifrar.configure(state="normal", text_color="white", border_color="#e74c3c")
        else:
            # Desencriptar
            botons_xifrar.configure(state="normal", text_color="white", border_color="#2ecc71")   
            botons_desxifrar.configure(state="disabled", text_color="gray", border_color="gray")

    # Files Grid
    files_grid = ctk.CTkScrollableFrame(area_principal, fg_color=COLOR_CARD, label_text_color="white")
    files_grid.pack(fill="both", expand=True, padx=10, pady=10)
    
    for i in range(5):
        files_grid.grid_columnconfigure(i, weight=1)

    # List Directory
    def llistar_directori():
        for widget in files_grid.winfo_children():
            widget.destroy()

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
