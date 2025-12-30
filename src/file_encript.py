import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from src.fichers import salt_read_file
from src.fichers import salt_read_file    
##FUNCIO PER DESENCRIPTAR
from cryptography.fernet import Fernet, InvalidToken

# def get_key_for_file_encription(password):
#     #SOLO lee la sal. Si no existe, lanza error. 
#     salt = salt_read_file()
#     if salt == None:
#         raise FileNotFoundError("CRITICAL: No se encuentra el archivo de Salt. El usuario no está registrado.")
#     # Si la sal existe, derivamos la clave
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=32,
#         salt=salt,
#         iterations=480000,
#     )
#     salt=base64.urlsafe_b64encode(kdf.derive(password.encode()))
#     return salt
    
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

#FUNCIO PER DESENCRIPTAR
def decrypt_file(file_path, password):
    try:
        # Recuperamos la MISMA clave usando la contraseña pasada por el usuario en caso de UI el pass de login
        key = get_key_for_file_encription(password)
        f = Fernet(key)
        # archivo cifrado (.enc)
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        # desencriptar
        # Si la password es incorrecta, aquí saltará un error (InvalidToken)
        decrypted_data = f.decrypt(encrypted_data)
        # Quitar extensión .enc para recuperar el nombre original
        if file_path.endswith(".enc"):
            new_path = file_path[:-4] # Borra los últimos 4 caracteres (.enc)
        else:
            new_path = file_path + ".decrypted"
        # Guardado del archivo limpio
        with open(new_path, "wb") as file:
            file.write(decrypted_data)
        # Borrado del archivo cifrado
        os.remove(file_path)
        print(f"Archivo restaurado: {new_path}")
        return True, new_path

    except InvalidToken:
        return False, "Contraseña incorrecta"
    except Exception as e:
        return False, f"Error al descifrar: {e}"
    