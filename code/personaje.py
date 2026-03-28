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
    lineas = arte_ascii  # ← ¡Cambio aquí!
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
    lineas = arte_ascii  # ← ¡Cambio aquí!
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
    lineas = arte_ascii  # ← ¡Cambio aquí!
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
    lineas = arte_ascii  # ← ¡Cambio aquí!
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
    lineas = arte_ascii  # ← ¡Cambio aquí!
    pos_y_actual = pos_y
    line_height = fuente.get_height()

    for linea in lineas:
        superficie_texto = fuente.render(linea, True, NEGRO)
        pantalla.blit(superficie_texto, (pos_x, pos_y_actual))
        pos_y_actual += line_height