import customtkinter as ctk

def create_sidebar(parent, color_sidebar):
    barra_lateral = ctk.CTkFrame(parent, width=200, corner_radius=0, fg_color=color_sidebar)
    barra_lateral.grid(row=0, column=0, sticky="nsew")

    titol_lateral = ctk.CTkLabel(barra_lateral, text="Accessos ràpids", font=("Arial", 16, "bold"), text_color="white")
    titol_lateral.pack(pady=20)

    for item in ["Escriptori", "Descargues", "Documents", "Imatges"]:
        colors_botons = ctk.CTkButton(barra_lateral, text=item, fg_color="transparent", text_color="white", hover_color="grey", anchor="w")
        colors_botons.pack(fill="x", padx=10, pady=2)
    
    return barra_lateral
