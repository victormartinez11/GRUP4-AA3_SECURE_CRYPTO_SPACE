# -*- coding: latin_1 -*-
import random
import os

def overwrite_and_deleate():
    while True:
        print("\nAtención! Este paso es ireversible y va a borrar el archivo.\n"
              "Desea proceder con la operacion? (s/n)\n")

        confirmacion = input("> ").lower()

        if confirmacion == "s":
            print("Operacion confirmada.\n")
            break
        elif confirmacion == "n":
            print("\nOperacion cancelada."
                  "Volviendo al menu principal...\n")
            return
        else:
            print("\nIntroduce una opción valida.\n")
            continue


    print("Escribe el nombre del documento que quieres borrar.")
    file_name = input("> ")


    carpetas = ["funcion borrar y sobreescribir","placeholder1", "placeholder2", "placeholder3"]

    sobreescribir(file_name, carpetas)
    borrar(file_name, carpetas)



def sobreescribir(file_name, carpetas):
    
    archivo_encontrado = False

    for direcion in carpetas:
        if not os.path.exists(direcion):
            print(f"Aviso: No se encontro la carpeta {direcion}")
            continue

        for ruta, subcarpetas, archivos in os.walk(direcion):
            if file_name in archivos:
                archivo_encontrado = True
                file_path = os.path.join(ruta, file_name)

                try:
                    with open(file_path, "r") as f:
                        file_len = len(f.read())
                    
                    with open(file_path, "w") as f:
                        for letter in range (file_len):
                            alphabet = "qwertyuiopasdfghjklñzxcvbnm"
                            f.write(random.choice(alphabet))

                except FileNotFoundError:
                    print("Error: Archivo no encontrado")
                    return
                except UnicodeDecodeError:
                    print("Error: Archivo corrupto o no encontrado")
                    return
                except OSError as e:
                    print(f"Error del sistema: {e}")
                    return
    if not archivo_encontrado:
        print("Error: El archivo no se encontro en ninguna carpeta")

def borrar(file_name, carpetas):
    try:
        archivo_encontrado = False
        for direcion in carpetas:
            if not os.path.exists(direcion):
                print(f"Aviso: No se encontro la carpeta {direcion}")
                continue
            for ruta, subcarpetas, archivos in os.walk(direcion):
                if file_name in archivos:
                    archivo_encontrado = True
                    file_path = os.path.join(ruta, file_name)
        
                    os.remove(file_path)
                    print("Archivo borrado exitosamente.")
                    return
        if not archivo_encontrado:
            print("Error: El archivo no se encontro en ninguna carpeta")
    except FileNotFoundError:
        print("Error: Archivo no encontrado")
        return
    except OSError as e:
        print(f"Error del sistema: {e}")
        return

overwrite_and_deleate()