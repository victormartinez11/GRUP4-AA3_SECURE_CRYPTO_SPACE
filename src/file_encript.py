import os
from cryptography.fernet import Fernet
from src.password_utils import generate_key

def encrypt_file(file_path, password):
    #Cifra usando la contraseña del usuario
    try:
        key = generate_key(password)
        f = Fernet(key)

        with open(file_path, "rb") as file:
            file_data = file.read()

        encrypted_data = f.encrypt(file_data)

        new_path = file_path + ".enc"
        with open(new_path, "wb") as file:
            file.write(encrypted_data)

        os.remove(file_path) # Borrar original CAMBIAR POR WIPE
        print(f"Cifrado con éxito.")
        return True, new_path

    except Exception as e:
        print(f"Error al cifrar: {e}")
        return False, str(e)