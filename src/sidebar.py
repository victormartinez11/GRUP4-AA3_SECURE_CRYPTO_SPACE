import customtkinter as ctk
from tkinter import ttk
import os

def create_sidebar(parent, color_sidebar):

    barra_lateral = ctk.CTkFrame(parent, width=200, corner_radius=0, fg_color=color_sidebar)
    barra_lateral.grid(row=0, column=0, sticky="nsew")

    # Títol
    titol = ctk.CTkLabel(barra_lateral, text="Arxius", font=("Arial", 16, "bold"), text_color="white")
    titol.pack(pady=20)

    # Configuració colors 
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background=color_sidebar, foreground="white", fieldbackground=color_sidebar, borderwidth=0)

    # Creació Treeview
    tree = ttk.Treeview(barra_lateral, show="tree", selectmode="browse")
    tree.pack(fill="both", expand=True, padx=10, pady=5)


    def omplir_node(node, ruta):
        # Esborrem el que hi hagi dins per no duplicar
        if tree.get_children(node):
            tree.delete(*tree.get_children(node))
            
        try:
            # Busquem només carpetes
            for nom in os.listdir(ruta):
                ruta_completa = os.path.join(ruta, nom)
                if os.path.isdir(ruta_completa):
                    # 'values' guarda la ruta invisible per utilitzarla després
                    nou_node = tree.insert(node, "end", text=nom, values=[ruta_completa])
                    tree.insert(nou_node, "end", text="dummy")
        except:
            pass # Si no tenim permís ignorem


    
    def al_expandir(event):
        item = tree.focus()
        ruta = tree.item(item, "values")[0]
        omplir_node(item, ruta)

    # Quan fas clic al nom
    def al_seleccionar(event):
        seleccionat = tree.selection()
        if seleccionat:
            ruta = tree.item(seleccionat[0], "values")[0]
            print(f"RUTA SELECCIONADA: {ruta}")

    tree.bind("<<TreeviewOpen>>", al_expandir)
    tree.bind("<<TreeviewSelect>>", al_seleccionar)

    ruta_inici = os.path.expanduser("~") 
    root = tree.insert("", "end", text="Inici", open=True, values=[ruta_inici])
    omplir_node(root, ruta_inici)

    # Botó de tancar 
    btn_sortir = ctk.CTkButton(barra_lateral, text="Cerrar Vault", fg_color="#c0392b", command=parent.destroy)
    btn_sortir.pack(side="bottom", pady=20, padx=10)

    return barra_lateral