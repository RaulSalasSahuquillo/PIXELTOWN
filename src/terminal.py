"""
PIXELTOWN - This is the PIXELTOWN's terminal, in its early developement.
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
from localization import load_language, _

def terminalbeggining():
    print("""
██████╗ ██╗██╗  ██╗███████╗██╗  ████████╗ ██████╗ ██╗    ██╗███╗   ██╗
██╔══██╗██║╚██╗██╔╝██╔════╝██║  ╚══██╔══╝██╔═══██╗██║    ██║████╗  ██║
██████╔╝██║ ╚███╔╝ █████╗  ██║     ██║   ██║   ██║██║ █╗ ██║██╔██╗ ██║
██╔═══╝ ██║ ██╔██╗ ██╔══╝  ██║     ██║   ██║   ██║██║███╗██║██║╚██╗██║
██║     ██║██╔╝ ██╗███████╗███████╗██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
                   PIXELTOWN OFFICIAL TERMINAL.
          
          Welcome to the PIXELTOWN terminal!
""")
    
    while True:
        language = input("What language do you want to play the game?\n- Spanish (ES)\n- English (EN)\n> ")
        lang_clean = language.strip().lower()
        
        if lang_clean in ("es", "español", "spanish"):
            load_language("es")
            break
        elif lang_clean in ("en", "ingles", "english", "inglés"):
            load_language("en")
            break
        else:
            print("Invalid option. Please write 'ES' or 'EN'.\n")

    # Una vez cargado el idioma, importamos el main único y lanzamos el juego
    from game import main
    main()