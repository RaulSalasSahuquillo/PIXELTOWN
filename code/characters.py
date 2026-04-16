"""
PIXELTOWN - Some ASCII drawings we could use in a future!
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

import pygame

def flecha(pantalla, fuente, pos_x, pos_y):
    arte_ascii = [
        "      ████      ",
        "      ████      ",
        "      ████      ",
        "      ████      ",
        "      ████      ",
        "  ████████████  ",
        "    ████████    ",
        "     ██████     ",
        "      ████      ",
    ]

    NEGRO = (0, 0, 0)
    lineas = arte_ascii
    pos_y_actual = pos_y
    line_height = fuente.get_height()

    for linea in lineas:
        superficie_texto = fuente.render(linea, True, NEGRO)
        pantalla.blit(superficie_texto, (pos_x, pos_y_actual))
        pos_y_actual += line_height

def bipo(pantalla, fuente, pos_x, pos_y):
    arte_ascii = [
        "      ██████████",
        "    ██▒▒▒▒▒▒▒▒▒▒██",
        "   ██▒▒ ▒▒ ▒▒ ▒▒ ██",
        "  ██▒▒  ▒▒▒▒▒▒  ▒▒██",
        "  ██▒▒  █▀▀▀█  ▒▒██",
        "  ██▒▒  █ ● █  ▒▒██",
        "  ██▒▒  █▄▄▄█  ▒▒██",
        "   ██▒▒   ▄   ▒▒██",
        "    ██▒▒     ▒▒██",
        "      ██▒▒▒▒▒▒██",
        "      ██████████",
        "     ▒▒  ██  ▒▒",
        "    ██  █  █  ██"
    ]
    NEGRO = (0, 0, 0)
    lineas = arte_ascii
    pos_y_actual = pos_y
    line_height = fuente.get_height()

    for linea in lineas:
        superficie_texto = fuente.render(linea, True, NEGRO)
        pantalla.blit(superficie_texto, (pos_x, pos_y_actual))
        pos_y_actual += line_height

def daemon(pantalla, fuente, pos_x, pos_y):
    arte_ascii = [
        " ┌───────────────┐",
        " █ █ █ █ █ █ █ █ █",
        " █   ░ ░ ░ ░   █",
        " █ ░ ░ █ █ ░ ░ █",
        " █ ░ █  ●  █ ░ █",
        " █ ░ ░ █ █ ░ ░ █",
        " █   ░ ░ ░ ░   █",
        " █ █ █ █ █ █ █ █",
        "   █         █",
        "   █   ██    █",
        "    █      █"
    ]

    NEGRO = (0, 0, 0)
    lineas = arte_ascii
    pos_y_actual = pos_y
    line_height = fuente.get_height()

    for linea in lineas:
        superficie_texto = fuente.render(linea, True, NEGRO)
        pantalla.blit(superficie_texto, (pos_x, pos_y_actual))
        pos_y_actual += line_height
        
def persona(pantalla, fuente, pos_x, pos_y):
    arte_ascii = [
        "      ██████",
        "    ██      ██",
        "   ██  ●  ●  ██",
        "   ██   ▄▄   ██",
        "    ██      ██",
        "     ████████",
        "    ██ ████ ██",
        "   ██  ████  ██",
        "  ██         ██",
        " ██   ████    ██",
        "██   ██  ██    ██",
        "    ██    ██",
        "   ██      ██",
        "  ██        ██",
        " ██          ██"
    ]

    NEGRO = (0, 0, 0)
    lineas = arte_ascii
    pos_y_actual = pos_y
    line_height = fuente.get_height()

    for linea in lineas:
        superficie_texto = fuente.render(linea, True, NEGRO)
        pantalla.blit(superficie_texto, (pos_x, pos_y_actual))
        pos_y_actual += line_height

def pingu(pantalla, fuente, pos_x, pos_y):
    arte_ascii = """
                _________________________
               ( ¡BIENVENIDO A PIXELTOWN! )
                -------------------------
                    o
                o
         .--.
        |o_o |
        |:_/ |
       //   \ \
      (|     | )
     /'\_   _/`\
     \___)=(___/
"""
    NEGRO = (0, 0, 0)
    lineas = arte_ascii.strip().split('\n')
    pos_y_actual = pos_y
    line_height = fuente.get_height()

    for linea in lineas:
        superficie_texto = fuente.render(linea, True, NEGRO)
        pantalla.blit(superficie_texto, (pos_x, pos_y_actual))
        pos_y_actual += line_height

def bipobienvenida(pantalla, fuente, pos_x, pos_y):
    arte_ascii = [
        "                    _________________________",
        "                   ( ¡BIENVENIDO A PIXELTOWN! )",
        "                    -------------------------",
        "                       o",
        "                    o",
        "                o",
        "      ██████████",
        "    ██▒▒▒▒▒▒▒▒▒▒██",
        "   ██▒▒ ▒▒ ▒▒ ▒▒ ██",
        "  ██▒▒  ▒▒▒▒▒▒  ▒▒██",
        "  ██▒▒  █▀▀▀█  ▒▒██",
        "  ██▒▒  █ ● █  ▒▒██",
        "  ██▒▒  █▄▄▄█  ▒▒██",
        "   ██▒▒   ▄   ▒▒██",
        "    ██▒▒     ▒▒██",
        "      ██▒▒▒▒▒▒██",
        "      ██████████",
        "     ▒▒  ██  ▒▒",
        "    ██  █  █  ██"
    ]
    NEGRO = (0, 0, 0)
    lineas = arte_ascii
    pos_y_actual = pos_y
    line_height = fuente.get_height()

    for linea in lineas:
        superficie_texto = fuente.render(linea, True, NEGRO)
        pantalla.blit(superficie_texto, (pos_x, pos_y_actual))
        pos_y_actual += line_height