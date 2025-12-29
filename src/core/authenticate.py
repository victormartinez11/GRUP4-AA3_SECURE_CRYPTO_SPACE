import src.vars as var
import src.fichers as fichers
import src.core.security as secure
def user_exists(username):
    exists = False
    userlist = fichers.read_usersjson()
    for user in userlist:
        if user.get("username") == username:
            exists = True
    return exists

#AÑADIR UN CONFIRM PASSWORD
def register_validation(username, password):
    validation = False
    if not username or not password:
        raise ValueError("Tots els camps són obligatoris.")
    else:
        if len(username) < 4 or len(password) < 8:
            raise ValueError("El nom d'usuari ha de tenir almenys 4 caràcters i la contrasenya almenys 8 caràcters.")
        # elif password != confirm_password:
        #     raise ValueError("Les contrasenyes no coincideixen.")
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

        new_user = {"User": username, "Salt": salt, "Hash": key_hash}
        current_users = fichers.read_usersjson()
        current_users.append(new_user)
        fichers.write_usersjson(current_users)

        return True, "Usuari registrat correctament."

    except ValueError as ve:
        return False, str(ve)
        
    except Exception as e:
        return False, f"Error crític del sistema: {e}"

def login_user(username, password):
    try:
        if not username or not password:
            return False, "Usuari o contrasenya buits."
            
        current_users = fichers.read_usersjson()
        user_data = None
        
        for user in current_users:
            if user["User"] == username:
                user_data = user
                break #TEMPORAL
        
        if not user_data:
            return False, "Usuari o contrasenya incorrectes." 
            
        stored_salt_hex = user_data["Salt"]
        stored_hash_hex = user_data["Hash"]
        
        salt = bytes.fromhex(stored_salt_hex)
        stored_hash = bytes.fromhex(stored_hash_hex)
        
        derived_key = secure.key_derivation(password, salt)
        
        if derived_key == stored_hash:
            return True, "Login correcte."
        else:
             return False, "Usuari o contrasenya incorrectes."

    except Exception as e:
        return False, f"Error en login: {e}"