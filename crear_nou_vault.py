# -*- coding: latin-1 -*-

#importación de recursos necessarios
import os
import hashlib
import shutil

BASE_DIR = "storage" #carpeta base
VAULT = os.path.join(BASE_DIR, "Vault") #carpeta donde se guardaran los archivos
PASSWORD_FILE = os.path.join(BASE_DIR, "password.txt") archivo donde se guarda la contraseña cifrada

#función para crear el vault si no existe
def create_vault():
    if not os.path.exists(VAULT):
        os.makedirs(VAULT)

#función para guardar la contraseña del usuario, cifrado con SHA-256
def set_password(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with open(PASSWORD_FILE, "w") as f:
        f.write(hashed)

#devuelve si la contraseña es correcta o no
def check_password(password):
    if not os.path.exists(PASSWORD_FILE):
        return False

    hashed = hashlib.sha256(password.encode()).hexdigest()
    with open(PASSWORD_FILE, "r") as f:
        return f.read() == hashed

#función para importar un archivo al vault
def import_file(file_path, password):
    if not check_password(password):
        print("Contraseña incorrecta.")
        return

    if not os.path.exists(file_path):
        print("El archivo no existe.")
        return

    vault = "storage/vault"
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