
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
        return None
    except Exception as e:
        print("[ERROR] Reading salt: ", e)
        return None