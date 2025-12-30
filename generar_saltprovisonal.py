# import os
# from src.fichers import salt_write_file

# def generar_salt_inicial():
#     print("HERRAMIENTA DE GENERACIÓN DE SALT (TEST)")
    
#     # Generamos 16 bytes aleatorios (la "sal")
#     nueva_salt = os.urandom(16)
    
#     # Usamos tu función de 'fichers.py' para guardarla
#     try:
#         salt_write_file(nueva_salt)
#         print(f"Archivo 'file_salt.key' generado correctamente.")
#         print("Ahora ya puedes usar el menú de pruebas.")
#     except Exception as e:
#         print(f"Error al escribir la salt: {e}")

# generar_salt_inicial()