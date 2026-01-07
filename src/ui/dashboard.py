import customtkinter as ctk
import os
from PIL import Image   
from src.ui.sidebar import create_sidebar
from src.core.security import encrypt_file, decrypt_file
import datetime
import src.logic.importer as importer
import src.core.file_manager as fm
import src.config.constants as const
from functools import partial
from tkinter import messagebox, filedialog

try:
    IMG_FOLDER = ctk.CTkImage(light_image=Image.open("assets/folder.png"), dark_image=Image.open("assets/folder.png"), size=(50, 50))
    IMG_FILE = ctk.CTkImage(light_image=Image.open("assets/file.png"), dark_image=Image.open("assets/file.png"), size=(50, 50))
    IMG_LOCK   = ctk.CTkImage(light_image=Image.open("assets/candado.png"), dark_image=Image.open("assets/candado.png"), size=(50, 50))
except Exception:
    IMG_FOLDER = None
    IMG_FILE = None
    IMG_LOCK = None

def dashboard(app, current_user, session_password):
    
    app_state = {"selected_file": None}
    
    search_var = ctk.StringVar()

    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    ruta_vault = os.path.join("data", "vaults", current_user)
    fm.create_directory(ruta_vault)
    current_path_state = [ruta_vault]

    def select_file_action(name, current_path, label, btn_enc, btn_dec, btn_del):
        full_path = os.path.join(current_path, name)
        app_state["selected_file"] = full_path
        
        label.configure(text=f"Seleccionado: {name}", text_color="white")
        
        btn_del.configure(state="normal") # Sempre actiu si hi ha selecció

        if fm.is_directory(full_path):
            btn_enc.configure(state="disabled")
            btn_dec.configure(state="disabled")
            return

        if name.endswith(".enc"):
            btn_enc.configure(state="disabled")
            btn_dec.configure(state="normal")
        else:
            btn_enc.configure(state="normal")
            btn_dec.configure(state="disabled")

    def create_row_callback(name, path, label, btn_enc, btn_dec, btn_del):
        def callback():
            select_file_action(name, path, label, btn_enc, btn_dec, btn_del)
        return callback

    def update_listing_view(container_frame, path, status_label, btn_encrypt, btn_decrypt, btn_delete, navigate_callback=None):
        for widget in container_frame.winfo_children():
            widget.destroy()
        
        items = fm.list_directory(path)

        text_cerca = search_var.get().lower()
        if text_cerca:
            items = [f for f in items if text_cerca in f.lower()]

        container_frame.grid_columnconfigure(0, weight=0, minsize=40) 
        container_frame.grid_columnconfigure(1, weight=2, minsize=70) 
        container_frame.grid_columnconfigure(2, weight=1, minsize=120) 
        container_frame.grid_columnconfigure(3, weight=0, minsize=80) 
        container_frame.grid_columnconfigure(4, weight=0, minsize=100) 

        headers = ["", "NOMBRE", "FECHA", "TAMAÑO", "ESTADO"] 
        col_configs = [
            {"anchor": "center", "justify": "center", "padx": 5},
            {"anchor": "w",      "justify": "left",   "padx": 5}, 
            {"anchor": "w",      "justify": "left",   "padx": 5}, 
            {"anchor": "e",      "justify": "right",  "padx": 5}, 
            {"anchor": "e",      "justify": "right",  "padx": (5, 10)}
        ]
        
        for i, h in enumerate(headers):
            ctk.CTkLabel(
                container_frame, 
                text=h, 
                font=const.FONT_HEADER, 
                text_color=const.COLOR_ACCENT,
                anchor=col_configs[i]["anchor"]
            ).grid(row=0, column=i, sticky="ew", padx=col_configs[i]["padx"], pady=(5, 10))
        
        row = 1
        for name in items:
            if name.startswith("."): 
                continue 
            
            full_path = os.path.join(path, name)
            info = fm.get_file_info(full_path)
            if not info["exists"]:
                continue

            es_carpeta = info["is_dir"]
            es_encriptado = name.endswith(".enc")
            
            date_str = info["date_str"]
            size_str = "-" if es_carpeta else f"{info['size'] / 1024:.1f} KB"
            
            if es_carpeta:
                img = IMG_FOLDER
                fallback = "DIR"
                status_txt = ""
                status_col = "white"
            elif es_encriptado:
                img = IMG_LOCK
                fallback = "LOCK"
                status_txt = "ENCRIPTADO"
                status_col = const.COLOR_ENCRYPTED
            else:
                img = IMG_FILE
                fallback = "FILE"
                status_txt = "VISIBLE"
                status_col = const.COLOR_VISIBLE
            
            txt_icon = "" if img else fallback
            
            pady_row = 2

            icon_label = ctk.CTkLabel(container_frame, text=txt_icon, image=img, width=30, anchor="center")
            icon_label.grid(row=row, column=0, sticky="ew", padx=5, pady=pady_row)
            
            cmd = create_row_callback(name, path, status_label, btn_encrypt, btn_decrypt, btn_delete)
            
            btn_name = ctk.CTkButton(
                container_frame,
                text=name,
                font=const.FONT_NORMAL,
                fg_color="transparent",
                text_color="white", 
                hover_color=const.COLOR_BTN_HOVER_LIST,
                anchor="w", 
                height=24,  
                command=cmd
            )
            btn_name.grid(row=row, column=1, sticky="ew", padx=5, pady=pady_row)
            
            # --- Lògica Doble Clic (GRUP4-59) ---
            if es_carpeta and navigate_callback:
                def on_double_click(event, p=full_path):
                    if os.path.isdir(p):
                        navigate_callback(p)
                
                # Vinculem doble clic esquerre al botó i a la icona
                btn_name.bind("<Double-Button-1>", on_double_click)
                icon_label.bind("<Double-Button-1>", on_double_click)
            
            ctk.CTkLabel(container_frame, text=date_str, font=const.FONT_NORMAL, text_color=const.COLOR_TEXT_DIM, anchor="w").grid(row=row, column=2, sticky="ew", padx=5, pady=pady_row)
            
            ctk.CTkLabel(container_frame, text=size_str, font=const.FONT_NORMAL, text_color=const.COLOR_TEXT_DIM, anchor="e").grid(row=row, column=3, sticky="ew", padx=5, pady=pady_row)
            
            ctk.CTkLabel(container_frame, text=status_txt, font=const.FONT_SMALL_BOLD, text_color=status_col, anchor="e").grid(row=row, column=4, sticky="ew", padx=(5,10), pady=pady_row+1)

            row += 1

    def refresh_views():
        update_listing_view(files_grid, current_path_state[0], label_arxiu_seleccionat, botons_xifrar, botons_desxifrar, botons_esborrar, navigate_to)


    def on_search_change(*args):
        refresh_views()
    search_var.trace("w", on_search_change)

    def navigate_to(path):
        current_path_state[0] = path
        cami_directori.configure(text=f" {path}")
        search_var.set("") # Netejar cerca en canviar de carpeta
        refresh_views() 

    def import_func():
        # Passem la ruta actual del navegador com a carpeta de desti
        current_dir = current_path_state[0]
        if importer.accio_importar(session_password, current_user, destination_folder=current_dir):
            refresh_views()
    
    def handle_encrypt_click():
         execute_encrypt(label_arxiu_seleccionat, botons_xifrar, botons_desxifrar)

    def handle_decrypt_click():
         execute_decrypt(label_arxiu_seleccionat, botons_xifrar, botons_desxifrar)

    def handle_delete_click():
        target = app_state["selected_file"]
        if not target: return
        
        confirmacio = messagebox.askyesno(
            "Esborrat Segur", 
            "ATENCIÓ: Aquesta acció sobrescriurà l'arxiu i no es podrà recuperar.\nVols continuar?"
        )
        
        if confirmacio:
            exito, missatge = fm.secure_delete(target)
            
            if exito:
                refresh_views()
                label_arxiu_seleccionat.configure(text=missatge, text_color="green")
                botons_xifrar.configure(state="disabled")
                botons_desxifrar.configure(state="disabled")
                botons_esborrar.configure(state="disabled")
            else:
                messagebox.showerror("Error", missatge)

    def execute_encrypt(label, encrypt_btn, decrypt_btn):
        target = app_state["selected_file"]
        if not target: return

        dialog = ctk.CTkInputDialog(text="Introduce la contraseña para encriptar:", title="Encriptar")
        passwd = dialog.get_input()
        if passwd:
            success, msg = encrypt_file(target, passwd)
            if success:
                refresh_views()
                label.configure(text="S'ha encriptat l'arxiu", text_color=const.COLOR_GREEN)
                encrypt_btn.configure(state="disabled")
                decrypt_btn.configure(state="disabled")
            else:
                label.configure(text=f"Error: {msg}", text_color=const.COLOR_RED)

    # Funcio per exportar arxiu desencriptat a una ruta especifica
    def accio_exportar():
        objectiu = app_state["selected_file"]
        
        # Verificacio inicial: ha de ser un fitxer .enc
        if not objectiu or not objectiu.endswith(".enc"):
            messagebox.showwarning("Avís", "Selecciona un arxiu encriptat (.enc) per exportar.")
            return

        # Nom per defecte sense la extensio .enc
        nom_inicial = os.path.basename(objectiu).replace(".enc", "")

        # Demanar ruta de desti
        ruta_desti = filedialog.asksaveasfilename(
            title="Exportar arxiu desencriptat",
            initialfile=nom_inicial,
            defaultextension=".*"
        )
        
        if not ruta_desti:
            return

        # Demanar contrasenya
        dialeg = ctk.CTkInputDialog(text="Introdueix la contrasenya per desencriptar:", title="Seguretat")
        password = dialeg.get_input()

        if password:
            # Cridem a security.decrypt_file amb output_path
            exito, missatge = decrypt_file(objectiu, password, output_path=ruta_desti)
            
            if exito:
                messagebox.showinfo("Exportat", f"Arxiu exportat correctament a:\n{ruta_desti}")
            else:
                messagebox.showerror("Error", f"No s'ha pogut exportar: {missatge}")

    create_sidebar(app, current_user, import_command=import_func, navigate_callback=navigate_to)
        
    area_principal = ctk.CTkFrame(app, fg_color=const.COLOR_BG, corner_radius=0)
    area_principal.grid(row=0, column=1, sticky="nsew")

    path_container = ctk.CTkFrame(area_principal, fg_color="transparent")
    path_container.pack(fill="x", padx=20, pady=(20, 10))
    
    ctk.CTkLabel(path_container, text="Ruta:", text_color=const.COLOR_ACCENT, font=const.FONT_PATH_BOLD).pack(side="left")
    cami_directori = ctk.CTkLabel(path_container, text=f" {ruta_vault}", text_color=const.COLOR_TEXT_SECONDARY, font=const.FONT_PATH)
    cami_directori.pack(side="left")

   # barra per poder filtrar els fitxers per noms
    search_entry = ctk.CTkEntry(
        path_container, 
        placeholder_text="Buscar fitxer...", 
        textvariable=search_var, 
        width=200,
        fg_color="#212533",
        text_color="white",
        border_color=const.COLOR_ACCENT)
    search_entry.pack(side="right", padx=10)

    action_bar = ctk.CTkFrame(area_principal, fg_color=const.COLOR_SIDEBAR, corner_radius=15, height=50)
    action_bar.pack(fill="x", padx=20, pady=10)
    
    label_arxiu_seleccionat = ctk.CTkLabel(action_bar, text="Ningún archivo seleccionado", text_color="gray", font=const.FONT_NORMAL)
    label_arxiu_seleccionat.pack(side="left", padx=20, pady=15)

    botons_desxifrar = ctk.CTkButton(
        action_bar, 
        text="EXPORTAR", 
        fg_color="#e67e22", # Color Taronja
        hover_color="#d35400",
        state="disabled", 
        text_color="white",
        width=120, 
        command=accio_exportar 
    )
    botons_desxifrar.pack(side="right", padx=(10, 20), pady=10)

    botons_xifrar = ctk.CTkButton(
        action_bar, 
        text="ENCRIPTAR", 
        fg_color=const.COLOR_BTN_ENCRYPT, 
        hover_color=const.COLOR_BTN_ENCRYPT_HOVER,
        state="disabled", 
        text_color="gray",
        width=120, 
        command=handle_encrypt_click 
    )
    botons_xifrar.pack(side="right", padx=0, pady=10)

    # Botó Esborrar 
    botons_esborrar = ctk.CTkButton(
        action_bar, 
        text="ELIMINAR", 
        fg_color=const.COLOR_BTN_EXIT,
        hover_color=const.COLOR_BTN_EXIT_HOVER,
        state="disabled", 
        text_color="white",
        width=120, 
        command=handle_delete_click 
    )
    botons_esborrar.pack(side="right", padx=10, pady=10)

    files_grid = ctk.CTkScrollableFrame(area_principal, fg_color="transparent")
    files_grid.pack(fill="both", expand=True, padx=20, pady=10)

    refresh_views()
