import src.const.constants as constst
import src.core.file_manager as fichers
import src.core.security as secure

# Aquesta funció mira si un usuari ja existeix a la llista
# Crida la funció de llegir usuaris
def user_exists(username):
    exists = False
    userlist = fichers.read_usersjson()
    for user in userlist:
        if user.get("User") == username:
            exists = True
    return exists

# Aquesta funció comprova que el nom i la contrasenya siguin correctes (mida, etc.)
def register_validation(username, password):
    validation = False
    if not username or not password:
        raise ValueError("Tots els camps són obligatoris.")
    else:
        # Mirem si tenen la longitud mínima
        if len(username) < 4 and len(password) < 8:
            raise ValueError("El nom d'usuari ha de tenir almenys 4 caràcters i la contrasenya almenys 8 caràcters.")
        else:
            if user_exists(username):
                raise ValueError("El nom d'usuari ja existeix.")
            else:
                validation = True

    return validation

# Aquesta funció registra un nou usuari i guarda la seva clau
# Crida funcions de seguretat per generar la clau
def register_user(username, password):
    try:
        register_validation(username, password)
        salt = secure.generate_salt()
        key_hash = secure.key_derivation(password, salt)

        # Convertim a text hexadecimal per guardar-ho al fitxer
        new_user = {"User": username, "Salt": salt.hex(), "Hash": key_hash.hex()}
        current_users = fichers.read_usersjson()
        current_users.append(new_user)
        fichers.write_usersjson(current_users)

        return True, "Usuari registrat correctament."

    except ValueError as ve:
        return False, str(ve)
        
    except Exception as e:
        return False, f"Error crític del sistema: {e}"

# Aquesta funció deixa entrar l'usuari si la contrasenya és bona
# Compara el hash de la contrasenya amb el que tenim guardat
def login_user(username, password):
    try:
        if not username or not password:
            return False, "Usuari o contrasenya buits."
            
        current_users = fichers.read_usersjson()
        user_data = None
        
        # Busquem l'usuari
        for user in current_users:
            if user.get("User") == username:
                user_data = user
        
        if not user_data:
            return False, "Usuari o contrasenya incorrectes." 
            
        try:
            salt = bytes.fromhex(user_data["Salt"])
            stored_hash = bytes.fromhex(user_data["Hash"])
        except ValueError:
             return False, "Error en el format de dades de l'usuari."

        derived_key = secure.key_derivation(password, salt)
        
        if derived_key == stored_hash:
            return True, "Login correcte."
        else:
             return False, "Usuari o contrasenya incorrectes."

    except Exception as e:
        return False, f"Error en login: {e}"
