import json
import os

texts = {}

def load_language(lang_code):
    """Carga el archivo JSON del idioma seleccionado (es o en)"""
    global texts
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'locals', f'{lang_code}.json')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            texts = json.load(f)
    except FileNotFoundError:
        print(f"Error: File in {file_path} not fund. Loading 'es'.")
        if lang_code != 'es':
            load_language('es')

def _(key):
    """Devuelve el texto traducido según la clave. Si no existe, muestra la clave."""
    return texts.get(key, f"[{key} missing]")