# -*- coding: latin-1 -*-

#importación de recursos necessarios
import os
import hashlib
import shutil

carpeta_base = "storage"
VAULT = os.path.join(carpeta_base, "Vault") #carpeta donde se guardaran los archivos
contraseña = os.path.join(carpeta_base, "password.txt") 

#función para crear el vault si no existe
def crear_vault():
    if not os.path.exists(VAULT):
        os.makedirs(VAULT)

#función para guardar la contraseña del usuario, cifrado con SHA-256
def crear_contraseña(password):
    os.makedirs(carpeta_base, exist_ok=True)

    hashed = hashlib.sha256(password.encode()).hexdigest()
    with open(contraseña, "w") as f:
        f.write(hashed)

#devuelve si la contraseña es correcta o no
def comprovar_contraseña(password):
    if not os.path.exists(contraseña):
        print("No hay contraseña configurada.")
        return False

    hashed = hashlib.sha256(password.encode()).hexdigest()
    with open(contraseña, "r") as f:
        return f.read() == hashed

#función para importar un archivo al vault y borrarlo en su ubicación anterior
def importar_archivo(file_path, password):
    if not check_password(password):
        print("Contraseña incorrecta.")
        return

    if not os.path.exists(file_path):
        print("El archivo no existe.")
        return

    os.makedirs(vault, exist_ok=True)

    file_name = os.path.basename(file_path)
    destination = os.path.join(vault, file_name)

    try:
        shutil.copy(file_path, destination) 
        
        os.remove(file_path)

        print("Archivo importado exitosamente")
        print("Se ha borrado el archivo en su ubicación anterior")

    except PermissionError:
        print("Error: No tenemos permisos para modificar el archivo")
    except OSError:
        print("Error del sistema.")