import os
from src.file_encript import encrypt_file
from src.encriptar import encrypt_folder

def main():
    print("--- MENU TEST ---") 
    if not os.path.exists("file_salt.key"):
        print("ALERTA: No existe 'file_salt.key'.")
        print("Ejecuta primero: python generar_saltprovisonal.py")
        return

    opcion = input("¿Qué quieres cifrar? (1=Archivo, 2=Carpeta): ")
    ruta = input("Ruta del archivo/carpeta: ").strip('"') # .strip quita comillas si arrastras el fichero
    password = input("Contraseña: ")
    if opcion == "1":
        if os.path.isfile(ruta):
            exito, mensaje = encrypt_file(ruta, password)
            print(f"Resultado: {mensaje}")
        else:
            print("Error: Eso no es un archivo.")

    elif opcion == "2":
        if os.path.isdir(ruta):
            res = encrypt_folder(ruta, password)
            print(res)
        else:
            print("Error: Eso no es una carpeta.")
    elif opcion == "3":
        if os.path.isfile(ruta):
            res = decrypt_file(ruta, password)
            print(f"Resultado: {res}")
        else:
            print("Error: Eso no es un archivo.")
    else:
        print("Opción no válida.")


main()