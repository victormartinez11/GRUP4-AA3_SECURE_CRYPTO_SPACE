import os
from src.file_encript import encrypt_file

def encrypt_folder(folder_path, password):
    print(f"Procesando carpeta: {folder_path}...")
    archivos_procesados = 0
    errores = 0
    # os.walk permite entrar en subcarpetas automáticamente
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            
           
            if file_name.endswith(".enc") or file_name == "vault.key" or file_name == "file_salt.key" or file_name == "file_key.key":
                continue
            full_path = os.path.join(root, file_name)
            # Llamamos a tu función de encriptar 
            exito, mensaje = encrypt_file(full_path, password)
            if exito == True:
                archivos_procesados += 1
            else:
                errores += 1
                print(f"Error en {file_name}: {mensaje}")

    return (f"Proceso terminado. Encriptados: {archivos_procesados}. Errores: {errores}")
