import json
import os
import datetime
import shutil
import src.config.constants as const

#Funcions per a la gestio de claus-->Lectura
def read_key():
    try:
        with open("file_key.key", "r") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        print("[ERROR] Key not found")
        return None
    
    return key
#Funcions per a la gestio de claus-->Escritura
def write_key(key):
    try:
        with open("file_key.key", "w") as key_file:
            key_file.write(key)
    except FileNotFoundError:
        print("[ERROR] Key not found")

#Funcion per a escritura de salt en fitxer
def salt_write_file(salt):
    try:
        with open("file_salt.key", "wb") as salt_file:
            salt_file.write(salt)
    except FileNotFoundError as e:
        print("[ERROR] Salt not found Details: ", e)
    except Exception as e:
        print("[ERROR] Exception Details: ", e)

#Funcion per a lectura de salt en fitxer
def salt_read_file():
    try:
        with open("file_salt.key", "rb") as salt_file:
            salt = salt_file.read()
        return salt
    except FileNotFoundError:
        print("[ERROR] Salt not found")
    except Exception as e:
        print("[ERROR] Reading salt: ", e)
      
#Funcio per a lectura de fitxer users.json
def read_usersjson():
    try:
        if not os.path.exists(const.USERS_FILE):
            print("[ERROR] Users not found")
            return []
        else:
            with open(const.USERS_FILE, "r") as file_users:
                userslist = json.load(file_users)
            return userslist

    except Exception as e:
        print("[WARNING] Error reading users or empty file, returning empty list:", e)
        return []
      
#Funcio per a escritura de fitxer users.json
def write_usersjson(data):
    try:
        os.makedirs(os.path.dirname(const.USERS_FILE), exist_ok=True)
        with open(const.USERS_FILE, "w") as file_users:
            json.dump(data, file_users, indent=4)

    except Exception as e:
        print("[ERROR] Writing users: ", e)

# Validar ruta de fitxer
def validate_file(path):
    if not path:
        return False, f"La ruta està buida." 

    if not os.path.exists(path):
        return False, f"No s'ha trobat el fitxer: {path}" 
    
    if not os.path.isfile(path):
        return False, f"La ruta és una carpeta, no un fitxer: {path}" 

    return True, "[OK]"
#Funcio per a escritura de fitxer encriptat
def write_content(path, data, binary):
    try:
        folder = os.path.dirname(path)
        if folder and not os.path.exists(folder): 
            os.makedirs(folder, exist_ok=True)
    except Exception as e:
        print("[ERROR] Creating folder: ", e)
    
    try:
        mode = "wb" if binary else "w"
        
        with open(path, mode) as f:
            f.write(data)
        
        return True, f"Fitxer guardat: {path} [OK]"

    except Exception as e:
        print("[ERROR] Writing file: ", e)
        return False, f"Error escrivint {path}: {e} [ERROR]"

#Funcio per a lectura de fitxer encriptat
def read_content(path, binary):
    valid, msg = validate_file(path)
    if not valid:
        return False, msg
    try:
        mode = "rb" if binary else "r"
        
        with open(path, mode) as f:
            data = f.read()
        
        return True, data
    except FileNotFoundError:
        print("[ERROR] File not found: ", path)
        return False, f"Fitxer no trobat: {path}"

    except IsADirectoryError:
        print("[ERROR] Path is a directory: ", path)
        return False, f"La ruta és una carpeta, no un fitxer: {path}"

    except Exception as e:
        print("[ERROR] Reading file: ", e)
        return False, f"Error llegint {path}: {e}"

def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        return True, f"Carpeta creada: {path}"
    except Exception as e:
        return False, f"Error creant carpeta: {e}"
#Funcio per a llistat de fitxers i carpetes y retornar la llista ordenada
def list_directory(path):
    try:
        if not os.path.exists(path):
            return []
        items = os.listdir(path)
        items.sort()
        return items
    except Exception as e:
        print(f"[ERROR] Listing directory {path}: {e}")
        return []
#Funcio per a obtenir informacio de fitxer
def get_file_info(path):
    try:
        stats = os.stat(path)
        is_dir = os.path.isdir(path)
        timestamp = stats.st_mtime
        date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
        size = stats.st_size
        return {
            "is_dir": is_dir,
            "timestamp": timestamp,
            "date_str": date_str,
            "size": size,
            "exists": True
        }
    except Exception:
        return {"exists": False}
#Funcio per a comprovar si la ruta es una carpeta
def is_directory(path):
    return os.path.isdir(path)
#Funcio per a la unio de ruta
def path_join(*args):
    return os.path.join(*args)
#Funcio per a obtenir nom de fitxer
def get_basename(path):
    return os.path.basename(path)
#Funcio per a esborrar de manera segura
def secure_delete(path):
    try:
        if os.path.isfile(path):
            length = os.path.getsize(path)
            
            with open(path, "wb") as f:
                f.write(os.urandom(length))
                
            os.remove(path)
            return True, "Arxiu eliminat de forma segura (Wiped)."
            
        elif os.path.isdir(path):
            shutil.rmtree(path)
            return True, "Carpeta eliminada correctament."
            
        return False, "L'arxiu no existeix."

    except Exception as e:
        return False, f"Error eliminant: {e}"

# Funcio per guardar la configuracio (ruta del vault)
def save_config(path):
    try:
        with open(const.CONFIG_FILE, "w") as f:
            f.write(path)
        return True, "Configuració guardada."
    except Exception as e:
        print(f"[ERROR] Guardant configuració: {e}")
        return False, f"Error guardant configuració: {e}"

# Funcio per carregar l'ultim vault utilitzat
def load_last_vault():
    try:
        if os.path.exists(const.CONFIG_FILE):
            with open(const.CONFIG_FILE, "r") as f:
                path = f.read().strip()
                if os.path.isdir(path):
                    return path
    except Exception as e:
        print(f"[ERROR] Carregant configuració: {e}")
    return None
