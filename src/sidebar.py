import customtkinter as ctk
from tkinter import ttk
import os
from src import importfile
def create_sidebar(parent, color_sidebar, import_command):
    sidebar = ctk.CTkFrame(parent, width=200, corner_radius=0, fg_color=color_sidebar)
    sidebar.grid(row=0, column=0, sticky="nsew")

    title = ctk.CTkLabel(sidebar, text="Accessos ràpids", font=("Arial", 16, "bold"), text_color="white")
    title.pack(pady=20)
def create_sidebar(parent, color_sidebar):
    # marc lateral
    barra_lateral = ctk.CTkFrame(parent, width=250, corner_radius=0, fg_color=color_sidebar)
    barra_lateral.grid(row=0, column=0, sticky="nsew")
    
    # Configurem que la fila 1 s'expandeixi
    barra_lateral.grid_rowconfigure(1, weight=1) 
    barra_lateral.grid_columnconfigure(0, weight=1)

    # Quick Access Buttons
    for item in ["Escriptori", "Descargues", "Documents", "Imatges"]:
        color_button = ctk.CTkButton(sidebar, text=item, fg_color="transparent", text_color="white", hover_color="grey", anchor="w")
        color_button.pack(fill="x", padx=10, pady=2)
    # Títol amb estil
    titol = ctk.CTkLabel(barra_lateral, text="MY VAULT", font=("Verdana", 20, "bold"), text_color="#5c55e6")
    titol.grid(row=0, column=0, pady=(30, 20))

    style = ttk.Style()
    style.theme_use("clam") 
    
    style.configure("Treeview",
                    background=color_sidebar,
                    foreground="#e0e0e0",      # Blanc
                    fieldbackground=color_sidebar,
                    borderwidth=0,
                    rowheight=30,              
                    font=("Verdana", 10)) 
    
    # Color quan selecciones
    style.map("Treeview", background=[('selected', '#5c55e6')])
  
    # marc petit per contenir l'arbre
    tree_frame = ctk.CTkFrame(barra_lateral, fg_color="transparent")
    tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    
    tree = ttk.Treeview(tree_frame, show="tree", selectmode="browse")
    tree.pack(fill="both", expand=True)

 
    def omplir_node(node, ruta):
        if tree.get_children(node):
            tree.delete(*tree.get_children(node))
            
        try:
            items = os.listdir(ruta)
            for nom in items:
                ruta_completa = os.path.join(ruta, nom)
                if os.path.isdir(ruta_completa):
                   
                    text_visual = f"📁  {nom}" 
                    
                    nou_node = tree.insert(node, "end", text=text_visual, values=[ruta_completa])
                    tree.insert(nou_node, "end", text="dummy")
        except:
            pass 


    def al_expandir(event):
        item = tree.focus()
        valors = tree.item(item, "values")
        if valors:
            omplir_node(item, valors[0])

    def al_seleccionar(event):
        seleccionat = tree.selection()
        if seleccionat:
            ruta = tree.item(seleccionat[0], "values")[0]
            print(f"RUTA SELECCIONADA: {ruta}")

    tree.bind("<<TreeviewOpen>>", al_expandir)
    tree.bind("<<TreeviewSelect>>", al_seleccionar)

    ruta_inici = os.path.expanduser("~")

    root = tree.insert("", "end", text="  Inici", open=True, values=[ruta_inici])
    omplir_node(root, ruta_inici)

    # Botó Sortir                                                           #gris fluix              #vermell                                #vermell
    btn_sortir = ctk.CTkButton(barra_lateral, text="Tancar Sessió", fg_color="#2c3e50", hover_color="#c0392b", border_width=1, border_color="#c0392b", command=parent.destroy)
    btn_sortir.grid(row=2, column=0, pady=20, padx=20, )
    return barra_lateral

    # Botton Sortir
    exit_button = ctk.CTkButton(sidebar, text="Cerrar Vault", fg_color="#c0392b", command=parent.destroy, width=180, height=35)
    exit_button.pack(side="bottom", pady=20, padx=10)

    # Import botton
    import_button = ctk.CTkButton(
        sidebar, 
        text="IMPORTAR", 
        fg_color="#3498db",
        text_color="white",
        hover_color="#2980b9",
        width=180,
        height=35,
        command=import_command
    )
    import_button.pack(side="bottom", padx=10, pady=10)

    return sidebar
