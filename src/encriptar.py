import os
from cryptography.fernet import Fernet

salt=os.urandom(16)
print(salt)
key=Fernet.generate_key()
print(key)

