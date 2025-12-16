import random
import os

def overwrite_and_deleate():
    try:
        print("Escribe el nombre del documento que quieres borrar.")
        file_name = input("> \n")

        carpetas = ["placeholder1", "placeholder2", "placeholder3"]

        while True:
            print("Atención! Este paso es ireversible y va a borrar el archivo.\n"
                  "Desea proceder con la operacion? (s/n)\n")

            confirmacion = input("> \n").lower()

            if confirmacion == "s":
                print("Borrando...\n")
                break
            elif confirmacion == "n":
                print("Operacion cancelada."
                      "Volviendo al menu principal...\n")
                return
            else:
                print("Introduce una opción valida.\n")
                continue

        for direcion in carpetas:
            if os.path.exists(direcion):
                for ruta, subcarpetas, archivos in os.walk(direcion):
                    if file_name in archivos:
                        file = os.path.join(ruta, file_name)

                        with open(file, "r") as f:
                            file_len = len(f.read())
                        with open(file, "w") as f:
                            for letter in range (file_len):
                                alphabet = "qwertyuiopasdfghjklñzxcvbnm"
                                f.write(random.choice(alphabet))
                        os.remove(file)
                        print("Archivo borrado.")
                        return
    except FileNotFoundError:
        print("Error: Archivo no encontrado."
              "Volviendo al menu principal...\n")
        return

overwrite_and_deleate()