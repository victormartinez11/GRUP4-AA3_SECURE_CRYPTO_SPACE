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
import src.ui.dashboard_actions as actions
# Aquesta funció crea la pantalla del dashboard
def dashboard(app, current_user, session_password):
    app_state = {"selected_file": None}
    search_var = ctk.StringVar()

    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)
    #S'hagafa la ruta del vault del usuari actual i es crea si no existeix si l'usuario no selecciona un vault
    ruta_vault = os.path.join("data", "vaults", current_user)
    fm.create_directory(ruta_vault)
    current_path_state = [ruta_vault]

    # Aquesta funció actualitza la llista d'arxius
    def refresh_views():
        actions.update_listing_view(
            files_grid, 
            current_path_state[0], 
            app_state, 
            label_arxiu_seleccionat, 
            botons_xifrar, 
            botons_desxifrar, 
            botons_esborrar, 
            search_var.get(), 
            navigate_to
        )

    # Aquesta funció filtra els arxius quan escrivim al cercador
    def on_search_change(*args):
        refresh_views()
    search_var.trace("w", on_search_change)

    # Aquesta funció canvia de carpeta
    def navigate_to(path):
        current_path_state[0] = path
        cami_directori.configure(text=f" {path}")
        search_var.set("") # Netejar cerca en canviar de carpeta
        refresh_views() 
    # Funcions per pasar variables a les accions del boto (import, encriptar, desencriptar, esborrar) 
    # Aquesta funció importa un arxiu
    def import_func():
        actions.execute_import(current_path_state[0], session_password, current_user, refresh_views)
    
    # Aquesta funció encripta l'arxiu seleccionat
    def handle_encrypt_click():
         actions.execute_encrypt(app_state, label_arxiu_seleccionat, botons_xifrar, botons_desxifrar, session_password, refresh_views)

    # Aquesta funció esborra l'arxiu seleccionat
    def handle_delete_click():
        actions.execute_delete(app_state, label_arxiu_seleccionat, botons_xifrar, botons_desxifrar, botons_esborrar, refresh_views)

    # Aquesta funció exporta l'arxiu seleccionat
    def accio_exportar():
        actions.execute_export(app_state, session_password, refresh_views, label_arxiu_seleccionat, botons_desxifrar, botons_esborrar)

    # Creacio de la barra lateral
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
    #Boto Exportar
    botons_desxifrar = ctk.CTkButton(
        action_bar, 
        text="EXPORTAR", 
        fg_color="#e67e22", 
        hover_color="#d35400",
        state="disabled", 
        text_color="white",
        width=120, 
        command=accio_exportar 
    )
    botons_desxifrar.pack(side="right", padx=(10, 20), pady=10)
    #Boto Encriptar
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
