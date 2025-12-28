




def register_validation(username, password, confirm_password):
    validation = False
    if not username or not password:
        raise ValueError("Tots els camps són obligatoris.")
    else:
        if len(username) < 4 and len(password) < 8 and len(confirm_password) < 8:
            raise ValueError("El nom d'usuari ha de tenir almenys 4 caràcters i la contrasenya almenys 8 caràcters.")
        elif password != confirm_password:
            raise ValueError("Les contrasenyes no coincideixen.")
        else:
            userlist = read_users()
            if username in userlist:
                raise ValueError("El nom d'usuari ja existeix.")
            else:
                validation = True

    return validation

    