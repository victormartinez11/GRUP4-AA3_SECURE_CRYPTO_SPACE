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
        return sha256_hash.digest()
    except FileNotFoundError:
        print(f"[Error]: No es troba el fitxer {file_path}")
    except Exception as e:
        print(f"[Error]: {e}")

def calculate_hash(data):
    hashcalc=hashlib.sha256(data).digest()
    return hashcalc

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
        #original_hash = calculate_hash(file_data) 
        original_hash = calculate_file_hash(file_path)
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
    binary=True
    exit_lectura, contingut = fil.read_content(file_path, binary)

    if not exit_lectura:
        return False, contingut 

    try:
        salt = contingut[:16]
        iv = contingut[16:32]
        hash_guardat = contingut[32:64]
        dades_encriptades = contingut[64:]

        key = key_derivation(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        padded_data = decryptor.update(dades_encriptades) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        dades_originals = unpadder.update(padded_data) + unpadder.finalize()

        hash_calculat = calculate_hash(dades_originals)

        if hash_calculat != hash_guardat:
            return False, "[ALERTA]: Hash incorrecte. El fitxer podria estar corrupte o manipulat."

        if file_path.endswith(".enc"):
            ruta_sortida = file_path[:-4]
        else:
            ruta_sortida = file_path + ".decrypted"

        exit_escriptura, missatge_escriptura = fil.write_content(ruta_sortida, dades_originals, binary=True)
        
        if exit_escriptura:     
            try:
                os.remove(file_path)
            except OSError:
                pass 
            
            return True, f"Arxiu recuperat: {os.path.basename(ruta_sortida)}"
        else:
            return False, missatge_escriptura

    except ValueError:
        return False, "Contrasenya incorrecta."
    except Exception as e:
        return False, f"Error desencriptant: {e}"