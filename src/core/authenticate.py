import src.config.constants as const
import src.core.file_manager as fichers
import src.core.security as secure
from finestres_errors import *

def user_exists(username):
    exists = False
    userlist = fichers.read_usersjson()
    for user in userlist:
        if user.get("User") == username:
            exists = True
    return exists

def register_validation(username, password):
    validation = False
    if not username or not password:
        raise ValueError("Tots els camps són obligatoris.")
    else:
        # Validació de contrasenya bàsica
        if len(username) < 4 and len(password) < 8:
            raise ValueError("El nom d'usuari ha de tenir almenys 4 caràcters i la contrasenya almenys 8 caràcters.")
        else:
            if user_exists(username):
                raise ValueError("El nom d'usuari ja existeix.")
            else:
                validation = True

    return validation

def register_user(username, password):
    try:
        register_validation(username, password)
        salt = secure.generate_salt()
        key_hash = secure.key_derivation(password, salt)

        new_user = {"User": username, "Salt": salt.hex(), "Hash": key_hash.hex()}
        current_users = fichers.read_usersjson()
        current_users.append(new_user)
        fichers.write_usersjson(current_users)

        return True, "Usuari registrat correctament."

    except ValueError as ve:
        return False, value_error(ve)
        
    except Exception:
        return False, error_critic_sistema()

def login_user(username, password):
    try:
        if not username or not password:
            return False, "Usuari o contrasenya buits."
            
        current_users = fichers.read_usersjson()
        user_data = None
        
        for user in current_users:
            if user.get("User") == username:
                user_data = user
        
        if not user_data:
            return False, value_error() 
            
        try:
            salt = bytes.fromhex(user_data["Salt"])
            stored_hash = bytes.fromhex(user_data["Hash"])
        except ValueError:
             return False, value_error()

        derived_key = secure.key_derivation(password, salt)
        
        if derived_key == stored_hash:
            return True, "Login correcte."
        else:
             return False, error_login()

    except Exception:
        return False, error_login()
