import shutil 
from customtkinter import filedialog 
import os
import src.core.security as secure
import src.config.constants as const
from tkinter import messagebox
import customtkinter as ctk
import src.core.file_manager as fm

# Funció per importar fitxer
def accio_importar(session_password, current_username, destination_folder=None):
    try:
        origin = filedialog.askopenfilename(
                title="Import to vault",
                filetypes=(("All files", "*.*"), ("Text files", "*.txt"), ("Image files", "*.png;*.jpg"))
            )
        if origin:
            filename = os.path.basename(origin)
            
            # Si destination_folder està definit, l'usem. Si no, usem la arrel del vault.
            if destination_folder:
                vault_dir = destination_folder
            else:
                vault_dir = os.path.join("data", "vaults", current_username)
                
            os.makedirs(vault_dir, exist_ok=True)
    
            destination = os.path.join(vault_dir, filename + ".enc")

            exito, mensaje = secure.encrypt_file(origin, session_password, destination)
            if exito:
                fm.secure_delete(origin)
                print(f"File imported: {origin}")
                return True
            else:
                print(f"[ERROR IMPORTING]: {mensaje}")
                return False
    except Exception as e:
        print(f"[ERROR]: {e}")
        return False


def accio_exportar(ruta_seleccionada, session_password):
    # Validar que hem rebut una ruta i que es un fitxer encriptat
    if not ruta_seleccionada or not ruta_seleccionada.endswith(".enc"):
        messagebox.showwarning("Avís", "Selecciona un arxiu encriptat (.enc) per exportar.")
        return False

    # Nom per defecte eliminant l'extensio .enc
    default_name = os.path.basename(ruta_seleccionada).replace(".enc", "")

    # Demanar on guardar el fitxer desencriptat
    ruta_desti = filedialog.asksaveasfilename(
        title="Exportar arxiu desencriptat",
        initialfile=default_name,
        defaultextension=".*"
    )

    if not ruta_desti:
        return False

    # Ja no demanem contrasenya, usem la de la sessió
    if session_password:
        # Cridem a security.decrypt_file amb output_path
        exito, msg = secure.decrypt_file(ruta_seleccionada, session_password, output_path=ruta_desti)

        if exito:
            # Si s'ha exportat bé, eliminem l'original de forma segura
            fm.secure_delete(ruta_seleccionada)
            messagebox.showinfo("Exportació Exitosa", f"Arxiu exportat i esborrat del vault:\n{ruta_desti}")
            return True
        else:
            messagebox.showerror("Error", msg)
            return False
    return False