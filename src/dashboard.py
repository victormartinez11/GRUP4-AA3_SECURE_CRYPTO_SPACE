import customtkinter as ctk
import os
from PIL import Image   
from src.sidebar import create_sidebar
from src.file_encript import encrypt_file, decrypt_file
import datetime

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
    IMG_LOCK   = ctk.CTkImage(light_image=Image.open("assets/candado.png"), dark_image=Image.open("assets/candado.png"), size=(50, 50))
except Exception as e:
    print(f"Error loading images: {e}")

def dashboard(app, current_user):

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

    # FILES GRID
    files_grid = ctk.CTkScrollableFrame(area_principal, fg_color="transparent")
    files_grid.pack(fill="both", expand=True, padx=20, pady=10)

    def sel_element(name):
        ruta_absoluta = os.getcwd()
        full_path = os.path.join(ruta_absoluta, name)
        app_state[0] = full_path
        
        label_arxiu_seleccionat.configure(text=f"Seleccionado: {name}", text_color="white")
        
        if os.path.isdir(full_path):
            botons_xifrar.configure(state="disabled")
            botons_desxifrar.configure(state="disabled")
            return

        if name.endswith(".enc"):
            botons_xifrar.configure(state="disabled")
            botons_desxifrar.configure(state="normal")
        else:
            botons_xifrar.configure(state="normal")
            botons_desxifrar.configure(state="disabled")


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
    def llistar_directori():
        # Neteja de widgets anteriors
        for widget in files_grid.winfo_children():
            widget.destroy()
        #Llista de fitxers
        try:
            ruta_absoluta = os.getcwd()
            items = os.listdir(ruta_absoluta)
        except Exception as e:
            items = []
            print(f"Error: {e}")
        #Configuracio de columnes
        files_grid.grid_columnconfigure(0, weight=0, minsize=40) # Icono 
        files_grid.grid_columnconfigure(1, weight=2, minsize=70) # Nombre 
        files_grid.grid_columnconfigure(2, weight=1, minsize=120) # Fecha 
        files_grid.grid_columnconfigure(3, weight=0, minsize=80)  # Tamaño 
        files_grid.grid_columnconfigure(4, weight=0, minsize=100) # Estado 

        # CAPSALERES
        fuente_header = ("Arial", 12, "bold")
        color_header = "#5c55e6"
        
        headers = ["", "NOMBRE", "FECHA", "TAMAÑO", "ESTADO"] 
        
        col_configs = [
            {"anchor": "center", "justify": "center", "padx": 5}, # Icono
            {"anchor": "w",      "justify": "left",   "padx": 5}, # Nombre
            {"anchor": "w",      "justify": "left",   "padx": 5}, # Fecha
            {"anchor": "e",      "justify": "right",  "padx": 5}, # Tamaño
            {"anchor": "e",      "justify": "right",  "padx": (5, 10)} # Estado
        ]
        
        for i, h in enumerate(headers):
            cfg = col_configs[i]
            ctk.CTkLabel(
                files_grid, 
                text=h, 
                font=fuente_header, 
                text_color=color_header,
                anchor=cfg["anchor"]
            ).grid(row=0, column=i, sticky="ew", padx=cfg["padx"], pady=(5, 10))
        #FILES
        row = 1
        for name in items:
            if name.startswith("."): 
                print(f"Ignorando archivo oculto: {name}")
                continue 
            full_path = os.path.join(ruta_absoluta, name)
            
            try:
                stats = os.stat(full_path)
                es_carpeta = os.path.isdir(full_path)
                es_encriptado = name.endswith(".enc")
                fecha_ts = stats.st_mtime
                fecha_txt = datetime.datetime.fromtimestamp(fecha_ts).strftime('%Y-%m-%d %H:%M')
                
                if es_carpeta:
                    size_txt = "-"
                else:
                    size_txt = f"{stats.st_size / 1024:.1f} KB"

                # ICONS LOGIC
                if es_carpeta:
                    target_img = IMG_FOLDER
                    fallback_txt = "DIR"
                    estado_txt = ""
                    color_estado = "white"
                elif es_encriptado:
                    target_img = IMG_LOCK
                    fallback_txt = "LOCK"
                    estado_txt = "ENCRIPTADO"
                    color_estado = "#ff4757"
                else: 
                    target_img = IMG_FILE
                    fallback_txt = "FILE"
                    estado_txt = "VISIBLE"
                    color_estado = "#2ed573"
            
                if target_img is not None:
                    img_actual = target_img
                    txt_icono = ""  
                else:
                    img_actual = None
                    txt_icono = fallback_txt

            except Exception:
                continue 
            pady_fila = 2 
            # ICONO
            ctk.CTkLabel(
                files_grid, 
                text=txt_icono,   
                image=img_actual,  
                width=30,
                anchor="center"
            ).grid(row=row, column=0, sticky="ew", padx=col_configs[0]["padx"], pady=pady_fila)

            # NOMBRE 
            btn_nombre = ctk.CTkButton(
                files_grid,
                text=name,
                font=("Arial", 12),
                fg_color="transparent",
                text_color="white", 
                hover_color="#2f3542",
                anchor="w", 
                height=24,  
                command=lambda n=name: sel_element(n)
            )
            btn_nombre.grid(row=row, column=1, sticky="ew", padx=col_configs[1]["padx"], pady=pady_fila)
            
            # DATA
            ctk.CTkLabel(
                files_grid, 
                text=fecha_txt, 
                font=("Arial", 12), 
                text_color="gray", 
                anchor="w"
            ).grid(row=row, column=2, sticky="ew", padx=col_configs[2]["padx"], pady=pady_fila)

            # TAMANY
            ctk.CTkLabel(
                files_grid, 
                text=size_txt, 
                font=("Arial", 12), 
                text_color="gray", 
                anchor="e"
            ).grid(row=row, column=3, sticky="ew", padx=col_configs[3]["padx"], pady=pady_fila)

            # ESTAT
            ctk.CTkLabel(
                files_grid, 
                text=estado_txt, 
                font=("Arial", 10, "bold"), 
                text_color=color_estado, 
                anchor="e"
            ).grid(row=row, column=4, sticky="ew", padx=col_configs[4]["padx"], pady=pady_fila+1)

            row += 1

    llistar_directori()
