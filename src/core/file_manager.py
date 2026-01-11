import json
import os
import datetime
import shutil
import src.const.constants as const

# Aquesta funció llegeix la llista d'usuaris del fitxer json
# Fa servir el mòdul json
def read_usersjson():
    try:
        if not os.path.exists(const.USERS_FILE):
            print("[ERROR] Fitxer d'usuaris no trobat")
            return []
        else:
            with open(const.USERS_FILE, "r") as file_users:
                userslist = json.load(file_users)
            return userslist

    except Exception as e:
        print("[AVÍS] Error llegint usuaris o llista buida:", e)
        return []
      
# Aquesta funció guarda els usuaris al fitxer json
def write_usersjson(data):
    try:
        os.makedirs(os.path.dirname(const.USERS_FILE), exist_ok=True)
        with open(const.USERS_FILE, "w") as file_users:
            json.dump(data, file_users, indent=4)

    except Exception as e:
        print("[ERROR] Escrivint usuaris: ", e)

# Aquesta funció comprova si un fitxer existeix i és vàlid
def validate_file(path):
    if not path:
        return False, f"La ruta està buida." 

    if not os.path.exists(path):
        return False, f"No s'ha trobat el fitxer: {path}" 
    
    if not os.path.isfile(path):
        return False, f"Això és una carpeta, no un fitxer: {path}" 

    return True, "[OK]"

# Aquesta funció escriu dades (text o binari) en un fitxer
def write_content(path, data, binary):
    try:
        folder = os.path.dirname(path)
        if folder and not os.path.exists(folder): 
            os.makedirs(folder, exist_ok=True)
    except Exception as e:
        print("[ERROR] Creant carpeta: ", e)
    
    try:
        mode = "wb" if binary else "w"
        
        with open(path, mode) as f:
            f.write(data)
        
        return True, f"Fitxer guardat: {path} [OK]"

    except Exception as e:
        print("[ERROR] Escrivint fitxer: ", e)
        return False, f"Error escrivint {path}: {e} [ERROR]"

# Aquesta funció llegeix el contingut d'un fitxer
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
        print("[ERROR] Fitxer no trobat: ", path)
        return False, f"Fitxer no trobat: {path}"

    except IsADirectoryError:
        print("[ERROR] Això és una carpeta: ", path)
        return False, f"La ruta és una carpeta, no un fitxer: {path}"

    except Exception as e:
        print("[ERROR] Llegint fitxer: ", e)
        return False, f"Error llegint {path}: {e}"

# Aquesta funció crea una nova carpeta
def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        return True, f"Carpeta creada: {path}"
    except Exception as e:
        return False, f"Error creant carpeta: {e}"

# Aquesta funció ens diu quins fitxers hi ha dins una carpeta
# Fa servir os.listdir
def list_directory(path):
    try:
        if not os.path.exists(path):
            return []
        items = os.listdir(path)
        items.sort()
        return items
    except Exception as e:
        print(f"[ERROR] Llistant directori {path}: {e}")
        return []

# Aquesta funció obté informació del fitxer com la mida i la data
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

# Aquesta funció retorna si la ruta és una carpeta o no
def is_directory(path):
    return os.path.isdir(path)



# Aquesta funció esborra un fitxer de manera segura (sobrescriu abans d'esborrar)
def secure_delete(path):
    try:
        if os.path.isfile(path):
            length = os.path.getsize(path)
            # Sobrescrivim amb dades aleatòries
            with open(path, "wb") as f:
                f.write(os.urandom(length))
            # Ara ja podem esborrar
            os.remove(path)
            return True, "Arxiu eliminat de forma segura."
        elif os.path.isdir(path):
            shutil.rmtree(path)
            return True, "Carpeta eliminada correctament."
        return False, "L'arxiu no existeix."
    except Exception as e:
        return False, f"Error eliminant: {e}"

# Aquesta funció guarda la configuració de l'últim lloc obert
def save_config(path):
    try:
        with open(const.CONFIG_FILE, "w") as f:
            f.write(path)
        return True, "Configuració guardada."
    except Exception as e:
        print(f"[ERROR] Guardant configuració: {e}")
        return False, f"Error guardant configuració: {e}"

# Aquesta funció carrega l'última carpeta que hem visitat
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
