import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# El mòdul cryptography es fa servir per encriptar i desencriptar de forma segura
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import src.const.constants as const
import src.core.file_manager as fil

# Aquesta funció genera una "salt" aleatòria de 16 bytes per fer més segura la clau
# Fa servir el mòdul os
def generate_salt():
    salt = os.urandom(16)
    return salt

# Aquesta funció crea una clau segura barrejant la contrasenya i la salt
# Fa servir el mòdul hashlib i crida funcions de text
def key_derivation(password, salt):
    if not password or not salt:
        raise ValueError("La contrasenya i la salt no poden ser buides")
    
    if len(salt) != const.SALT_SIZE:
        raise ValueError(f"La salt ha de tenir una longitud de {const.SALT_SIZE}")
    
    if isinstance(password, str):
        password = password.encode("utf-8") 
        
    # Creem la clau fent moltes iteracions perquè sigui difícil d'endevinar
    key = hashlib.pbkdf2_hmac("sha256", password, salt, const.ITERATIONS, const.KEY_SIZE)      
    if len(key) != const.KEY_SIZE:
        raise ValueError(f"La clau ha de tenir una longitud de {const.KEY_SIZE}")
    return key

# Aquesta funció calcula el hash d'un fitxer per saber si l'han modificat
# Fa servir el mòdul hashlib
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

# Aquesta funció calcula el hash d'unes dades que tenim en memòria
# Fa servir el mòdul hashlib
def calculate_hash(data):
    hashcalc = hashlib.sha256(data).digest()
    return hashcalc

# Aquesta funció agafa un fitxer, l'encripta amb una contrasenya i el guarda
# Crida les funcions de generar salt, derivar clau i calcular hash finalment borra el fitxer original 
def encrypt_file(file_path, password, output=None):
    validate, missatge = fil.validate_file(file_path)
    if not validate:
        return False, missatge

    if output is None:
        output = file_path + ".enc"

    try:
        salt = generate_salt()
        key = key_derivation(password, salt)
        iv = os.urandom(16) # Un codi aleatori que necessita l'algoritme de xifrat
        
        success, file_data = fil.read_content(file_path, binary=True)
        if not success:
            return False, file_data 

        original_hash = calculate_file_hash(file_path)
        if original_hash is None:
             return False, "Error calculant el hash del fitxer"

        # Afegim farcit (padding) perquè les dades tinguin la mida correcta
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(file_data) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Guardem tot junt: Salt + IV + Hash + Dades Encriptades
        final_content = salt + iv + original_hash + encrypted_data
        
        binary = True
        success, msg = fil.write_content(output, final_content, binary)
        if not success:
            return False, msg
            
        return True, "Fitxer encriptat correctament"

    except Exception as e:
        return False, f"Error crític durant el xifratge: {e}"

# Aquesta funció agafa un fitxer encriptat i el restaura si la contrasenya és bona
# Comprova que el hash sigui correcte per seguretat i finalment borra el fitxer encriptat
def decrypt_file(file_path, password, output_path=None):
    binary = True
    success, contingut = fil.read_content(file_path, binary)

    if not success:
        return False, contingut 

    try:
        if len(contingut) < 64: 
             return False, "L'arxiu està corrupte o és massa curt."
        
        # Separem les parts del fitxer
        salt = contingut[:16]
        iv = contingut[16:32]
        hash_guardat = contingut[32:64]
        dades_encriptades = contingut[64:]

        key = key_derivation(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        padded_data = decryptor.update(dades_encriptades) + decryptor.finalize()

        # Traiem el farcit que havíem posat
        unpadder = padding.PKCS7(128).unpadder()
        dades_originals = unpadder.update(padded_data) + unpadder.finalize()

        hash_calculat = calculate_hash(dades_originals)

        if hash_calculat != hash_guardat:
            return False, "[ALERTA]: El fitxer ha estat modificat o està malament."

        eliminar_original = False
        
        if output_path:
            ruta_sortida = output_path
            eliminar_original = False 
        else:
            if file_path.endswith(".enc"):
                ruta_sortida = file_path[:-4]
            else:
                ruta_sortida = file_path + ".decrypted"
            eliminar_original = True

        success, msg = fil.write_content(ruta_sortida, dades_originals, binary=True)
        
        if success:     
            if eliminar_original:
                try:
                    os.remove(file_path)
                except OSError:
                    pass 
            
            return True, f"Arxiu guardat a: {os.path.basename(ruta_sortida)}"
        else:
            return False, msg

    except ValueError:
        return False, "La contrasenya no és correcta o el fitxer està trencat."
    except Exception as e:
        return False, f"Error desencriptant: {e}"