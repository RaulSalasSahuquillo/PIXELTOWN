"""
PIXELTOWN - Some ASCII drawings we could use in a future!
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

import pygame

def arrow(screen, font, pos_x, pos_y):
    ascii_art = [
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

    BLACK = (0, 0, 0)
    lines = ascii_art
    current_pos_y = pos_y
    line_height = font.get_height()

    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (pos_x, current_pos_y))
        current_pos_y += line_height

def bipo(screen, font, pos_x, pos_y):
    ascii_art = [
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
    BLACK = (0, 0, 0)
    lines = ascii_art
    current_pos_y = pos_y
    line_height = font.get_height()

    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (pos_x, current_pos_y))
        current_pos_y += line_height

def daemon(screen, font, pos_x, pos_y):
    ascii_art = [
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

    BLACK = (0, 0, 0)
    lines = ascii_art
    current_pos_y = pos_y
    line_height = font.get_height()

    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (pos_x, current_pos_y))
        current_pos_y += line_height
        
def person(screen, font, pos_x, pos_y):
    ascii_art = [
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

    BLACK = (0, 0, 0)
    lines = ascii_art
    current_pos_y = pos_y
    line_height = font.get_height()

    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (pos_x, current_pos_y))
        current_pos_y += line_height

def pingu(screen, font, pos_x, pos_y):
    ascii_art = """
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
    BLACK = (0, 0, 0)
    lines = ascii_art.strip().split('\n')
    current_pos_y = pos_y
    line_height = font.get_height()

    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (pos_x, current_pos_y))
        current_pos_y += line_height

def bipo_welcome(screen, font, pos_x, pos_y):
    ascii_art = [
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
    BLACK = (0, 0, 0)
    lines = ascii_art
    current_pos_y = pos_y
    line_height = font.get_height()

    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (pos_x, current_pos_y))
        current_pos_y += line_height