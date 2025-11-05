import os

# Directorio raíz del proyecto (un nivel por encima de /config)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carpeta principal de datos
DATA_DIR = os.path.join(BASE_DIR, "data")

# Subcarpetas
OUTPUT_DIR = os.path.join(DATA_DIR, "output")
DB_DIR = os.path.join(DATA_DIR, "database")

# Rutas completas a recursos concretos
DB_PATH = os.path.join(DB_DIR, "etl_results.db")
VISUALIZATIONS_DIR = os.path.join(OUTPUT_DIR, "visualizations")

# API de extracción
EXTRACT_BASE_URL = "https://randomuser.me/api/"
NUM_USERS = 5000  # número de usuarios a extraer

# Configuración del loader
RESET_DB_ON_START = True  # si True, borra y recrea la base de datos al iniciar

# Configuración del visualizador
CLEAN_VISUALS_ON_START = True  # limpia la carpeta de plots al iniciar

# Crear las carpetas si no existen
for path in [OUTPUT_DIR, DB_DIR, VISUALIZATIONS_DIR]:
    os.makedirs(path, exist_ok=True)
