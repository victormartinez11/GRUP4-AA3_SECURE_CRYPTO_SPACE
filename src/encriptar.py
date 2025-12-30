import os
from src.file_encript import encrypt_file
#DESENCRIPTAR LUEGO ORDENAR EN DIFERENTES ARCHIVOS O CARPETAS
from src.file_encript import encrypt_file, decrypt_file
# Removed bad import
def encrypt_folder(folder_path, password):
    print(f"Procesando carpeta: {folder_path}...")
    archivos_procesados = 0
    errores = 0
    # os.walk permite entrar en subcarpetas automáticamente
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_name = file_name.strip('"')
            partes = file_name.split('.')
            if partes[-1] == "enc" or partes[-1] == "key":
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

def decrypt_folder(folder_path, password):
    archivos_procesados = 0
    errores = 0
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # solo si acaba en .enc
            file_name = file_name.strip('"')
            partes = file_name.split('.')
            # Verificacion:
            if not file_name.endswith(".enc"):
                continue
            else:
                full_path = os.path.join(root, file_name)
                exito, mensaje = decrypt_file(full_path, password)
                if exito == True:
                    archivos_procesados += 1
                else:
                    errores += 1
                    print(f"Error en {file_name}: {mensaje}")

    return f"Proceso terminado. Restaurados: {archivos_procesados}. Errores: {errores}"