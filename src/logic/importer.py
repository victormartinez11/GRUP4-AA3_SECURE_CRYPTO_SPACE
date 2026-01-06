import shutil 
from customtkinter import filedialog 
import os
import src.core.security as secure
import src.config.constants as const

# Funció per importar fitxer
def accio_importar(session_password, current_username):
    try:
        origin = filedialog.askopenfilename(
                title="Import to vault",
                filetypes=(("All files", "*.*"), ("Text files", "*.txt"), ("Image files", "*.png;*.jpg"))
            )
        if origin:
            filename = os.path.basename(origin)
            vault_dir = os.path.join("data", "vaults", current_username)
            os.makedirs(vault_dir, exist_ok=True)
    
            destination = os.path.join(vault_dir, filename + ".enc")

            exito, mensaje = secure.encrypt_file(origin, session_password, destination)
            if exito:
                print(f"File imported: {origin}")
                return True
            else:
                print(f"[ERROR IMPORTING]: {mensaje}")
                return False
    except Exception as e:
        print(f"[ERROR]: {e}")
        return False
