import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import src.config.constants as const
import src.core.file_manager as fil

# Genera una salt aleatoria de 16 bytes
def generate_salt():
    salt=os.urandom(16)
    return salt

# Genera una key a partir de una password y una salt
def key_derivation(password, salt):
    if not password or not salt:
        raise ValueError("Password i salt no poden ser buits")
    
    if len(salt) != const.SALT_SIZE:
        raise ValueError(f"Salt ha de tenir una longitud de {const.SALT_SIZE}")
    
    if isinstance(password, str):
        password = password.encode("utf-8") 
        
    key = hashlib.pbkdf2_hmac("sha256", password, salt, const.ITERATIONS, const.KEY_SIZE)      
    if len(key) != const.KEY_SIZE:
        raise ValueError(f"Key ha de tenir una longitud de {const.KEY_SIZE}")
    return key

def calculate_file_hash(file_path):
    try:
        sha256_hash = hashlib.sha256()
    
        with open(file_path, "rb") as f:
            chunk = f.read(const.CHUNK_SIZE)
            while len(chunk) > 0:
                sha256_hash.update(chunk)
                chunk = f.read(const.CHUNK_SIZE)
        return sha256_hash.digest()
    except FileNotFoundError:
        print(f"[Error]: No es troba el fitxer {file_path}")
        return None
    except Exception as e:
        print(f"[Error]: {e}")
        return None
# Calcula el hash d'un fitxer
def calculate_hash(data):
    hashcalc=hashlib.sha256(data).digest()
    return hashcalc

# Encripta i desencripta un fitxer
def encrypt_file(file_path, password, output=None):
    validate, missatge = fil.validate_file(file_path)
    if not validate:
        return False, missatge

    if output is None:
        output = file_path + ".enc"

    try:
        salt = generate_salt()
        key = key_derivation(password, salt)
        iv = os.urandom(16)
        
        success, file_data = fil.read_content(file_path, binary=True)
        if not success:
            return False, file_data 

        original_hash = calculate_file_hash(file_path)
        if original_hash is None:
             return False, "Error calculant hash"

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(file_data) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        final_content = salt + iv + original_hash + encrypted_data
        
        binary=True
        success, msg = fil.write_content(output, final_content, binary)
        if not success:
            return False, msg
            
        return True, "Fitxer encriptat correctament"

    except Exception as e:
        return False, f"Error crític durant el xifratge: {e}"



def decrypt_file(file_path, password):
    binary=True
    success, contingut = fil.read_content(file_path, binary)

    if not success:
        return False, contingut 

    try:
        if len(contingut) < 64: 
             return False, "Arxiu corrupte o massa curt."
        
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

        success, msg = fil.write_content(ruta_sortida, dades_originals, binary=True)
        
        if success:     
            try:
                os.remove(file_path)
            except OSError:
                pass 
            
            return True, f"Arxiu recuperat: {os.path.basename(ruta_sortida)}"
        else:
            return False, msg

    except ValueError:
        return False, "Contrasenya incorrecta o dades corruptes (padding error)."
    except Exception as e:
        return False, f"Error desencriptant: {e}"

# Encriptar carpetes
def encrypt_folder(folder_path, password):
    print(f"Procesando carpeta: {folder_path}...")
    archivos_procesados = 0
    errores = 0
    
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_name = file_name.strip('"')
            partes = file_name.split('.')
            if partes[-1] == "enc" or partes[-1] == "key":
                continue
            full_path = os.path.join(root, file_name)
            
            exito, mensaje = encrypt_file(full_path, password)
            if exito:
                archivos_procesados += 1
                try:
                    os.remove(full_path)
                except:
                    pass
            else:
                errores += 1
                print(f"Error en {file_name}: {mensaje}")

    return f"Proceso terminado. Encriptados: {archivos_procesados}. Errores: {errores}"

# Desencriptar carpetes
def decrypt_folder(folder_path, password):
    archivos_procesados = 0
    errores = 0
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_name = file_name.strip('"')
            if not file_name.endswith(".enc"):
                continue
            else:
                full_path = os.path.join(root, file_name)
                exito, mensaje = decrypt_file(full_path, password)
                if exito:
                    archivos_procesados += 1
                else:
                    errores += 1
                    print(f"Error en {file_name}: {mensaje}")

    return f"Proceso terminado. Restaurados: {archivos_procesados}. Errores: {errores}"