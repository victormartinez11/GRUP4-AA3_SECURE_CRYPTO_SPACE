import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import src.vars as var
import src.fichers as fil
# Genera una salt aleatoria de 16 bytes
def generate_salt():
    salt=os.urandom(16)
    return salt

# Genera una key a partir de una password y una salt
def key_derivation(password,salt):
    if not password or not salt:
        raise ValueError("Password i salt no poden ser buits")
    elif not isinstance(password, str) or not isinstance(salt, bytes):
        raise TypeError("Password ha de ser una cadena i salt ha de ser bytes")
    elif len(salt) != var.SALT_SIZE:
        raise ValueError(f"Salt ha de tenir una longitud de {var.SALT_SIZE}")
    password = password.encode("utf-8") 
    key=hashlib.pbkdf2_hmac("sha256", password, salt, var.ITERATIONS, var.KEY_SIZE)      
    if len(key) != var.KEY_SIZE:
        raise ValueError(f"Key ha de tenir una longitud de {var.KEY_SIZE}")
    return key

def calculate_file_hash(file_path):
    try:
        sha256_hash = hashlib.sha256()
    
        with open(file_path, "rb") as f:
            chunk = f.read(var.CHUNK_SIZE)
            while len(chunk) > 0:
                sha256_hash.update(chunk)
                chunk = f.read(var.CHUNK_SIZE)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"[Error]: No es troba el fitxer {file_path}")
    except Exception as e:
        print(f"[Error]: {e}")


#Encripta i desencripta un fitxer
def encrypt_file(file_path, password, output=None):
    validate, missatge = fil.validate_file(file_path)
    if not validate:
        return False, missatge

    if output is None:
        output = file_path + ".enc"
    
    if os.path.exists(output):
        output = os.path.basename(output)
        return False, f"Error: Ja existeix un fitxer amb aquest nom: {output}"

    try:
        # Genera un salt aleatori que representara al fitcher a encriptar
        salt = generate_salt()
        # Derivar la key a partir de la password de l'usuario i la salt nou creat per el fitxer 
        key = key_derivation(password, salt)
        # Generar un IV aleatori pero el fitxer
        iv = os.urandom(16)
        with open(file_path, "rb") as f:
            file_data = f.read()

        # Calcular el HASH abans de encriptar
        original_hash = calculate_hash(file_data) # 32 bytes

        # Padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(file_data) + padder.finalize()

        # Encriptar
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        #Genera el fitxer encriptat
        final_content = salt + iv + original_hash + encrypted_data
        
        binary=True
        fildata=fil.write_content(output, final_content, binary)
        if not fildata:
            return False, "Error crític durant el xifratge"
        return True, fildata

    except Exception as e:
        return False, f"Error crític durant el xifratge: {e}"



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