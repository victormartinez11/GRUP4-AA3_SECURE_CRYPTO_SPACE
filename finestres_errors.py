import tkinter.messagebox as msg


def error_archivo_no_encontrado():
    msg.showerror(
        "Archivo no encontrado",
        "El archivo no existe o no se pudo localizar."
    )

def error_carpeta_no_encontrada(folder):
    msg.showerror(
        "Carpeta no encontrada",
        f"No se encontró la carpeta:\n{folder}"
    )

def error_permisos():
    msg.showerror(
        "Permisos insuficientes",
        "No tienes permisos para leer, modificar o borrar este archivo."
    )

def error_os(error):

def error_archivo_corrupto():

def error_contrasena_incorrecta():

def error_archivo_no_encontrado_en_carpetas():

def error_opcion_invalida():


