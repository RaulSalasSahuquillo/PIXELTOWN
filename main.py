"""
PIXELTOWN - Root launcher and WebAssembly entry point.
Copyright (C) 2026  Raúl Salas Sahuquillo

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

# /// script
# dependencies = [
#  "pygame-ce",
# ]
# ///

import os
import sys
import asyncio

# Top-level pygame reference for pygbag dependency scanner
try:
    import pygame
except Exception:
    pass


# Ensure src/ directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Check for WebAssembly environment (pygbag / Emscripten)
IS_WEB = sys.platform in ("emscripten", "wasi")

# Pygbag requires an `async def main()` at module level,
# and `asyncio.run(main())` at the bottom.
# In the browser, asyncio.run() is intercepted by Pygbag's event loop.

async def main():
    if IS_WEB:
        print("[PIXELTOWN] Modo WebAssembly activo. Iniciando PIXELTOWN...")
        try:
            import platform
            import localization

            # Language detection: ?lang=en/es -> localStorage -> browser settings
            active_lang = "es"
            try:
                search_query = str(platform.window.location.search or "")
                cached_lang = str(platform.window.localStorage.getItem("pixeltown_lang") or "")
                if "lang=en" in search_query:
                    active_lang = "en"
                elif "lang=es" in search_query:
                    active_lang = "es"
                elif cached_lang in ("en", "es"):
                    active_lang = cached_lang
                else:
                    nav_lang = str(platform.window.navigator.language or "")
                    if nav_lang.lower().startswith("en"):
                        active_lang = "en"
            except Exception as lang_err:
                print(f"[PIXELTOWN] Aviso al detectar idioma web: {lang_err}")

            print(f"[PIXELTOWN] Configurando idioma web: {active_lang}")
            localization.load_language(active_lang)
            try:
                platform.window.localStorage.setItem("pixeltown_lang", active_lang)
            except Exception:
                pass

            import game
            await game.async_main(username="WebPlayer")
        except Exception as e:
            print(f"[PIXELTOWN] Error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

    else:
        from terminal import terminal_beginning
        import text
        text.terminal_title()
        print("""
            PIXELTOWN  Copyright (C) 2026  Raúl Salas Sahuquillo
            This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
            This is free software, and you are welcome to redistribute it
            under certain conditions; type `show c' for details.
        """)
        terminal_beginning()

# Pygbag intercepts this asyncio.run() call in the browser.
# On desktop, it runs normally.
asyncio.run(main())
