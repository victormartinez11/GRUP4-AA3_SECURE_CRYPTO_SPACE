import shutil #Copi file
from customtkinter import filedialog # Windows selector
import os

def accio_importar():
    try:
        #Open windows explorer
        origin= filedialog.askopenfilename(
                title="Import to vault",
                filetypes=(("All files", "*.*"), ("Text files", "*.txt"), ("Image files", "*.png;*.jpg"))
            )
        if origin:
            #Copy file
            destination = os.getcwd()
            shutil.copy(origin, destination)
            print(f"File imported: {origin}")
        else:
            raise Exception("No file selected")
    except Exception as e:
        print(f"[ERROR]: {e}")
      

