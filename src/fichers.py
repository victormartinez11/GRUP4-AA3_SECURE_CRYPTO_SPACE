import json
import os
import src.vars as var
def read_key():
    try:
        with open("file_key.key", "r") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        print("[ERROR] Key not found")
        return None
    
    return key

def write_key(key):
    try:
        with open("file_key.key", "w") as key_file:
            key_file.write(key)
    except FileNotFoundError:
        print("[ERROR] Key not found")


def salt_write_file(salt):
    try:
        with open("file_salt.key", "wb") as salt_file:
            salt_file.write(salt)
    except FileNotFoundError as e:
        print("[ERROR] Salt not found Details: ", e)
    except Exception as e:
        print("[ERROR] Exception Details: ", e)

def salt_read_file():
    try:
        with open("file_salt.key", "rb") as salt_file:
            salt = salt_file.read()
        return salt
    except FileNotFoundError:
        print("[ERROR] Salt not found")
    except Exception as e:
        print("[ERROR] Reading salt: ", e)
      

def read_usersjson():
    try:
        if not os.path.exists(var.USERS_FILE):
            print("[ERROR] Users not found")
            userslist = []
            return userslist
        else:
            with open(var.USERS_FILE, "r") as file_users:
                userslist = json.load(file_users)
            return userslist

    except Exception as e:
        print("[WARNING] Error reading users or empty file, returning empty list:", e)
        return []
      
def write_usersjson(data):
    try:
        os.makedirs(os.path.dirname(var.USERS_FILE), exist_ok=True)
        with open(var.USERS_FILE, "w") as file_users:
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

def write_content(path, data, binary):
    try:
        folder = os.path.dirname(path)
        if folder not in os.listdir(): 
            os.makedirs(folder, exist_ok=True)
    except Exception as e:
        print("[ERROR] Creating folder: ", e)
    
    try:
        if binary == True:
            mode = "wb"
        else:
            mode = "w"
        
        with open(path, mode) as f:
            f.write(data)
        correcte = True
        return correcte, f"Fitxer guardat: {path} [OK]"

    except Exception as e:
        print("[ERROR] Writing file: ", e)
        correcte = False
        return correcte, f"Error escrivint {path}: {e} [ERROR]"

def read_content(path, binary):
    valid, msg = validate_file(path)
    if valid == False:
        return valid, msg
    try:
        if binary == True:
            mode = "rb"
        else:
            mode = "r"
        
        with open(path, mode) as f:
            data = f.read()
        
        correcte = True
        return correcte, data
    except FileNotFoundError:
        print("[ERROR] File not found: ", path)
        correcte = False
        return correcte, f"Fitxer no trobat: {path}"

    except IsADirectoryError:
        print("[ERROR] Path is a directory: ", path)
        correcte = False
        return correcte, f"La ruta és una carpeta, no un fitxer: {path}"

    except Exception as e:
        print("[ERROR] Reading file: ", e)
        correcte = False
        return correcte, f"Error llegint {path}: {e}"