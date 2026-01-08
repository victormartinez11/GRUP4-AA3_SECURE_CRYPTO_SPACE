import tkinter as tk
import tkinter.messagebox as msg

ventana_raiz = tk.tk()
ventana_raiz.withdraw()

def error_archivo_no_encontrado():
    msg.showerror(
        "Archivo no encontrado",
        "El archivo no existe o no se pudo localizar."
        parent = ventana_raiz
    )

def error_carpeta_no_encontrada(folder):
    msg.showerror(
        "Carpeta no encontrada",
        f"No se encontró la carpeta:\n{folder}"
        parent = ventana_raiz
    )

def error_permisos():
    msg.showerror(
        "Permisos insuficientes",
        "No tienes permisos para leer, modificar o borrar este archivo."
        parent = ventana_raiz
    )

def error_os(error):
    msg.showerror(
        "Error del sistema",
        f"Ocurrió un error del sistema:\n{error}"
        parent = ventana_raiz
    )

def error_archivo_corrupto():
    msg.showerror(
        "Archivo corrupto",
        "El archivo está dañado o no tiene un formato válido."
        parent = ventana_raiz
    )

def error_contrasena_incorrecta():
    msg.showerror(
        "Contraseña incorrecta",
        "La contraseña introducida no es correcta."
        parent = ventana_raiz
    )

def error_archivo_no_encontrado_en_carpetas():
    msg.showerror(
        "Archivo no encontrado",
        "El archivo no se encontró en ninguna de las carpetas indicadas."
        parent = ventana_raiz
    )

def error_opcion_invalida():
    msg.showerror(
        "Opción inválida",
        "La opción introducida no es válida."
        parent = ventana_raiz
    )

