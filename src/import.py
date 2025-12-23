import shutil #Copi file
from customtkinter import filedialog # Windows selector
import os

def accio_importar():
    try:
        origin= filedialog.askopenfilename(
                title="Import to vault",
                filetypes=(("All files", "*.*"), ("Text files", "*.txt"), ("Image files", "*.png;*.jpg"))
            )
        if not origin:
            return
        destination = os.getcwd()
        shutil.copy(origin, destination)
        print(f"File imported: {origin}")
    except Exception as e:
        print(f"[ERROR]: {e}")
      