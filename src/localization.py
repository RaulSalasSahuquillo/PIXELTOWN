"""
PIXELTOWN - localization.py
Copyright (C) 2026  Raúl Salas Sahuquillo, ENEI PROJECT

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import json
import os

texts = {}

def load_language(lang_code):
    # Carga el archivo JSON del idioma seleccionado (es o en)
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
    # Devuelve el texto traducido según la clave. Si no existe, muestra la clave
    return texts.get(key, f"[{key} missing]")