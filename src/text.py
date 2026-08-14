"""
PIXELTOWN - This is made for long characters and texts for Pygame and the terminal
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

def title(screen, font, pos_x, pos_y):
    ascii_art = """
██████╗ ██╗██╗  ██╗███████╗██╗  ████████╗ ██████╗ ██╗    ██╗███╗   ██╗
██╔══██╗██║╚██╗██╔╝██╔════╝██║  ╚══██╔══╝██╔═══██╗██║    ██║████╗  ██║
██████╔╝██║ ╚███╔╝ █████╗  ██║     ██║   ██║   ██║██║ █╗ ██║██╔██╗ ██║
██╔═══╝ ██║ ██╔██╗ ██╔══╝  ██║     ██║   ██║   ██║██║███╗██║██║╚██╗██║
██║     ██║██╔╝ ██╗███████╗███████╗██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
"""

    BLACK = (0, 0, 0)
    lines = ascii_art.strip().split('\n')
    
    current_pos_y = pos_y
    line_height = font.get_height()

    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (pos_x, current_pos_y))
        current_pos_y += line_height

def info_text_1(screen, font, pos_x, pos_y):
    from localization import _
    text = _("info_text_1")
    
    BLACK = (0, 0, 0)
    lines = text.strip().split('\n')
    
    current_pos_y = pos_y
    line_height = font.get_height()

    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (pos_x, current_pos_y))
        current_pos_y += line_height

def info_text_2(screen, font, pos_x, pos_y):
    from localization import _
    text = _("info_text_2")
    
    BLACK = (0, 0, 0)
    lines = text.strip().split('\n')
    
    current_pos_y = pos_y
    line_height = font.get_height()

    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (pos_x, current_pos_y))
        current_pos_y += line_height