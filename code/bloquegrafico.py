def rio():
    print("""
~~~~~~~~~~~~~~~~~~~~~~~~
~   ~   ~   ~   ~   ~
~   ~   ~   ~   ~   ~
~   ~   ~   ~   ~   ~
~~~~~~~~~~~~~~~~~~~~~~~~
          """)
    
def rio(pantalla, fuente, pos_x, pos_y):
    arte_ascii = [
        "~~~~~~~~~~~~~~~~~~~~~~~~",
        "~   ~   ~   ~   ~   ~",
        "~   ~   ~   ~   ~   ~",
        "~   ~   ~   ~   ~   ~",
        "~~~~~~~~~~~~~~~~~~~~~~~~",
    ]

    NEGRO = (0, 0, 0)
    lineas = arte_ascii  # ← ¡Cambio aquí!
    pos_y_actual = pos_y
    line_height = fuente.get_height()

    for linea in lineas:
        superficie_texto = fuente.render(linea, True, NEGRO)
        pantalla.blit(superficie_texto, (pos_x, pos_y_actual))
        pos_y_actual += line_height
    
def edificio1():
    print(r"""
      / \
     / _ \
    / | | \
   /  | |  \
  /___|_|___\
   |   _   |
   |  |_|  |
   |   _   |
   |  |_|  |
   |_______|
          """)