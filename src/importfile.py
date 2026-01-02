import shutil #Copiar fitxer
from customtkinter import filedialog # Selector de fitxer 
import os

#Funcio per importar fitxer
def accio_importar():
    try:
        #Obrir explorador de fitxers
        origin= filedialog.askopenfilename(
                title="Import to vault",
                filetypes=(("All files", "*.*"), ("Text files", "*.txt"), ("Image files", "*.png;*.jpg"))
            )
        if origin:
            #Copiar fitxer
            destination = os.getcwd()
            shutil.copy(origin, destination)
            print(f"File imported: {origin}")
        else:
            raise Exception("No file selected")
    except Exception as e:
        print(f"[ERROR]: {e}")
      

