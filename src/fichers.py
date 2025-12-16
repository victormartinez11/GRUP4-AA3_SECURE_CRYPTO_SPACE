
def read_key():
    try:
        with open("file_key.key", "r") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        print("[ERROR] Key not found")
    
    return key

def write_key(key):
    try:
        with open("file_key.key", "w") as key_file:
            key_file.write(key)
    except FileNotFoundError:
        print("[ERROR] Key not found")
