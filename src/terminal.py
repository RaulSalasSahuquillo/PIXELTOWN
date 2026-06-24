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
import sys
import hashlib
import getpass
from localization import load_language, _

def get_save_dir():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_path = os.path.join(base, "saves")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    return save_path

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def load_accounts():
    save_dir = get_save_dir()
    accounts_file = os.path.join(save_dir, "accounts.json")
    if not os.path.exists(accounts_file):
        return {}
    try:
        with open(accounts_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading accounts: {e}")
        return {}

def save_accounts(accounts):
    save_dir = get_save_dir()
    accounts_file = os.path.join(save_dir, "accounts.json")
    try:
        with open(accounts_file, "w", encoding="utf-8") as f:
            json.dump(accounts, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving accounts: {e}")
        return False

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

    logged_in_user = None
    accounts = load_accounts()

    while True:
        print(_("terminal_menu_title"))
        print(_("terminal_option_login"))
        print(_("terminal_option_register"))
        print(_("terminal_option_guest"))
        print(_("terminal_option_exit"))
        
        option = input(_("terminal_select_option")).strip()
        
        if option == "1":
            # Login
            username = input(_("terminal_enter_username")).strip()
            if not username:
                print(_("terminal_username_empty"))
                continue
            password = getpass.getpass(_("terminal_enter_password"))
            if not password:
                print(_("terminal_password_empty"))
                continue
            
            hashed = hash_password(password)
            if username in accounts and accounts[username] == hashed:
                print(_("terminal_login_success").format(username=username))
                logged_in_user = username
                break
            else:
                print(_("terminal_login_fail"))
                
        elif option == "2":
            # Register
            username = input(_("terminal_enter_username")).strip()
            if not username:
                print(_("terminal_username_empty"))
                continue
            if username in accounts:
                print(_("terminal_register_exists").format(username=username))
                continue
            password = getpass.getpass(_("terminal_enter_password"))
            if not password:
                print(_("terminal_password_empty"))
                continue
            
            accounts[username] = hash_password(password)
            if save_accounts(accounts):
                print(_("terminal_register_success").format(username=username))
                logged_in_user = username
                break
                
        elif option == "3":
            # Guest mode
            logged_in_user = None
            break
            
        elif option == "4":
            # Exit
            print("Goodbye / ¡Adiós!")
            sys.exit(0)
        else:
            print("Invalid option / Opción inválida.")

    # Una vez cargado el idioma, importamos el main único y lanzamos el juego
    from game import main
    main(username=logged_in_user)