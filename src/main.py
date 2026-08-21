"""
PIXELTOWN - This is the launcher. It loads the terminal language selection screen.
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

from terminal import terminal_beginning
import text

if __name__ == '__main__':
    text.terminal_title()
    print("""
            PIXELTOWN  Copyright (C) 2026  Raúl Salas Sahuquillo, ENEI PROJECT
            This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
            This is free software, and you are welcome to redistribute it
            under certain conditions; type `show c' for details.
        """)
    terminal_beginning()
