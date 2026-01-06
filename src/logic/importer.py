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


def accio_exportar(ruta_seleccionada):
    # Validar que hem rebut una ruta i que es un fitxer encriptat
    if not ruta_seleccionada or not ruta_seleccionada.endswith(".enc"):
        return

    # Nom per defecte eliminant l'extensio .enc
    default_name = os.path.basename(ruta_seleccionada).replace(".enc", "")

    # Demanar on guardar el fitxer desencriptat
    ruta_desti = filedialog.asksaveasfilename(
        title="Exportar arxiu desencriptat",
        initialfile=default_name,
        defaultextension=".*"
    )

    if not ruta_desti:
        return
    # Demanar contrasenya per desencriptar
    dialog = ctk.CTkInputDialog(text="Introdueix la contrasenya:", title="Seguretat")
    password = dialog.get_input()

    if password:
        exito, msg = secure.decrypt_file(ruta_seleccionada, password)

        if exito:
            # El movem a la ruta de desti seleccionada per l'usuari
            decrypted_temp = ruta_seleccionada.replace(".enc", "")
            try:
                shutil.move(decrypted_temp, ruta_desti)
                messagebox.showinfo("Exportació Exitosa", f"Arxiu guardat a:\n{ruta_desti}")
            except Exception as e:
                messagebox.showerror("Error", f"Error movent el fitxer: {e}")
        else:
            messagebox.showerror("Error", msg)