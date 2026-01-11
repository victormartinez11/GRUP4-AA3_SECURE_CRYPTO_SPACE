import customtkinter as ctk
from tkinter import ttk
import os
import src.core.file_manager as fm 
import src.const.constants as const

def create_sidebar(parent, current_user, import_command, navigate_callback=None):

    sidebar = ctk.CTkFrame(parent, width=const.SIDEBAR_WIDTH, corner_radius=0, fg_color=const.COLOR_SIDEBAR)
    sidebar.grid(row=0, column=0, sticky="nsew")
    
    sidebar.grid_rowconfigure(1, weight=1) 
    sidebar.grid_columnconfigure(0, weight=1)

    title = ctk.CTkLabel(sidebar, text="MY VAULT", font=const.FONT_TITLE, text_color=const.COLOR_ACCENT)
    title.grid(row=0, column=0, pady=(30, 20))

    style = ttk.Style()
    style.theme_use("clam") 
    #Arbre de carpetes 
    style.configure("Treeview",
                    background=const.COLOR_SIDEBAR,
                    foreground="#e0e0e0",
                    fieldbackground=const.COLOR_SIDEBAR,
                    borderwidth=0,
                    rowheight=30,              
                    font=("Verdana", 10)) 
    style.map("Treeview", background=[('selected', const.COLOR_ACCENT)])
  
    tree_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    
    tree = ttk.Treeview(tree_frame, show="tree", selectmode="browse")
    tree.pack(fill="both", expand=True)

    # Funció auxiliar per a la lògica de l'arbre que llegeix el contingut de la carpeta i la mostra en l'arbre
    def omplir_node(node, ruta):
        if tree.get_children(node):
            tree.delete(*tree.get_children(node))
            
        try:
            items = os.listdir(ruta)
            items.sort() 
            
            for nom in items:
                if nom.startswith("."): 
                    continue
                ruta_completa = os.path.join(ruta, nom)
                if os.path.isdir(ruta_completa):
                    text_visual = f"{nom}" 
                    nou_node = tree.insert(node, "end", text=text_visual, values=[ruta_completa])
                    tree.insert(nou_node, "end", text="dummy")
        except Exception as e:
            print(f"Error llegint arbre: {e}")

    #Funció per a la lògica de l'arbre que s'executa quan s'expandeix un node
    def al_expandir(event):
        item = tree.focus()
        valors = tree.item(item, "values")
        if valors:
            omplir_node(item, valors[0])

    #Funció per a la lògica de l'arbre que s'executa quan s'expandeix un node
    def al_seleccionar(event):
        seleccionat = tree.selection()
        if seleccionat:
            item_id = seleccionat[0]
            valors = tree.item(item_id, "values")
            if valors:
                ruta_seleccionada = valors[0]
                if os.path.isdir(ruta_seleccionada):
                    if navigate_callback:
                        navigate_callback(ruta_seleccionada)

    tree.bind("<<TreeviewOpen>>", al_expandir)
    tree.bind("<<TreeviewSelect>>", al_seleccionar)

    ruta_vault = os.path.join("data", "vaults", current_user)
    os.makedirs(ruta_vault, exist_ok=True)

    root_node = tree.insert("", "end", text=f"  Vault: {current_user}", open=True, values=[ruta_vault])
    omplir_node(root_node, ruta_vault)

    #Funció per a la lògica de la creació d'una nova carpeta
    def accio_nova_carpeta():
        seleccionat = tree.selection()
        
        if seleccionat:
            item_id = seleccionat[0]
            ruta_pare = tree.item(item_id, "values")[0]
            nodo_a_refrescar = item_id
        else:
            ruta_pare = ruta_vault
            nodo_a_refrescar = root_node

        dialog = ctk.CTkInputDialog(text="Nom de la nova carpeta:", title="Crear Carpeta")
        nom_carpeta = dialog.get_input()

        if nom_carpeta:
            nova_ruta = os.path.join(ruta_pare, nom_carpeta)
            progress, msg = fm.create_directory(nova_ruta)
            if progress:
                print(msg)
                omplir_node(nodo_a_refrescar, ruta_pare)
                tree.item(nodo_a_refrescar, open=True) 
            else:
                print(msg)
    #Botó per a la creació d'una nova carpeta
    btn_new_folder = ctk.CTkButton(
        sidebar, 
        text="+ Nova Carpeta", 
        fg_color=const.COLOR_BTN_NEW_FOLDER, 
        hover_color=const.COLOR_BTN_NEW_FOLDER_HOVER,
        text_color="white",
        width=180,
        height=30,
        command=accio_nova_carpeta
    )
    btn_new_folder.grid(row=2, column=0, padx=10, pady=(10, 5))

    #Botó per a la importació d'un arxiu
    import_button = ctk.CTkButton(
        sidebar, 
        text="IMPORTAR ARXIU", 
        fg_color=const.COLOR_BTN_IMPORT,
        text_color="white",
        hover_color=const.COLOR_BTN_IMPORT_HOVER,
        width=180,
        height=35,
        command=import_command
    )
    import_button.grid(row=3, column=0, padx=10, pady=(5, 10))

    #Botó per a la tancada de la sessió
    exit_button = ctk.CTkButton(
        sidebar, 
        text="Cerrar Vault", 
        fg_color=const.COLOR_BTN_EXIT, 
        hover_color=const.COLOR_BTN_EXIT_HOVER,
        width=180, 
        height=35,
        command=parent.destroy
    )
    exit_button.grid(row=4, column=0, padx=10, pady=(0, 20))

    return sidebar
