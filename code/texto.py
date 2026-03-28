import pygame

def titulo(pantalla, fuente, pos_x, pos_y):
    arte_ascii = """
██████╗ ██╗██╗  ██╗███████╗██╗  ████████╗ ██████╗ ██╗    ██╗███╗   ██╗
██╔══██╗██║╚██╗██╔╝██╔════╝██║  ╚══██╔══╝██╔═══██╗██║    ██║████╗  ██║
██████╔╝██║ ╚███╔╝ █████╗  ██║     ██║   ██║   ██║██║ █╗ ██║██╔██╗ ██║
██╔═══╝ ██║ ██╔██╗ ██╔══╝  ██║     ██║   ██║   ██║██║███╗██║██║╚██╗██║
██║     ██║██╔╝ ██╗███████╗███████╗██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
"""

    NEGRO = (0, 0, 0)
    lineas = arte_ascii.strip().split('\n')
    
    pos_y_actual = pos_y
    line_height = fuente.get_height()

    for linea in lineas:
        superficie_texto = fuente.render(linea, True, NEGRO)
        pantalla.blit(superficie_texto, (pos_x, pos_y_actual))
        pos_y_actual += line_height

def informaciontexto1(pantalla, fuente, pos_x, pos_y):
    texto = """
¡Te damos la bienvenida a PIXELTOWN!
¡Hola, líder! Te damos la bienvenida al mundo de PIXELTOWN, un lugar donde tus 
decisiones darán forma a una nueva metrópolis desde sus cimientos. Tu aventura 
comienza aquí, con un puñado de recursos, un terreno virgen y un potencial 
ilimitado.

En PIXELTOWN, no eres solo un jugador, eres el alcalde, arquitecto y visionario.
Tu misión principal es transformar esta tierra prometedora en una ciudad 
próspera, vibrante y, sobre todo, feliz. Tendrás que gestionar cuidadosamente 
tu presupuesto, invertir en nuevas construcciones, atraer a nuevos ciudadanos y
asegurarte de que sus necesidades estén cubiertas. ¿Construirás una zona 
residencial tranquila, un bullicioso centro de negocios o un paraíso verde 
lleno de parques? Cada edificio que coloques y cada moneda que inviertas 
tendrá un impacto directo en el crecimiento y el alma de tu ciudad.
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
Un Vistazo al Futuro (Aviso Importante)
PIXELTOWN se encuentra en una fase muy temprana de su desarrollo (pre-alfa). 
Esto significa que lo que estás viendo es solo el esqueleto de un proyecto 
mucho más grande y ambicioso. Es como visitar el solar de un futuro rascacielos: 
ya se ven los cimientos, pero aún faltan las paredes, las ventanas y toda la 
magia que lo hará brillar. Actualmente, muchas de las características que 
tenemos planeadas (como sistemas económicos más complejos, eventos especiales, 
mayor variedad de edificios y personalización avanzada) todavía no están 
implementadas. Es muy probable que te encuentres con fallos, errores visuales 
o mecánicas incompletas. Te pedimos paciencia y te agradecemos enormemente
que formes parte de esta etapa tan crucial. Tu participación nos ayuda a 
probar las ideas fundamentales y nos motiva a seguir construyendo.

Sobre el Creador
PIXELTOWN es un proyecto personal desarrollado con gran pasión por Raúl Salas, 
bajo el nombre de su estudio independiente, ENEI PROJECT. Cada línea de código, 
cada píxel y cada idea nacen del deseo de crear un juego de gestión de ciudades
que sea a la vez relajante, desafiante y divertido. Esperamos que disfrutes de
este primer vistazo al universo de PIXELTOWN tanto como nosotros disfrutamos
dándole vida. ¡Ahora te invitamos a construir la ciudad de tus sueños!
    """
    
    NEGRO = (0, 0, 0)
    lineas = texto.strip().split('\n')
    
    pos_y_actual = pos_y
    line_height = fuente.get_height()

    for linea in lineas:
        superficie_texto = fuente.render(linea, True, NEGRO)
        pantalla.blit(superficie_texto, (pos_x, pos_y_actual))
        pos_y_actual += line_height