# FITXERS I RUTES
USERS_FILE = "data/users.json"
CONFIG_FILE = "last_vault.txt"

# SEGURETAT I ENCRIPTACIÓ
SALT_SIZE = 16
KEY_SIZE = 32
BLOCK_SIZE = 16
ITERATIONS = 100000
CHUNK_SIZE = 4096  

# Colors Generals
COLOR_BG = "#0f111a"
COLOR_SIDEBAR = "#161925"
COLOR_CARD = "#212533"
COLOR_ACCENT = "#5c55e6"

# Colors de Text
COLOR_TEXT_PRIMARY = "#ffffff"
COLOR_TEXT_SECONDARY = "#a0a0a0"
COLOR_TEXT_DIM = "gray"

# Colors d'Estat
COLOR_GREEN = "#2ecc71"
COLOR_RED = "#c0392b"
COLOR_VISIBLE = "#2ed573"
COLOR_ENCRYPTED = "#ff4757"

# Colors de Botons
COLOR_BTN_NEW_FOLDER = "#27ae60"
COLOR_BTN_NEW_FOLDER_HOVER = "#2ecc71"

COLOR_BTN_IMPORT = "#3498db"
COLOR_BTN_IMPORT_HOVER = "#2980b9"

COLOR_BTN_EXIT = "#c0392b"
COLOR_BTN_EXIT_HOVER = "#e74c3c"

COLOR_BTN_ENCRYPT = "#27ae60" 
COLOR_BTN_ENCRYPT_HOVER = "#2ecc71"

COLOR_BTN_DECRYPT = "#c0392b" 
COLOR_BTN_DECRYPT_HOVER = "#e74c3c"

COLOR_BTN_HOVER_LIST = "#2f3542"

# Fonts
FONT_TITLE = ("Verdana", 20, "bold")
FONT_HEADER = ("Arial", 12, "bold")
FONT_NORMAL = ("Arial", 12)
FONT_SMALL_BOLD = ("Arial", 10, "bold")
FONT_PATH = ("Consolas", 14)
FONT_PATH_BOLD = ("Consolas", 14, "bold")

# Dimensions
SIDEBAR_WIDTH = 250

# CONFIGURACIÓ DE COLUMNES 

# Capçaleres de la llista d'arxius
DASHBOARD_HEADERS = ["", "NOMBRE", "FECHA", "TAMAÑO", "ESTADO"]

# Configuració visual de cada columna
DASHBOARD_COL_CONFIGS = [
    {"anchor": "center", "justify": "center", "padx": 5},      # Icona
    {"anchor": "w",      "justify": "left",   "padx": 5},      # Nom
    {"anchor": "w",      "justify": "left",   "padx": 5},      # Data
    {"anchor": "e",      "justify": "right",  "padx": 5},      # Mida
    {"anchor": "e",      "justify": "right",  "padx": (5, 10)} # Estat
]

# Configuració del Grid 
DASHBOARD_GRID_CONFIG = [
    {"index": 0, "weight": 0, "minsize": 40},
    {"index": 1, "weight": 2, "minsize": 70},
    {"index": 2, "weight": 1, "minsize": 120},
    {"index": 3, "weight": 0, "minsize": 80},
    {"index": 4, "weight": 0, "minsize": 100}
]
