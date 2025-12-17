import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from src.fichers import salt_read_file
from src.fichers import salt_read_file   
def get_key_for_file_encription(password):
    #SOLO lee la sal. Si no existe, lanza error. 
    salt = salt_read_file()
    if salt == None:
        raise FileNotFoundError("CRITICAL: No se encuentra el archivo de Salt. El usuario no está registrado.")
    # Si la sal existe, derivamos la clave
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    salt=base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return salt
    
def encrypt_file(file_path, password):
    #Cifra usando la contraseña del usuario
    try:
        key = get_key_for_file_encription(password)
        f = Fernet(key)
        try:
            with open(file_path, "rb") as file:
                file_data = file.read()
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return False
        
        encrypted_data = f.encrypt(file_data)
        path = file_path + ".enc"
        with open(path, "wb") as file:
            file.write(encrypted_data)

        os.remove(file_path) # Borrar original CAMBIAR POR WIPE
        print(f"Cifrado con éxito.")
        return True, path

    except Exception as e:
        print(f"Error al cifrar: {e}")
        return False

    