import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import src.vars as var

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