# -*- coding: latin-1 -*-
import tkinter as tk
import tkinter.messagebox as msg

ventana_raiz = tk.tk()
ventana_raiz.withdraw()

def error_archivo_no_encontrado(archivo):
    msg.showerror(
        "Archiu no localitzat",
        f"L'archiu {archivo} no existeix o no s'ha pogut localizar."
        parent = ventana_raiz
    )

def error_carpeta_no_encontrada(folder):
    msg.showerror(
        "No s'ha trobat la carpeta",
        f"No se encontró la carpeta:\n{folder}"
        parent = ventana_raiz
    )

def error_permisos():
    msg.showerror(
        "Error de permisos",
        "No tens permisos per llegir, modificar o esborrar aquest archiu."
        parent = ventana_raiz
    )

def error_os():
    msg.showerror(
        "Error del sistema",
        "Ha ocurregut un error inesperat en el sistema amb 'os'"
        parent = ventana_raiz
    )

def error_archivo_corrupto():
    msg.showerror(
        "Archiu corrupte",
        "L'archivo está corromput o no té un format válid."
        parent = ventana_raiz
    )

def error_login():
    msg.showerror(
        "Error al iniciar sessió",
        "L'usuari o la contrasenya són incorrectes"
        parent = ventana_raiz
    )

def error_archivo_no_encontrado_en_carpetas():
    msg.showerror(
        "Archiu no trobat",
        "L'archiu no s'ha trobat en cap de les carpetes indicades."
        parent = ventana_raiz
    )

def error_opcion_invalida():
    msg.showerror(
        "Opció inválida",
        "L'opció introducida no es válid."
        parent = ventana_raiz
    )

def error_critic_sistema(e):
    msg.showerror(
        "Error crritic del sistema:"
        f"Ha ocurregut un error crític en el sistema: {e}"
        parent = ventana_raiz
    )

def value_error():
    msg.showerror(
        "Error de valor",
        f"S'ha produit un error de valor en les dades de l'usuari'",
        parent=ventana_raiz
    )

def error_sistema(e):
    msg.showerror(
        "Ha ocurregut un error inesperat"
        f"Detalls de l'error: {e}"
        parent=ventana_raiz
    )

def error_directori(path):
    msg.showerror(
        "Error:"
        f"La ruta {path} és una carpeta, no un fitxer"
        parent= ventana_raiz
        )