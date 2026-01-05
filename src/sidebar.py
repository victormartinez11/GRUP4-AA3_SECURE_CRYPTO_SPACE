import customtkinter as ctk
from tkinter import ttk
import os

def create_sidebar(parent, color_sidebar, current_user, import_command, navigate_callback=None):

    sidebar = ctk.CTkFrame(parent, width=250, corner_radius=0, fg_color=color_sidebar)
    sidebar.grid(row=0, column=0, sticky="nsew")
    
    sidebar.grid_rowconfigure(1, weight=1) 
    sidebar.grid_columnconfigure(0, weight=1)

    title = ctk.CTkLabel(sidebar, text="MY VAULT", font=("Verdana", 20, "bold"), text_color="#5c55e6")
    title.grid(row=0, column=0, pady=(30, 20))

    style = ttk.Style()
    style.theme_use("clam") 
    style.configure("Treeview",
                    background=color_sidebar,
                    foreground="#e0e0e0",
                    fieldbackground=color_sidebar,
                    borderwidth=0,
                    rowheight=30,              
                    font=("Verdana", 10)) 
    style.map("Treeview", background=[('selected', '#5c55e6')])
  
    tree_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    
    tree = ttk.Treeview(tree_frame, show="tree", selectmode="browse")
    tree.pack(fill="both", expand=True)

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

    def al_expandir(event):
        item = tree.focus()
        valors = tree.item(item, "values")
        if valors:
            omplir_node(item, valors[0])

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

    def accio_nova_carpeta():
        seleccionat = tree.selection()
        
        if seleccionat:
            item_id = seleccionat[0]
            ruta_pare = tree.item(item_id, "values")[0]
            nodo_a_refrescar = item_id
        else:
            ruta_pare = ruta_vault
            nodo_a_refrescar = root_node

        # Pedir nombre
        dialog = ctk.CTkInputDialog(text="Nom de la nova carpeta:", title="Crear Carpeta")
        nom_carpeta = dialog.get_input()

        if nom_carpeta:
            nova_ruta = os.path.join(ruta_pare, nom_carpeta)
            try:
                # Crear en disco
                os.makedirs(nova_ruta, exist_ok=True)
                print(f"Carpeta creada: {nova_ruta}")
                
                # Refrescar el arbre visualment
                omplir_node(nodo_a_refrescar, ruta_pare)
                tree.item(nodo_a_refrescar, open=True) 
                
            except Exception as e:
                print(f"Error creant carpeta: {e}")

    # Botó NOVA CARPETA
    btn_new_folder = ctk.CTkButton(
        sidebar, 
        text="+ Nova Carpeta", 
        fg_color="#27ae60", 
        hover_color="#2ecc71",
        text_color="white",
        width=180,
        height=30,
        command=accio_nova_carpeta
    )
    btn_new_folder.grid(row=2, column=0, padx=10, pady=(10, 5))

    # Botón IMPORTAR
    import_button = ctk.CTkButton(
        sidebar, 
        text="IMPORTAR ARXIU", 
        fg_color="#3498db",
        text_color="white",
        hover_color="#2980b9",
        width=180,
        height=35,
        command=import_command
    )
    import_button.grid(row=3, column=0, padx=10, pady=(5, 10))

    # Botón SALIR
    exit_button = ctk.CTkButton(
        sidebar, 
        text="Cerrar Vault", 
        fg_color="#c0392b", 
        hover_color="#e74c3c",
        width=180, 
        height=35,
        command=parent.destroy
    )
    exit_button.grid(row=4, column=0, padx=10, pady=(0, 20))

    return sidebar