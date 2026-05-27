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
from text import titulo

def informaciontexto1(pantalla, fuente, pos_x, pos_y):
    texto = """
Welcome to PIXELTOWN!
Hello, leader! Welcome to the world of PIXELTOWN, a place where your 
decisions will shape a new metropolis from its foundations. Your adventure 
begins here, with a handful of resources, raw land, and limitless 
potential.

In PIXELTOWN, you are not just a player; you are the mayor, architect, and visionary.
Your main mission is to transform this promising land into a thriving, 
vibrant, and above all, happy city. You will have to carefully manage your 
budget, invest in new constructions, attract new citizens, and ensure their 
needs are met. Will you build a quiet residential area, a bustling business 
center, or a green paradise full of parks? Every building you place and 
every coin you invest will have a direct impact on the growth and soul of 
your city.
    """
    
    NEGRO = (0, 0, 0)
    lineas = texto.strip().split('\n')
    
    pos_y_actual = pos_y
    line_height = fuente.get_height()

    for linea in lineas:
        superficie_texto = fuente.render(linea, True, NEGRO)
        pantalla.blit(superficie_texto, (pos_x, pos_y_actual))
        pos_y_actual += line_height

def informaciontexto2(pantalla, fuente, pos_x, pos_y):
    texto = """
A Glimpse into the Future (Important Notice)
PIXELTOWN is in a very early stage of development (pre-alpha). This means 
that what you are seeing is only the skeleton of a much larger and more 
ambitious project. It's like visiting the construction site of a future 
skyscraper: you can already see the foundation, but the walls, windows, 
and all the magic that will make it shine are still missing. Currently, 
many of the features we have planned (such as more complex economic systems, 
special events, greater variety of buildings, and advanced customization) 
are not yet implemented. It is very likely that you will encounter bugs, 
visual glitches, or incomplete mechanics. We ask for your patience and 
thank you immensely for being part of this crucial phase. Your participation 
helps us test the fundamental ideas and motivates us to keep building.

About the Creator
PIXELTOWN is a personal project developed with great passion by Raúl Salas, 
under the name of his independent studio, ENEI PROJECT. Every line of code, 
every pixel, and every idea are born from the desire to create a city 
management game that is relaxing, challenging, and fun all at the same 
time. We hope you enjoy this first look at the PIXELTOWN universe as much 
as we enjoyed bringing it to life. Now, we invite you to build the city 
of your dreams!
    """
    
    NEGRO = (0, 0, 0)
    lineas = texto.strip().split('\n')
    
    pos_y_actual = pos_y
    line_height = fuente.get_height()

    for linea in lineas:
        superficie_texto = fuente.render(linea, True, NEGRO)
        pantalla.blit(superficie_texto, (pos_x, pos_y_actual))
        pos_y_actual += line_height
