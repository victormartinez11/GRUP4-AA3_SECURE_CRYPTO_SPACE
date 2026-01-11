import os
import customtkinter as ctk
from tkinter import messagebox, filedialog
import src.core.file_manager as fm
import src.core.security as secure
import src.logic.importer as importer
import src.const.constants as const
from PIL import Image

# Aquesta funció carrega les imatges per a les icones
try:
    IMG_FOLDER = ctk.CTkImage(light_image=Image.open("assets/folder.png"), dark_image=Image.open("assets/folder.png"), size=(50, 50))
    IMG_FILE = ctk.CTkImage(light_image=Image.open("assets/file.png"), dark_image=Image.open("assets/file.png"), size=(50, 50))
    IMG_LOCK   = ctk.CTkImage(light_image=Image.open("assets/candado.png"), dark_image=Image.open("assets/candado.png"), size=(50, 50))
except Exception:
    IMG_FOLDER = None
    IMG_FILE = None
    IMG_LOCK = None

# Aquesta funció selecciona un arxiu i activa els botons
def select_file_action(name, current_path, app_state, label, btn_enc, btn_dec, btn_del):
    full_path = os.path.join(current_path, name)
    app_state["selected_file"] = full_path
    
    label.configure(text=f"Seleccionado: {name}", text_color="white")
    btn_del.configure(state="normal") 

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

# Aquesta funció mostra la llista d'arxius a la pantalla
def update_listing_view(container_frame, path, app_state, status_label, btn_encrypt, btn_decrypt, btn_delete, search_text, navigate_callback=None):
    for widget in container_frame.winfo_children():
        widget.destroy()
    
    items = fm.list_directory(path)

    if search_text:
        filtered_items = []
        for f in items:
            if search_text.lower() in f.lower():
                filtered_items.append(f)
        
        items = filtered_items

    # Configuració de columnes
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
        if es_carpeta:
            size_str = "-"
        else:
            size_str = f"{info['size'] / 1024:.1f} KB"
        
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
        
        if img:
            txt_icon = ""
        else:
            txt_icon = fallback   
        
        pady_row = 2

        # Etiqueta per a la icona (carpeta, arxiu o cadenat)
        icon_label = ctk.CTkLabel(container_frame, text=txt_icon, image=img, width=30, anchor="center")
        icon_label.grid(row=row, column=0, sticky="ew", padx=5, pady=pady_row)
        
        # Callback per quan fem clic
        def cmd(n=name, p=path):
            select_file_action(n, p, app_state, status_label, btn_encrypt, btn_decrypt, btn_delete)
        

        # Etiqueta per al nom de l'arxiu, funciona com a botó per seleccionar-lo
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
        
        # Lògica Doble Clic
        if es_carpeta and navigate_callback:
            def on_double_click(event, p=full_path):
                if os.path.isdir(p):
                    navigate_callback(p)
            
            btn_name.bind("<Double-Button-1>", on_double_click)
            icon_label.bind("<Double-Button-1>", on_double_click)
        
        # Etiqueta per a la data
        ctk.CTkLabel(container_frame, text=date_str, font=const.FONT_NORMAL, text_color=const.COLOR_TEXT_DIM, anchor="w").grid(row=row, column=2, sticky="ew", padx=5, pady=pady_row)
        
        # Etiqueta per al mida
        ctk.CTkLabel(container_frame, text=size_str, font=const.FONT_NORMAL, text_color=const.COLOR_TEXT_DIM, anchor="e").grid(row=row, column=3, sticky="ew", padx=5, pady=pady_row)
        
        # Etiqueta per al estat
        ctk.CTkLabel(container_frame, text=status_txt, font=const.FONT_SMALL_BOLD, text_color=status_col, anchor="e").grid(row=row, column=4, sticky="ew", padx=(5,10), pady=pady_row+1)

        row += 1

# Aquesta funció encripta l'arxiu seleccionat
def execute_encrypt(app_state, label, encrypt_btn, decrypt_btn, session_password, refresh_callback):
    target = app_state["selected_file"]
    if not target: 
        label.configure(text="Ningún archivo seleccionado", text_color="gray")
        return

    if session_password:
        success, msg = secure.encrypt_file(target, session_password)
        if success:
            # Esborrem de forma segura després d'encriptar
            fm.secure_delete(target)   
            refresh_callback()
            label.configure(text="Arxiu encriptat i original eliminat", text_color=const.COLOR_GREEN)
            encrypt_btn.configure(state="disabled")
            decrypt_btn.configure(state="disabled")
        else:
            label.configure(text=f"Error: {msg}", text_color=const.COLOR_RED)

# Aquesta funció esborra l'arxiu seleccionat de forma segura
def execute_delete(app_state, label, btn_enc, btn_dec, btn_del, refresh_callback):
    target = app_state["selected_file"]
    if not target: 
        messagebox.showerror("Error", "No s'ha seleccionat cap arxiu.")
        return
    
    confirmacio = messagebox.askyesno(
        "Esborrat Segur", 
        "ATENCIÓ: Aquesta acció sobrescriurà l'arxiu i no es podrà recuperar.\nVols continuar?")
    
    if confirmacio:
        exito, missatge = fm.secure_delete(target)
        
        if exito:
            refresh_callback()
            label.configure(text=missatge, text_color="green")
            btn_enc.configure(state="disabled")
            btn_dec.configure(state="disabled")
            btn_del.configure(state="disabled")
        else:
            messagebox.showerror("Error", missatge)

# Aquesta funció exporta i desencripta l'arxiu seleccionat
def execute_export(app_state, session_password, refresh_callback, label, btn_dec, btn_del):
    objectiu = app_state["selected_file"]
    if not objectiu:
        messagebox.showerror("Error", "No s'ha seleccionat cap arxiu.")
        return
    
    # Deleguem el mòdul importer, passant la contrasenya de sessió
    if importer.accio_exportar(objectiu, session_password):
        refresh_callback()
        label.configure(text="Ningún archivo seleccionado", text_color="gray")
        btn_dec.configure(state="disabled")
        btn_del.configure(state="disabled")

# Aquesta funció importa un nou arxiu al vault
def execute_import(current_path, session_password, current_user, refresh_callback):
    if importer.accio_importar(session_password, current_user, destination_folder=current_path):
        refresh_callback()
