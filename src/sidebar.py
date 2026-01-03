import customtkinter as ctk
from src import importfile
def create_sidebar(parent, color_sidebar, import_command):
    sidebar = ctk.CTkFrame(parent, width=200, corner_radius=0, fg_color=color_sidebar)
    sidebar.grid(row=0, column=0, sticky="nsew")

    title = ctk.CTkLabel(sidebar, text="Accessos ràpids", font=("Arial", 16, "bold"), text_color="white")
    title.pack(pady=20)

    # Quick Access Buttons
    for item in ["Escriptori", "Descargues", "Documents", "Imatges"]:
        color_button = ctk.CTkButton(sidebar, text=item, fg_color="transparent", text_color="white", hover_color="grey", anchor="w")
        color_button.pack(fill="x", padx=10, pady=2)

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
