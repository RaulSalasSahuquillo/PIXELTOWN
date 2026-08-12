"""
PIXELTOWN - This is the main file, where all the actions of the game happen. Its purpose is to get shorter and divide it into multiple programs.
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

# IMPORTING LIBRARIES AND MODULES
import os
import pygame
import time
import sys
import json
from snake import run_snake
from tetris import run_tetris
from solarsystem import run_solarsystem
from pyvidplayer2 import Video
from characters import bipo, daemon, persona, flecha, bipobienvenida
from text import titulo, informaciontexto1, informaciontexto2
from localization import _

# PATH CONFIGURATION (Don't mess with these!)
# When running as a PyInstaller bundle, files are extracted to sys._MEIPASS
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_IMAGENES = os.path.join(BASE_DIR, "assets", "imagenes")
DIR_PIXELTOWN_OST = os.path.join(BASE_DIR, "assets", "PIXELTOWN_OST")
DIR_VISUAL = os.path.join(BASE_DIR, "assets", "visual")

# width and height of screen
w = 1200
h = 600

# Display scaling globals
pantalla_real = None
ancho_real = 1200
alto_real = 600

dinero = 10000  # Initial money (Don't spend it all in one place!)
poblacion = 10  # Initial population (Small, but it will grow)
edificios = []  # List of dicts: {"tipo": str, "pos": (x, y)}
felicidad = 50  # Initial happiness (We really need to cheer them up)
experiencia = 0  # Initial experience
dineroporhabitante = 1000 # Each inhabitant brings in 1000 money
tiempo = 1 # Time in days
deuda = 0 # Your debt
nivel = 1 # Your level
sound_on = 1 # Volume toggle (0 for off, 1 for on)
mouseDown = False # if mouse is down in the previous frame, it is True
alert = ["",0] # [message, timer]

# SESSION AND SAVES STATE
logged_in_username = None
ultimo_guardado_time = 0
mensaje_guardado = ""
datos_jugador = {"nombre_usuario": "", "nombre_ciudad": ""}

EDIFICIOS_CONFIG = {
    "casa": {
        "imagen": os.path.join(DIR_IMAGENES, "Casa.png"),
        "costo": 500,
        "experiencia": 100,
        "nombre_key": "simple_house"
    },
    "supermercado": {
        "imagen": os.path.join(DIR_IMAGENES, "supermercado.png"),
        "costo": 1500,
        "experiencia": 300,
        "nombre_key": "supermarket"
    },
    "tarraco": {
        "imagen": os.path.join(DIR_IMAGENES, "tarraco.png"),
        "costo": 10000,
        "experiencia": 900,
        "nombre_key": "tarraco"
    },
    "farola": {
        "imagen": os.path.join(DIR_IMAGENES, "farola.png"),
        "costo": 100,
        "experiencia": 25,
        "nombre_key": "streetlamp"
    },
    "my_town_my_rules": {
        "imagen": os.path.join(DIR_IMAGENES, "AdornoMYTOWNMYRULES.png"),
        "costo": 250,
        "experiencia": 100,
        "nombre_key": "my_town_my_rules"
    },
    "arbusto": {
        "imagen": os.path.join(DIR_IMAGENES, "arbusto.png"),
        "costo": 50,
        "experiencia": 10,
        "nombre_key": "bush"
    }
}

def obtener_precio_venta(tipo_edificio):
    return EDIFICIOS_CONFIG.get(tipo_edificio, {}).get("costo", 0) // 2

def obtener_experiencia_venta(tipo_edificio):
    return EDIFICIOS_CONFIG.get(tipo_edificio, {}).get("experiencia", 0) // 2

def obtener_nombre_edificio(tipo_edificio):
    key = EDIFICIOS_CONFIG.get(tipo_edificio, {}).get("nombre_key", "")
    if key:
        return _(key)
    return tipo_edificio.capitalize()

def get_save_dir():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_path = os.path.join(base, "saves")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    return save_path

def get_save_path(username):
    save_dir = get_save_dir()
    return os.path.join(save_dir, f"{username}_save.json")

def guardar_progreso(username):
    if not username:
        return False
    path = get_save_path(username)
    state = {
        "dinero": dinero,
        "poblacion": poblacion,
        "edificios": edificios,
        "felicidad": felicidad,
        "experiencia": experiencia,
        "dineroporhabitante": dineroporhabitante,
        "tiempo": tiempo,
        "deuda": deuda,
        "nivel": nivel,
        "datos_jugador": datos_jugador
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
        print(f"Progreso guardado para {username} en {path}")
        return True
    except Exception as e:
        print(f"Error al guardar progreso: {e}")
        return False

def cargar_progreso(username):
    global dinero, poblacion, edificios, felicidad, experiencia, dineroporhabitante, tiempo, deuda, nivel, datos_jugador
    if not username:
        return False
    path = get_save_path(username)
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
        
        dinero = state.get("dinero", 10000)
        poblacion = state.get("poblacion", 10)
        
        raw_edificios = state.get("edificios", [])
        edificios = []
        for ed in raw_edificios:
            pos = ed.get("pos", [0, 0])
            edificios.append({
                "tipo": ed.get("tipo", "casa"),
                "pos": (pos[0], pos[1])
            })
            
        felicidad = state.get("felicidad", 50)
        experiencia = state.get("experiencia", 0)
        dineroporhabitante = state.get("dineroporhabitante", 1000)
        tiempo = state.get("tiempo", 1)
        deuda = state.get("deuda", 0)
        nivel = state.get("nivel", 1)
        
        loaded_datos_jugador = state.get("datos_jugador", {})
        datos_jugador["nombre_usuario"] = loaded_datos_jugador.get("nombre_usuario", username)
        datos_jugador["nombre_ciudad"] = loaded_datos_jugador.get("nombre_ciudad", "PixelTown")
        
        print(f"Progreso cargado con éxito para {username} desde {path}")
        return True
    except Exception as e:
        print(f"Error al cargar progreso: {e}")
        return False

def sound_button(pantalla):
    global sound_on, mouseDown

    # load image and setup rect
    sound_imgs = [pygame.image.load(os.path.join(DIR_IMAGENES, "soundoff.png")), 
                    pygame.image.load(os.path.join(DIR_IMAGENES, "soundon.png"))]
    for img in range(len(sound_imgs)):
        sound_imgs[img] = pygame.transform.scale(sound_imgs[img], (50, 50))
    sound_rect = pygame.Rect(50, 500, 50, 50)

    # checking for sound button pressed
    if sound_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not mouseDown:
        sound_on = (sound_on + 1) % 2 # 1 -> 0, 0 -> 1
        if sound_on == 0:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(1)

    # draw the button
    pantalla.blit(sound_imgs[sound_on], (sound_rect.x, sound_rect.y))

def show_alert(pantalla):
    global alert, w, h

    if alert[1] > 0:
        text = pygame.font.Font(None, 16).render(alert[0], True, (0,0,0))
        textpos = text.get_rect(centerx=w/2, centery=h*0.9)
        pantalla.blit(text, textpos)

        alert[1] -= 1

# SCENE DEFINITION
def escena_intro(pantalla, reloj):
    try:
        ruta_video = os.path.join(DIR_VISUAL, 'intro.mp4')
        video = Video(ruta_video)
        
        # Same dimensions as the pygame screen
        dimensiones_pantalla = pantalla.get_size()
        video.resize(pantalla.get_size())

        while video.active:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    video.close()
                    return "salir"
            video.draw(pantalla, (0, 0), dimensiones_pantalla)
            pygame.display.flip()
            reloj.tick(video.frame_rate) 

        video.close()

    except FileNotFoundError:
        print("Error: No se encontró el archivo de video 'intro.mp4'. Saltando intro.")
    except Exception as e:
        print(f"Ocurrió un error al reproducir el video con pyvidplayer2: {e}. Saltando intro.")

    try:
        pygame.mixer.music.load(os.path.join(DIR_PIXELTOWN_OST, "anewbegining.mp3"))
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"No se pudo cargar el archivo de música: {e}")

    return "menu"

def escena_menu(pantalla, fuente_titulo, fuente_boton, eventos): # menu_scene
    global w, h
    boton_jugar = pygame.Rect(900, 500, 200, 50) # play button

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_jugar.collidepoint(evento.pos):
                print("Cambiando a la escena del juego...")
                return "jugando"

    pantalla.fill((220, 220, 255))  # (screen) Light lilac background (Soothing, right? It took me hours to find the perfect colour. Thank me later!)    
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'PIXELTOWN_portada.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (w, h))
        pantalla.blit(player_image_scaled, (0, 0))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")

    # Drawing the PLAY button
    pos_raton = pygame.mouse.get_pos()
    color_boton = (100, 180, 255) if boton_jugar.collidepoint(pos_raton) else (0, 128, 255)
    pygame.draw.rect(pantalla, color_boton, boton_jugar)
    texto_surf = fuente_boton.render(_("play"), True, (0, 0, 0))
    texto_rect = texto_surf.get_rect(center=boton_jugar.center)
    pantalla.blit(texto_surf, texto_rect)

    sound_button(pantalla)

    return "menu"


def escena_juego(pantalla, fuente_boton, eventos, fuente_titulo):
    boton_volver = pygame.Rect(50, 500, 250, 50)
    boton_continuar = pygame.Rect(900, 500, 250, 50)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_volver.collidepoint(evento.pos):
                print("Volviendo al menú...")
                return "menu"
            elif boton_continuar.collidepoint(evento.pos):
                print("Continuando a la escena de pregunta...")
                return "preguntando"

    pantalla.fill((200, 255, 200))  # Light green background
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'BIENVENIDO.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (400, 400))
        pantalla.blit(player_image_scaled, (400, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")

    pos_raton = pygame.mouse.get_pos()
    color_volver = (255, 100, 100) if boton_volver.collidepoint(pos_raton) else (200, 50, 50)
    color_continuar = (100, 180, 255) if boton_continuar.collidepoint(pos_raton) else (0, 128, 255)

    pygame.draw.rect(pantalla, color_volver, boton_volver)
    texto_surf_volver = fuente_boton.render(_("back_to_menu"), True, (255, 255, 255))
    texto_rect_volver = texto_surf_volver.get_rect(center=boton_volver.center)
    pantalla.blit(texto_surf_volver, texto_rect_volver)

    pygame.draw.rect(pantalla, color_continuar, boton_continuar)
    texto_surf_continuar = fuente_boton.render(_("continue"), True, (255, 255, 255))
    texto_rect_continuar = texto_surf_continuar.get_rect(center=boton_continuar.center)
    pantalla.blit(texto_surf_continuar, texto_rect_continuar)

    return "jugando"


def pregunta(pantalla, fuente_titulo, fuente_normal, eventos, caja_texto_estado, datos_jugador):
    input_box = pygame.Rect(pantalla.get_width() // 2 - 200, 300, 400, 40)
    color_inactivo = pygame.Color('lightskyblue3')
    color_activo = pygame.Color('dodgerblue2')

    texto_usuario = caja_texto_estado['texto']
    activo = caja_texto_estado['activo']
    color = color_activo if activo else color_inactivo

    boton_volver = pygame.Rect(pantalla.get_width() // 2 - 125, 500, 250, 50)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver.collidepoint(evento.pos):
                return "menu"
            activo = input_box.collidepoint(evento.pos)

        if activo and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                print(f"Respuesta enviada: {texto_usuario}")
                datos_jugador['nombre_usuario'] = texto_usuario
                caja_texto_estado['texto'] = ""
                texto_usuario = ""
                activo = False
                return "preguntando2"
            elif evento.key == pygame.K_BACKSPACE:
                texto_usuario = texto_usuario[:-1]
            else:
                texto_usuario += evento.unicode

    caja_texto_estado['texto'] = texto_usuario
    caja_texto_estado['activo'] = activo

    pantalla.fill((220, 220, 255))
    texto_pregunta_surf = fuente_titulo.render(_("what_is_your_name"), True, (0, 0, 0))
    texto_pregunta_rect = texto_pregunta_surf.get_rect(center=(pantalla.get_width() // 2, 200))
    pantalla.blit(texto_pregunta_surf, texto_pregunta_rect)

    texto_surf = fuente_normal.render(texto_usuario, True, (0, 0, 0))
    input_box.w = max(400, texto_surf.get_width() + 20)
    pygame.draw.rect(pantalla, color, input_box, 2)
    pantalla.blit(texto_surf, (input_box.x + 10, input_box.y + 10))

    pos_raton = pygame.mouse.get_pos()
    color_boton = (255, 100, 100) if boton_volver.collidepoint(pos_raton) else (200, 50, 50)
    pygame.draw.rect(pantalla, color_boton, boton_volver)
    texto_surf_boton = fuente_normal.render(_("back_to_menu"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_volver.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)

    return "preguntando"


def pregunta2(pantalla, fuente_titulo, fuente_normal, eventos, caja_texto_estado, datos_jugador):
    global logged_in_username
    input_box = pygame.Rect(pantalla.get_width() // 2 - 200, 300, 400, 40)
    color_inactivo = pygame.Color('lightskyblue3')
    color_activo = pygame.Color('dodgerblue2')

    texto_usuario = caja_texto_estado['texto']
    activo = caja_texto_estado['activo']
    color = color_activo if activo else color_inactivo

    boton_volver = pygame.Rect(pantalla.get_width() // 2 - 125, 500, 250, 50)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver.collidepoint(evento.pos):
                return "menu"
            activo = input_box.collidepoint(evento.pos)

        if activo and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                print(f"Respuesta enviada: {texto_usuario}")
                datos_jugador['nombre_ciudad'] = texto_usuario
                texto_usuario = ""
                activo = False
                if logged_in_username:
                    guardar_progreso(logged_in_username)
                return "cargamapa"
            elif evento.key == pygame.K_BACKSPACE:
                texto_usuario = texto_usuario[:-1]
            else:
                texto_usuario += evento.unicode

    caja_texto_estado['texto'] = texto_usuario
    caja_texto_estado['activo'] = activo

    pantalla.fill((220, 220, 255))
    nombre_usuario = datos_jugador.get('nombre_usuario', 'Tú')
    texto_pregunta_surf = fuente_titulo.render(
        _("welcome_city_name").format(username=nombre_usuario), True, (0, 0, 0))
    texto_pregunta_rect = texto_pregunta_surf.get_rect(center=(pantalla.get_width() // 2, 200))
    pantalla.blit(texto_pregunta_surf, texto_pregunta_rect)

    texto_surf = fuente_normal.render(texto_usuario, True, (0, 0, 0))
    input_box.w = max(400, texto_surf.get_width() + 20)
    pygame.draw.rect(pantalla, color, input_box, 2)
    pantalla.blit(texto_surf, (input_box.x + 10, input_box.y + 10))

    pos_raton = pygame.mouse.get_pos()
    color_boton = (255, 100, 100) if boton_volver.collidepoint(pos_raton) else (200, 50, 50)
    pygame.draw.rect(pantalla, color_boton, boton_volver)
    texto_surf_boton = fuente_normal.render(_("back_to_menu"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_volver.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)

    return "preguntando2"


def cargamapa(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    pygame.mixer.music.stop()
    pantalla.fill((220, 220, 255))  # Light lilac background (Soothing, right?)

    boton_vermapa = pygame.Rect(pantalla.get_width() // 2 - 125, 500, 250, 50)

    texto_titulo_surf = fuente_titulo.render(_("loading_map"), True, (0, 0, 0))
    texto_titulo_rect = texto_titulo_surf.get_rect(center=(pantalla.get_width() // 2, 200))
    pantalla.blit(texto_titulo_surf, texto_titulo_rect)

    pos_raton = pygame.mouse.get_pos()
    color_boton = (255, 100, 100) if boton_vermapa.collidepoint(pos_raton) else (200, 50, 50)
    pygame.draw.rect(pantalla, color_boton, boton_vermapa)
    texto_surf_boton = fuente_normal.render(_("back_to_menu"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_vermapa.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"

    pygame.display.flip()
    return "mapainicial"


def mostrar_texto(pantalla, fuente, texto, x, y, color=(0, 0, 0), line_spacing=5):
    lines = texto.split("\n")
    current_y = y
    for line in lines:
        # Render the actual lines
        text_surface = fuente.render(line, True, color)
        # Draw it on the screen
        pantalla.blit(text_surface, (x, current_y))
        current_y += text_surface.get_height() + line_spacing


def mapainicial(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal, datos_jugador):
    global nivel, experiencia, logged_in_username, ultimo_guardado_time, mensaje_guardado, alert
    pantalla.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    boton_acciones = pygame.Rect(900, 500, 250, 50)
    boton_guardar = pygame.Rect(125, 500, 250, 50)
    pos_raton = pygame.mouse.get_pos()
    
    if experiencia >= 100 and nivel < 5:
        experiencia = 0
        nivel += 1
    elif experiencia >= 1000 and (nivel >= 5 and nivel < 10):
        experiencia = 0
        nivel += 1
    color_boton = (255, 100, 100) if boton_acciones.collidepoint(pos_raton) else (200, 50, 50)
    pygame.draw.rect(pantalla, color_boton, boton_acciones)
    texto_surf_boton = fuente_normal.render(_("actions"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_acciones.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)

    # Save button drawing
    if logged_in_username:
        color_boton_guardar = (100, 200, 100) if boton_guardar.collidepoint(pos_raton) else (50, 150, 50)
        texto_guardar = _("save_progress")
    else:
        color_boton_guardar = (180, 180, 180)
        texto_guardar = _("guest_cannot_save")
        
    pygame.draw.rect(pantalla, color_boton_guardar, boton_guardar)
    texto_surf_guardar = fuente_normal.render(texto_guardar, True, (255, 255, 255))
    texto_rect_guardar = texto_surf_guardar.get_rect(center=boton_guardar.center)
    pantalla.blit(texto_surf_guardar, texto_rect_guardar)

    # Success/Warning message
    if time.time() - ultimo_guardado_time < 3:
        color_texto = (0, 128, 0) if logged_in_username else (200, 0, 0)
        mostrar_texto(pantalla, fuente_normal, mensaje_guardado, 50, 460, color=color_texto)

    nombre_usuario = datos_jugador.get('nombre_usuario', 'Tú')
    nombre_ciudad = datos_jugador.get('nombre_ciudad', 'PixelTown')
    boton_verdatos = pygame.Rect(pantalla.get_width() - 170, 15, 150, 35)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (255, 100, 100) if boton_verdatos.collidepoint(pos_raton) else (200, 50, 50)
    pygame.draw.rect(pantalla, color_boton, boton_verdatos)
    texto_surf_boton = fuente_normal.render(_("view_stats"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_verdatos.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    if boton_verdatos.collidepoint(pos_raton):
        mostrar_texto(pantalla, fuente_normal, _("leader").format(username=nombre_usuario), 10, 10)
        mostrar_texto(pantalla, fuente_normal, _("city").format(cityname=nombre_ciudad), 10, 50)
        mostrar_texto(pantalla, fuente_normal, _("money").format(money=dinero), 10, 90)
        mostrar_texto(pantalla, fuente_normal, _("population").format(population=poblacion), 10, 130)
        mostrar_texto(pantalla, fuente_normal, _("happiness").format(happiness=felicidad), 10, 170)
        mostrar_texto(pantalla, fuente_normal, _("buildings").format(count=len(edificios)), 10, 210)
        mostrar_texto(pantalla, fuente_normal, _("experience").format(experience=experiencia), 10, 250)
        mostrar_texto(pantalla, fuente_normal, _("debt").format(debt=deuda), 10, 290)
        mostrar_texto(pantalla, fuente_normal, _("level").format(level=nivel), 10, 330)

    try:
        casa_img = pygame.transform.scale(pygame.image.load(os.path.join(DIR_IMAGENES, 'Casa.png')).convert_alpha(), (64, 64))
        supermercado_img = pygame.transform.scale(pygame.image.load(os.path.join(DIR_IMAGENES, 'supermercado.png')).convert_alpha(), (64, 64))
        tarraco_img = pygame.transform.scale(pygame.image.load(os.path.join(DIR_IMAGENES, 'tarraco.png')).convert_alpha(), (64, 64))
        farola_img = pygame.transform.scale(pygame.image.load(os.path.join(DIR_IMAGENES, 'farola.png')).convert_alpha(), (64, 64))
        mytown_img = pygame.transform.scale(pygame.image.load(os.path.join(DIR_IMAGENES, 'AdornoMYTOWNMYRULES.png')).convert_alpha(), (64, 64))
        arbusto_img = pygame.transform.scale(pygame.image.load(os.path.join(DIR_IMAGENES, 'arbusto.png')).convert_alpha(), (64, 64))
    except pygame.error as e:
        print(f"Error al cargar imágenes de edificios: {e}")
        return "menu"  # Exit to menu if images are not found (I hope you didn't delete them!)

    # Image dictionary
    imagenes_edificios = {
        "casa": casa_img,
        "supermercado": supermercado_img,
        "tarraco": tarraco_img,
        "farola": farola_img,
        "my_town_my_rules": mytown_img,
        "arbusto": arbusto_img
    }
    # Draw existing buildings (The real estate)
    for edificio in edificios:
        tipo = edificio["tipo"]
        pos = edificio["pos"]
        if tipo in imagenes_edificios:
            pantalla.blit(imagenes_edificios[tipo], pos)
        else:
            pygame.draw.rect(pantalla, (255, 0, 0), (*pos, 64, 64), 2)

    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'rio.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (450, 200))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    if felicidad < 10:
        print(_("citizens_unhappy"))
        print(_("coup_started"))
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(os.path.join(DIR_PIXELTOWN_OST, "efectodestruccion.mp3"))
                pygame.mixer.music.play()
        except pygame.error as e:
            print(f"No se pudo cargar el archivo de música: {e}")
        finally:
            print(_("game_over"))
            return "gameover"
    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_acciones.collidepoint(evento.pos):
                print("Cambiando a la escena de acciones...")
                return "acciones"
            if boton_guardar.collidepoint(evento.pos):
                if logged_in_username:
                    if guardar_progreso(logged_in_username):
                        ultimo_guardado_time = time.time()
                        mensaje_guardado = _("progress_saved")
                else:
                    ultimo_guardado_time = time.time()
                    mensaje_guardado = _("guest_cannot_save")
    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(os.path.join(DIR_PIXELTOWN_OST, "Aldea_soundtrack.mp3"))
            pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"No se pudo cargar el archivo de música: {e}")

    sound_button(pantalla)
    
    return "mapainicial"


def acciones(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    pantalla.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    mostrar_texto(pantalla, fuente_titulo, _("actions"), 10, 10)

    # BUY (Time to spend)
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'tienda.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (250, 250))
        pantalla.blit(player_image_scaled, (60, 30))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_comprar = pygame.Rect(60, 260, 250, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_comprar.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_comprar)
    texto_surf_boton = fuente_normal.render(_("buy"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_comprar.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_comprar.collidepoint(evento.pos):
                print("Cambiando a la escena de tienda...")
                return "tienda"

    # SELL
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'ganar_dinero.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (250, 250))
        pantalla.blit(player_image_scaled, (460, 30))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_ganar_dinero = pygame.Rect(460, 260, 250, 50)
    color_boton = (200, 200, 100) if boton_ganar_dinero.collidepoint(pos_raton) else (200, 200, 50) # R, G, B
    pygame.draw.rect(pantalla, color_boton, boton_ganar_dinero)
    texto_surf_boton = fuente_normal.render(_("invoice"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_ganar_dinero.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_ganar_dinero.collidepoint(evento.pos):
                print("Cambiando a la escena facturar...")
                return "facturar"
            
    # MINIGAMES
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'minijuegos.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (250, 250))
        pantalla.blit(player_image_scaled, (40, 300))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_minijuegos = pygame.Rect(60, 580, 250, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_minijuegos.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_minijuegos)
    texto_surf_boton = fuente_normal.render(_("minigames"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_minijuegos.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_minijuegos.collidepoint(evento.pos):
                print("Cambiando a la escena de minijuegos")
                return "minijuegos"

    # INFORMATION
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'info.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (250, 250))
        pantalla.blit(player_image_scaled, (860, 30))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_info = pygame.Rect(860, 260, 250, 50)
    color_boton = (200, 200, 100) if boton_info.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_info)
    texto_surf_boton = fuente_normal.render(_("information"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_info.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_info.collidepoint(evento.pos):
                print("Cambiando a la escena de información...")
                return "info"

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"

    pygame.display.flip()
    return "acciones"

def snakegame(pantalla):
    global _minigame_active, pantalla_real, ancho_real, alto_real
    _minigame_active = True
    try:
        result = run_snake(pantalla)
    finally:
        _minigame_active = False
        # Restore the PIXELTOWN virtual-surface display system
        pantalla_real = pygame.display._original_set_mode((ancho_real, alto_real), pygame.RESIZABLE)
        pygame.display.set_caption("PIXELTOWN")
    return result

def tetrisgame(pantalla):
    global _minigame_active, pantalla_real, ancho_real, alto_real
    _minigame_active = True
    try:
        result = run_tetris(pantalla)
    finally:
        _minigame_active = False
        pantalla_real = pygame.display._original_set_mode((ancho_real, alto_real), pygame.RESIZABLE)
        pygame.display.set_caption("PIXELTOWN")
    return result

def solarsystem(pantalla):
    global _minigame_active, pantalla_real, ancho_real, alto_real
    _minigame_active = True
    try:
        result = run_solarsystem(pantalla)
    finally:
        _minigame_active = False
        pantalla_real = pygame.display._original_set_mode((ancho_real, alto_real), pygame.RESIZABLE)
        pygame.display.set_caption("PIXELTOWN")
    return result

def tienda(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    pantalla.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    # CONSTRUCTION (Bob the builder vibes)
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'construccion.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (40, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_construccion = pygame.Rect(60, 380, 250, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_construccion.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_construccion)
    texto_surf_boton = fuente_normal.render(_("construction"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_construccion.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_construccion.collidepoint(evento.pos):
                print("Cambiando a la escena de construcción...")
                return "construccion"

    # PRODUCTS
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'productos.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (440, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_productos = pygame.Rect(460, 380, 250, 50)
    color_boton = (200, 200, 100) if boton_productos.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_productos)
    texto_surf_boton = fuente_normal.render(_("products"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_productos.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_productos.collidepoint(evento.pos):
                print("Cambiando a la escena de productos...")
                return "productos"

    # DECORATIONS (Make it pretty)
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'adorno.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (840, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_adorno = pygame.Rect(860, 380, 250, 50)
    color_boton = (200, 200, 100) if boton_adorno.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_adorno)
    texto_surf_boton = fuente_normal.render(_("decorations"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_adorno.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_adorno.collidepoint(evento.pos):
                print("Cambiando a la escena de adornos...")
                return "adorno"

    return "tienda"

def adorno(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    pantalla.fill((255, 255, 255))  # White background (Maybe a bit too bright?)

    # MYTOWNMYRULES button
    boton_mytownmyrules = pygame.Rect(410, 350, 250, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_mytownmyrules.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_mytownmyrules)
    texto_surf_boton = fuente_normal.render(_("my_town_my_rules"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_mytownmyrules.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP and boton_mytownmyrules.collidepoint(evento.pos):
            return "colocando_edificio", "my_town_my_rules"
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'AdornoMYTOWNMYRULES.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (400, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen 'AdornoMYTOWNMYRULES.png': {e}")


    boton_farola = pygame.Rect(10, 350, 250, 50)
    color_boton = (200, 200, 100) if boton_farola.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_farola)
    texto_surf_boton = fuente_normal.render(_("streetlamp"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_farola.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP and boton_farola.collidepoint(evento.pos):
            return "colocando_edificio", "farola"
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'farola.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (30, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen 'farola.png': {e}")

    # Bush
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'arbusto.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (770, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen 'arbusto.png': {e}")

    boton_arbusto = pygame.Rect(810, 350, 250, 50)
    color_boton = (200, 200, 100) if boton_arbusto.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_arbusto)
    texto_surf_boton = fuente_normal.render(_("bush"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_arbusto.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP and boton_arbusto.collidepoint(evento.pos):
            return "colocando_edificio", "arbusto"
    return "adorno"

def info(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    pantalla.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    informaciontexto1(pantalla, fuente_titulo, 10, 10)

    boton_siguiente = pygame.Rect(900, 500, 250, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_siguiente.collidepoint(pos_raton) else (97, 175, 14)
    pygame.draw.rect(pantalla, color_boton, boton_siguiente)
    texto_surf_boton = fuente_normal.render(_("next"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_siguiente.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_siguiente.collidepoint(evento.pos):
                print("Cambiando a la escena infodos...")
                return "infodos"

    boton_volver = pygame.Rect(10, 500, 250, 50)
    color_boton = (200, 200, 100) if boton_volver.collidepoint(pos_raton) else (97, 175, 14)
    pygame.draw.rect(pantalla, color_boton, boton_volver)
    texto_surf_boton = fuente_normal.render(_("back"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_volver.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_volver.collidepoint(evento.pos):
                print("Cambiando a mapa inicial")
                return "mapainicial"

    return "info"


def infodos(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    global mouseDown
    pantalla.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    informaciontexto2(pantalla, fuente_titulo, 10, 10)

    # exit button
    exit_button = pygame.Rect(1130, 20, 50, 50)
    pygame.draw.rect(pantalla, (255, 100, 100), exit_button)

    text = pygame.font.Font(None, 30).render("X", True, (255,255,255))

    if exit_button.collidepoint(pygame.mouse.get_pos()):
        text = pygame.font.Font(None, 38).render("X", True, (255,255,255))

        if pygame.mouse.get_pressed()[0] and not mouseDown:
            return "mapainicial"
        
    textpos = text.get_rect(centerx=exit_button.centerx, centery=exit_button.centery)
    pantalla.blit(text, textpos)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
    return "infodos"


def productos(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    global dinero, felicidad, experiencia
    
    # HAND SOAP (Clean hands are happy hands)
    pantalla.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    boton_comprar = pygame.Rect(100, 390, 310, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_comprar.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_comprar)
    texto_surf_boton = fuente_normal.render(_("hand_soap"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_comprar.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_comprar.collidepoint(evento.pos):
                print("Comprando producto...")
                if dinero >= 250:
                    dinero -= 250
                    felicidad += 5
                    experiencia += 10
                    print(_("purchase_success"))
                    return "mapainicial"
                else:
                    print(_("insufficient_money"))
                    return "mapainicial"
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'lovyc.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (500, 300))
        pantalla.blit(player_image_scaled, (10, 100))
    except pygame.error:
        print("Error cargando imagen")
        pass

    # FACE MASK IMAGE
    boton_mascarilla = pygame.Rect(700, 390, 310, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_mascarilla.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_mascarilla)
    texto_surf_boton = fuente_normal.render(_("face_mask"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_mascarilla.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_mascarilla.collidepoint(evento.pos):
                print("Comprando producto...")
                if dinero >= 150:
                    dinero -= 150
                    felicidad += 5
                    experiencia += 10
                    print(_("purchase_success"))
                    return "mapainicial"
                else:
                    print(_("insufficient_money"))
                    return "mapainicial"
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'lovyc_mascarilla.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (700, 100))
    except pygame.error:
        pass
    
    boton_siguiente = pygame.Rect(900, 500, 250, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_siguiente.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_siguiente)
    texto_surf_boton = fuente_normal.render(_("next"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_siguiente.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_siguiente.collidepoint(evento.pos):
                return "productos2"
    
    return "productos"

def productos2(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    global dinero, felicidad, experiencia
    pantalla.fill((255, 255, 255))
    
    # SHAMPOO IMAGE
    boton_champu = pygame.Rect(700, 390, 310, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_champu.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_champu)
    texto_surf_boton = fuente_normal.render(_("shampoo"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_champu.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_champu.collidepoint(evento.pos):
                print("Comprando producto...")
                if dinero >= 200:
                    dinero -= 200
                    felicidad += 10
                    experiencia += 10
                    print(_("purchase_success"))
                    return "mapainicial"
                else:
                    print(_("insufficient_money"))
                    return "mapainicial"
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'lovyc_champú.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (700, 100))
    except pygame.error:
        pass

    # WIPES IMAGE
    boton_comprar = pygame.Rect(100, 390, 310, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_comprar.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_comprar)
    texto_surf_boton = fuente_normal.render(_("wipes"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_comprar.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_comprar.collidepoint(evento.pos):
                print("Comprando producto...")
                if dinero >= 100:
                    dinero -= 100
                    felicidad += 5
                    experiencia += 10
                    print(_("purchase_success"))
                    return "mapainicial"
                else:
                    print(_("insufficient_money"))
                    return "mapainicial"
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'lovyc_toallitas.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (500, 300))
        pantalla.blit(player_image_scaled, (10, 100))
    except pygame.error:
        pass
    
    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
    return "productos2"

def construccion(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    pantalla.fill((255, 255, 255))  # White background (Maybe a bit too bright?)

    # House button
    boton_casasimple = pygame.Rect(10, 350, 250, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_casasimple.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_casasimple)
    texto_surf_boton = fuente_normal.render(_("simple_house"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_casasimple.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP and boton_casasimple.collidepoint(evento.pos):
            return "colocando_edificio", "casa"

    # Image and button for supermarket
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'supermercado.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (400, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen 'supermercado.png': {e}")

    boton_store = pygame.Rect(410, 350, 250, 50)
    color_boton = (200, 200, 100) if boton_store.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_store)
    texto_surf_boton = fuente_normal.render(_("supermarket"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_store.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP and boton_store.collidepoint(evento.pos):
            return "colocando_edificio", "supermercado"

    # House image (decorative)
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'Casa.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (30, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen 'Casa.png': {e}")

    # Tarraco Import Export 
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'tarraco.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (770, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen 'tarraco.png': {e}")

    boton_tarraco = pygame.Rect(810, 350, 250, 50)
    color_boton = (200, 200, 100) if boton_tarraco.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_tarraco)
    texto_surf_boton = fuente_normal.render(_("tarraco"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_tarraco.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP and boton_tarraco.collidepoint(evento.pos):
            return "colocando_edificio", "tarraco"

    return "construccion"


def escena_colocacion(pantalla, eventos, fuente_normal, tipo_edificio):
    global edificios, dinero, experiencia, alert

    if tipo_edificio not in EDIFICIOS_CONFIG:
        print(f"Error: Tipo de edificio '{tipo_edificio}' desconocido.")
        return "construccion"

    config = EDIFICIOS_CONFIG[tipo_edificio]
    ruta_imagen = config["imagen"]
    costo = config["costo"]
    recompensa_exp = config["experiencia"]

    # background/map
    pantalla.fill((255, 255, 255))
    try:
        rio_img = pygame.image.load(os.path.join(DIR_IMAGENES, 'rio.png')).convert_alpha()
        pantalla.blit(pygame.transform.scale(rio_img, (300, 300)), (450, 200))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")

    # River zone — buildings cannot be placed here
    RIO_RECT = pygame.Rect(488, 223, 250, 265)

    mostrar_texto(pantalla, fuente_normal, _("money").format(money=dinero), 10, 10)
    mostrar_texto(pantalla, fuente_normal, _("buildings_short").format(count=len(edificios)), 10, 40)
    mostrar_texto(pantalla, fuente_normal, _("experience").format(experience=experiencia), 10, 70)
    mostrar_texto(pantalla, fuente_normal, _("debt").format(debt=deuda), 10, 100)
    mostrar_texto(pantalla, fuente_normal, _("level").format(level=nivel), 10, 130)


    # load sprites
    try:
        casa_img = pygame.transform.scale(pygame.image.load(os.path.join(DIR_IMAGENES, 'Casa.png')).convert_alpha(), (64, 64))
        supermercado_img = pygame.transform.scale(pygame.image.load(os.path.join(DIR_IMAGENES, 'supermercado.png')).convert_alpha(), (64, 64))
        tarraco_img = pygame.transform.scale(pygame.image.load(os.path.join(DIR_IMAGENES, 'tarraco.png')).convert_alpha(), (64, 64))
        farola_img = pygame.transform.scale(pygame.image.load(os.path.join(DIR_IMAGENES, 'farola.png')).convert_alpha(), (64, 64))
        mytown_img = pygame.transform.scale(pygame.image.load(os.path.join(DIR_IMAGENES, 'AdornoMYTOWNMYRULES.png')).convert_alpha(), (64, 64))
        arbusto_img = pygame.transform.scale(pygame.image.load(os.path.join(DIR_IMAGENES, 'arbusto.png')).convert_alpha(), (64, 64))
    except pygame.error as e:
        print(f"Error cargando imágenes de edificios: {e}")
        return "construccion"

    imagenes_edificios = {
        "casa": casa_img, 
        "supermercado": supermercado_img, 
        "tarraco": tarraco_img,
        "farola": farola_img,
        "my_town_my_rules": mytown_img,
        "arbusto": arbusto_img
        }

    for ed in edificios:
        if ed["tipo"] in imagenes_edificios:
            pantalla.blit(imagenes_edificios[ed["tipo"]], ed["pos"])

    # ghost preview 
    pos_raton = pygame.mouse.get_pos()
    try:
        ghost = pygame.transform.scale(pygame.image.load(ruta_imagen).convert_alpha(), (64, 64))
        ghost.set_alpha(150)
        pantalla.blit(ghost, (pos_raton[0] - 32, pos_raton[1] - 32))
    except pygame.error:
        pass

    mostrar_texto(pantalla, fuente_normal,
                  _("placement_hint").format(cost=costo),
                  10, pantalla.get_height() - 30)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if dinero >= costo:
                    final_pos = (pos_raton[0] - 32, pos_raton[1] - 32)
                    edificio_rect = pygame.Rect(final_pos[0], final_pos[1], 64, 64)
                    if edificio_rect.colliderect(RIO_RECT):
                        print(_("cannot_build_on_river"))
                        alert = [_("cannot_build_on_river"), 60]
                    else:
                        edificios.append({"tipo": tipo_edificio, "pos": final_pos})
                        dinero -= costo
                        experiencia += recompensa_exp
                        print(_("building_built").format(type=tipo_edificio.capitalize(), pos=final_pos, exp=recompensa_exp))
                        return "mapainicial"
                else:
                    print(_("not_enough_money"))
                    return "construccion"
            if evento.button == 3:
                print(_("placement_cancelled"))
                return "construccion"
    return "colocando_edificio"

def facturar(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal, datos_jugador):
    global dinero, experiencia, felicidad, poblacion
    pantalla.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    # COLLECT TAXES
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'impuestos.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (40, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_impuestos = pygame.Rect(60, 380, 250, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_impuestos.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_impuestos)
    texto_surf_boton = fuente_normal.render(_("collect_taxes"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_impuestos.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_impuestos.collidepoint(evento.pos):
                print("Cambiando a la escena de cobrar impuestos...")
                return "impuestos"

    # SELL
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'venderedificio.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (440, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_vendeedificio = pygame.Rect(460, 380, 250, 50)
    color_boton = (200, 200, 100) if boton_vendeedificio.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_vendeedificio)
    texto_surf_boton = fuente_normal.render(_("sell_building"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_vendeedificio.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_vendeedificio.collidepoint(evento.pos):
                print("Cambiando a la escena de vender edificio...")
                return "vender_edificio"

    # ASK FOR A LOAN (Please don't go bankrupt)
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'prestamo.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (840, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_prestamo = pygame.Rect(860, 380, 250, 50)
    color_boton = (200, 200, 100) if boton_prestamo.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_prestamo)
    texto_surf_boton = fuente_normal.render(_("ask_loan"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_prestamo.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_prestamo.collidepoint(evento.pos):
                print("Cambiando a la escena de pedir préstamo...")
                return "prestamo"

    return "facturar"

def vender_edificio(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    global dinero, experiencia, edificios, deuda
    pantalla.fill((255, 255, 255))
    mostrar_texto(pantalla, fuente_titulo, _("sell_building"), 10, 10)
    mostrar_texto(pantalla, fuente_normal, _("click_building_to_sell"), 10, 44)

    pos_raton = pygame.mouse.get_pos()
    edificio_rects = []
    y_list = 90
    mostrar_texto(pantalla, fuente_normal, _("available_buildings"), 10, y_list)
    y_list += 30

    # Load building images for the sell screen
    imagenes_edificios = {}
    for tipo, config in EDIFICIOS_CONFIG.items():
        try:
            imagenes_edificios[tipo] = pygame.transform.scale(
                pygame.image.load(config["imagen"]).convert_alpha(),
                (64, 64)
            )
        except pygame.error:
            imagenes_edificios[tipo] = None

    for idx, ed in enumerate(edificios):
        tipo = ed["tipo"]
        pos = ed["pos"]
        rect = pygame.Rect(pos[0], pos[1], 64, 64)
        edificio_rects.append((rect, ed))

        if tipo in imagenes_edificios and imagenes_edificios[tipo] is not None:
            pantalla.blit(imagenes_edificios[tipo], pos)
        else:
            pygame.draw.rect(pantalla, (200, 200, 200), rect)
            pygame.draw.rect(pantalla, (0, 0, 0), rect, 2)

        precio_venta = obtener_precio_venta(tipo)
        nombre = obtener_nombre_edificio(tipo)
        texto_info = _("sells_for").format(name=nombre, price=precio_venta)
        texto_surf = fuente_normal.render(texto_info, True, (0, 0, 0))
        pantalla.blit(texto_surf, (pos[0], pos[1] + 70))

        if rect.collidepoint(pos_raton):
            pygame.draw.rect(pantalla, (255, 0, 0), rect, 3)
            mostrar_texto(pantalla, fuente_normal, _(f"click_to_sell"), 10, 70)

        lista_texto = f"{idx + 1}. {nombre}: {precio_venta}"
        texto_surf = fuente_normal.render(lista_texto, True, (0, 0, 0))
        pantalla.blit(texto_surf, (10, y_list + idx * 28))

    if not edificios:
        mostrar_texto(pantalla, fuente_normal, _("no_buildings_to_sell"), 10, 120)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos_click = evento.pos
            for rect, ed in edificio_rects:
                if rect.collidepoint(pos_click):
                    tipo_edificio = ed["tipo"]
                    if tipo_edificio in EDIFICIOS_CONFIG:
                        precio_venta = obtener_precio_venta(tipo_edificio)
                        if deuda > 0:
                            if precio_venta >= deuda:
                                dinero += (precio_venta - deuda)
                                print(_("loan_repaid").format(amount=deuda))
                                deuda = 0
                            else:
                                deuda -= precio_venta
                                print(_("loan_partially_repaid").format(amount=precio_venta, remaining=deuda))
                        else:
                            dinero += precio_venta
                        experiencia += obtener_experiencia_venta(tipo_edificio)
                        edificios.remove(ed)
                        print(_("building_sold").format(type=obtener_nombre_edificio(tipo_edificio), price=precio_venta))
                        return "mapainicial"
                    else:
                        print(f"Error: Tipo de edificio '{tipo_edificio}' desconocido.")
    return "vender_edificio"

def minijuegos(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    pantalla.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    mostrar_texto(pantalla, fuente_titulo, _("minigames"), 10, 10)

    # SNAKE GAME
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'snakelogo.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (40, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_snake = pygame.Rect(60, 380, 250, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_snake.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_snake)
    texto_surf_boton = fuente_normal.render(_("snakegame"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_snake.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_snake.collidepoint(evento.pos):
                print("Cargando el juego de la serpiente...")
                return "snakegame"
        if evento.type == pygame.QUIT:
            return "salir"

    # TETRIS GAME
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'tetrislogo.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (440, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_tetris = pygame.Rect(460, 380, 250, 50)
    color_boton = (200, 200, 100) if boton_tetris.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_tetris)
    texto_surf_boton = fuente_normal.render(_("tetrisgame"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_tetris.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_tetris.collidepoint(evento.pos):
                print("Cargando tetris...")
                return "tetrisgame"
        if evento.type == pygame.QUIT:
            return "salir"
        
    # SOLAR SYSTEM SIMULATOR
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'solarsystemlogo.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (840, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_solarsystem = pygame.Rect(860, 380, 250, 50)
    color_boton = (200, 200, 100) if boton_solarsystem.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_solarsystem)
    texto_surf_boton = fuente_normal.render(_("solarsystem"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_solarsystem.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_solarsystem.collidepoint(evento.pos):
                print("Cargando simulador del sistema solar...")
                return "solarsystem"
        
    boton_volver = pygame.Rect(10, 500, 250, 50)
    color_boton = (200, 200, 100) if boton_volver.collidepoint(pos_raton) else (97, 175, 14)
    pygame.draw.rect(pantalla, color_boton, boton_volver)
    texto_surf_boton = fuente_normal.render(_("back"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_volver.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_volver.collidepoint(evento.pos):
                print("Cambiando a mapa inicial")
                return "mapainicial"

    return "minijuegos"

def prestamo(pantalla, fuente_titulo, fuente_normal, eventos, datos_jugador, caja_texto_estado, datos_prestamo):
    global dinero, felicidad, experiencia, deuda
    
    input_box = pygame.Rect(pantalla.get_width() // 2 - 200, 300, 400, 40)
    color_inactivo = pygame.Color('lightskyblue3')
    color_activo = pygame.Color('dodgerblue2')

    texto_usuario = caja_texto_estado['texto']
    activo = caja_texto_estado['activo']
    color = color_activo if activo else color_inactivo

    boton_volver = pygame.Rect(pantalla.get_width() // 2 - 125, 500, 250, 50)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver.collidepoint(evento.pos):
                return "menu"
            activo = input_box.collidepoint(evento.pos)
        if activo and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                if texto_usuario.isdigit(): 
                    cantidad_int = int(texto_usuario)
                    
                    print(f"Respuesta enviada: {cantidad_int}")
                    if cantidad_int > dinero*1.3:
                        limitedeuda = _("debt_limit")
                        print(limitedeuda)
                        return "mapainicial"
                    datos_prestamo['cantidad'] = cantidad_int
                    datos_prestamo['deuda'] = datos_prestamo.get('deuda', 0) + cantidad_int
                    
                    dinero += cantidad_int
                    experiencia += 15
                    deuda += cantidad_int
                    texto_usuario = ""
                    activo = False
                    return "mapainicial"
                else:
                    print("Por favor, introduce un número válido.")
                    
            elif evento.key == pygame.K_BACKSPACE:
                texto_usuario = texto_usuario[:-1]
            else:
                # Avoid characters
                if evento.unicode.isdigit(): 
                    texto_usuario += evento.unicode

    caja_texto_estado['texto'] = texto_usuario
    caja_texto_estado['activo'] = activo

    pantalla.fill((220, 220, 255))
    
    # render 'texto_usuario'
    lineas_pregunta = _("borrow_question").split('\n') # Pygame doesn't know about \n by itself
    current_y = 180
    for linea in lineas_pregunta:
        texto_pregunta_surf = fuente_titulo.render(linea, True, (0, 0, 0))
        texto_pregunta_rect = texto_pregunta_surf.get_rect(center=(pantalla.get_width() // 2, current_y))
        pantalla.blit(texto_pregunta_surf, texto_pregunta_rect)
        current_y += texto_pregunta_surf.get_height() + 5

    texto_surf = fuente_normal.render(texto_usuario, True, (0, 0, 0))
    input_box.w = max(400, texto_surf.get_width() + 20)
    pygame.draw.rect(pantalla, color, input_box, 2)
    pantalla.blit(texto_surf, (input_box.x + 10, input_box.y + 10))

    pos_raton = pygame.mouse.get_pos()
    color_boton = (255, 100, 100) if boton_volver.collidepoint(pos_raton) else (200, 50, 50)
    pygame.draw.rect(pantalla, color_boton, boton_volver)
    texto_surf_boton = fuente_normal.render(_("back_to_menu"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_volver.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    return "prestamo"

def impuestos(pantalla, fuente_titulo, fuente_normal, eventos, datos_jugador, caja_texto_estado, datos_impuestos):
    global dinero, felicidad, experiencia, deuda
    input_box = pygame.Rect(pantalla.get_width() // 2 - 200, 300, 400, 40)
    color_inactivo = pygame.Color('lightskyblue3')
    color_activo = pygame.Color('dodgerblue2')

    texto_usuario = caja_texto_estado['texto']
    activo = caja_texto_estado['activo']
    color = color_activo if activo else color_inactivo

    boton_volver = pygame.Rect(pantalla.get_width() // 2 - 125, 500, 250, 50)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver.collidepoint(evento.pos):
                return "menu"
            activo = input_box.collidepoint(evento.pos)

        if activo and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                print(f"Respuesta enviada: {texto_usuario}")
                datos_impuestos['porcentaje'] = texto_usuario
                texto_usuario = ""
                impuestoapagar = poblacion * dineroporhabitante * (int(datos_impuestos['porcentaje']) / 100)
                print(_("tax_collected").format(amount=impuestoapagar))
                int_impuestoapagar = int(impuestoapagar)
                if (deuda > 0):
                    for i in range(int(impuestoapagar)):
                        deuda-=1
                        int_impuestoapagar-=1
                dinero += int_impuestoapagar
                felicidad -= 10
                experiencia += 15
                activo = False
                return "mapainicial"
            elif evento.key == pygame.K_BACKSPACE:
                texto_usuario = texto_usuario[:-1]
            else:
                texto_usuario += evento.unicode

    caja_texto_estado['texto'] = texto_usuario
    caja_texto_estado['activo'] = activo

    pantalla.fill((220, 220, 255))
    porcentaje = datos_impuestos.get('porcentaje', '0')
    texto_pregunta_surf = fuente_titulo.render(_("tax_question"), True, (0, 0, 0))
    texto_pregunta_rect = texto_pregunta_surf.get_rect(center=(pantalla.get_width() // 2, 200))
    pantalla.blit(texto_pregunta_surf, texto_pregunta_rect)

    texto_surf = fuente_normal.render(texto_usuario, True, (0, 0, 0))
    input_box.w = max(400, texto_surf.get_width() + 20)
    pygame.draw.rect(pantalla, color, input_box, 2)
    pantalla.blit(texto_surf, (input_box.x + 10, input_box.y + 10))

    pos_raton = pygame.mouse.get_pos()
    color_boton = (255, 100, 100) if boton_volver.collidepoint(pos_raton) else (200, 50, 50)
    pygame.draw.rect(pantalla, color_boton, boton_volver)
    texto_surf_boton = fuente_normal.render(_("back_to_menu"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_volver.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    return "impuestos"

def gameover(pantalla, eventos):
    global mouseDown, w, h

    pantalla.fill((180,0,0))

    text = pygame.font.Font(None, 128).render("GAME OVER", True, (255,255,255))
    textpos = text.get_rect(centerx=w*0.5, centery=h*0.4)
    pantalla.blit(text, textpos)

    text = pygame.font.Font(None, 32).render(_("citizens_unhappy"), True, (255,255,255))
    textpos = text.get_rect(centerx=w*0.5, centery=h*0.5)
    pantalla.blit(text, textpos)

    text = pygame.font.Font(None, 32).render(_("coup_started"), True, (255,255,255))
    textpos = text.get_rect(centerx=w*0.5, centery=h*0.6)
    pantalla.blit(text, textpos)

    quit_button = pygame.Rect(w*0.4, h*0.7, w*0.2, h*0.2)
    pygame.draw.rect(pantalla, (255, 100, 100), quit_button)

    text = pygame.font.Font(None, 30).render("Quit", True, (255,255,255))

    if quit_button.collidepoint(pygame.mouse.get_pos()):
        text = pygame.font.Font(None, 38).render("Quit", True, (255,255,255))

        if pygame.mouse.get_pressed()[0] and not mouseDown:
            return "salir"

    textpos = text.get_rect(centerx=quit_button.centerx, centery=quit_button.centery)
    pantalla.blit(text, textpos)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            print("hi")
            return "salir"

    pygame.display.flip()

    return "gameover"

# MAIN FUNCTION
def main(username=None):
    global logged_in_username, datos_jugador, mouseDown, w, h
    logged_in_username = username

    progreso_cargado = False
    if username:
        progreso_cargado = cargar_progreso(username)

    if not progreso_cargado:
        datos_jugador.clear()
        datos_jugador.update({"nombre_usuario": "", "nombre_ciudad": ""})

    pygame.init()

    # PIXELTOWN logo, only visible for Windows users (I'm an x11/Wayland Ubuntu user, so I blindly trust in this process)
    if sys.platform.startswith('win32'):
        try:
            ruta_icono = os.path.join(DIR_IMAGENES, 'pixeltown_logo.png')
            icono = pygame.image.load(ruta_icono)
            icono_escalado = pygame.transform.scale(icono, (32, 32))
            pygame.display.set_icon(icono_escalado)
        except pygame.error:
            print("No se pudo encontrar el logo, se usará el de por defecto.")

    global pantalla_real, ancho_real, alto_real
    virtual_surface = pygame.Surface((w, h))

    _original_set_mode = pygame.display.set_mode
    _original_flip = pygame.display.flip
    _original_update = pygame.display.update
    _original_get_pos = pygame.mouse.get_pos
    _original_event_get = pygame.event.get

    global _minigame_active
    _minigame_active = False
    initial_setup = True
    tamano_pendiente = None
    ultimo_cambio_tiempo = 0

    def custom_set_mode(size, flags=0, *args, **kwargs):
        global pantalla_real, ancho_real, alto_real
        nonlocal initial_setup
        if _minigame_active:
            return _original_set_mode(size, flags, *args, **kwargs)
        if size == (w, h) and initial_setup:
            initial_setup = False
            pantalla_real = _original_set_mode((w, h), flags | pygame.RESIZABLE, *args, **kwargs)
            ancho_real, alto_real = w, h
            return virtual_surface
        elif size == (w, h) and not initial_setup:
            pantalla_real = _original_set_mode((ancho_real, alto_real), flags | pygame.RESIZABLE, *args, **kwargs)
            return pantalla_real
        else:
            return _original_set_mode(size, flags, *args, **kwargs)

    def custom_flip():
        global pantalla_real, ancho_real, alto_real
        nonlocal tamano_pendiente, ultimo_cambio_tiempo
        if _minigame_active:
            _original_flip()
            return
        if tamano_pendiente is not None and (time.time() - ultimo_cambio_tiempo) > 0.15:
            pantalla_real = _original_set_mode(tamano_pendiente, pygame.RESIZABLE)
            ancho_real, alto_real = tamano_pendiente
            tamano_pendiente = None
        if pygame.display.get_surface() == pantalla_real and pantalla_real is not None:
            pygame.transform.scale(virtual_surface, pantalla_real.get_size(), pantalla_real)
        _original_flip()

    def custom_update(*args, **kwargs):
        global pantalla_real, ancho_real, alto_real
        nonlocal tamano_pendiente, ultimo_cambio_tiempo
        if _minigame_active:
            _original_update(*args, **kwargs)
            return
        if tamano_pendiente is not None and (time.time() - ultimo_cambio_tiempo) > 0.15:
            pantalla_real = _original_set_mode(tamano_pendiente, pygame.RESIZABLE)
            ancho_real, alto_real = tamano_pendiente
            tamano_pendiente = None
        if pygame.display.get_surface() == pantalla_real and pantalla_real is not None:
            pygame.transform.scale(virtual_surface, pantalla_real.get_size(), pantalla_real)
        _original_update(*args, **kwargs)

    def custom_get_pos():
        global pantalla_real
        x, y = _original_get_pos()
        if _minigame_active:
            return (x, y)
        if pygame.display.get_surface() == pantalla_real and pantalla_real is not None:
            w, h = pantalla_real.get_size()
            return (int(x * 1200 / w), int(y * 600 / h))
        return (x, y)

    def custom_event_get(*args, **kwargs):
        global pantalla_real, ancho_real, alto_real, w, h
        nonlocal tamano_pendiente, ultimo_cambio_tiempo
        events = _original_event_get(*args, **kwargs)
        if _minigame_active:
            return events
        modified_events = []
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                if pygame.display.get_surface() == pantalla_real and pantalla_real is not None:
                    tamano_pendiente = event.size
                    ultimo_cambio_tiempo = time.time()
            
            if pygame.display.get_surface() == pantalla_real and pantalla_real is not None:
                w, h = pantalla_real.get_size()
                
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    pos_x = int(event.pos[0] * 1200 / w)
                    pos_y = int(event.pos[1] * 600 / h)
                    event_dict = dict(event.__dict__)
                    event_dict['pos'] = (pos_x, pos_y)
                    modified_events.append(pygame.event.Event(event.type, event_dict))
                elif event.type == pygame.MOUSEMOTION:
                    pos_x = int(event.pos[0] * 1200 / w)
                    pos_y = int(event.pos[1] * 600 / h)
                    rel_x = int(event.rel[0] * 1200 / w)
                    rel_y = int(event.rel[1] * 600 / h)
                    event_dict = dict(event.__dict__)
                    event_dict['pos'] = (pos_x, pos_y)
                    event_dict['rel'] = (rel_x, rel_y)
                    modified_events.append(pygame.event.Event(event.type, event_dict))
                else:
                    modified_events.append(event)
            else:
                modified_events.append(event)
        return modified_events

    pygame.display.set_mode = custom_set_mode
    pygame.display.flip = custom_flip
    pygame.display.update = custom_update
    pygame.mouse.get_pos = custom_get_pos
    pygame.event.get = custom_event_get
    # Expose the original set_mode so minigame wrappers can restore the display
    pygame.display._original_set_mode = _original_set_mode

    pantalla = pygame.display.set_mode((w, h))
    pygame.display.set_caption("PIXELTOWN")
    reloj = pygame.time.Clock()

    # Fonts
    fuente_boton = pygame.font.Font(None, 35)
    fuente_titulo = pygame.font.SysFont('monospace', 25, bold=True)
    fuente_normal = pygame.font.Font(None, 32)

    # State variables (Keeping track of everything)
    estado_del_juego = "intro"

    # Text box state and player data
    estado_caja_texto = {"texto": username if (username and not progreso_cargado) else "", "activo": False}
    datos_impuestos = {"porcentaje": ""}

    # Selected building type to place
    edificio_a_colocar = None

    # MAIN GAME LOOP im literally learning spanish rn while doing this :)
    while estado_del_juego != "salir": # quit
        eventos = pygame.event.get()

        if estado_del_juego == "intro":
            estado_del_juego = escena_intro(pantalla, reloj)
        elif estado_del_juego == "menu":
            estado_del_juego = escena_menu(pantalla, fuente_titulo, fuente_boton, eventos)
        elif estado_del_juego == "jugando": # playing
            if progreso_cargado:
                estado_del_juego = "mapainicial"
            else:
                estado_del_juego = escena_juego(pantalla, fuente_boton, eventos, fuente_titulo) # game scene
        elif estado_del_juego == "preguntando": # ask
            estado_del_juego = pregunta(pantalla, fuente_titulo, fuente_normal, eventos, estado_caja_texto, datos_jugador)
        elif estado_del_juego == "preguntando2": # ask 2
            estado_del_juego = pregunta2(pantalla, fuente_titulo, fuente_normal, eventos, estado_caja_texto, datos_jugador)
        elif estado_del_juego == "cargamapa": # map loader
            estado_del_juego = cargamapa(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "mapainicial": # initial map
            estado_del_juego = mapainicial(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal, datos_jugador)
        elif estado_del_juego == "acciones": # actions
            estado_del_juego = acciones(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "tienda": # store
            estado_del_juego = tienda(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "info":
            estado_del_juego = info(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "infodos": # info2
            estado_del_juego = infodos(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "minijuegos": # minigame
            estado_del_juego = minijuegos(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "snakegame":
            estado_del_juego = snakegame(pantalla)
        elif estado_del_juego == "tetrisgame":
            estado_del_juego = tetrisgame(pantalla)
        elif estado_del_juego == "solarsystem":
            estado_del_juego = solarsystem(pantalla)
        elif estado_del_juego == "productos": # products
            estado_del_juego = productos(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "prestamo":
            estado_del_juego = prestamo(pantalla, fuente_titulo, fuente_normal, eventos, datos_jugador, estado_caja_texto, datos_impuestos)
        elif estado_del_juego == "facturar":
            estado_del_juego = facturar(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal, datos_jugador)
        elif estado_del_juego == "impuestos":
            estado_del_juego = impuestos(pantalla, fuente_titulo, fuente_normal, eventos, datos_jugador, estado_caja_texto, datos_impuestos)
        elif estado_del_juego == "productos2":
            estado_del_juego = productos2(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "vender_edificio":
            estado_del_juego = vender_edificio(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "adorno":
            resultado = adorno(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
            if isinstance(resultado, tuple):
                estado_del_juego, edificio_a_colocar = resultado
            else:
                estado_del_juego = resultado
        elif estado_del_juego == "construccion":
            resultado = construccion(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
            if isinstance(resultado, tuple):
                estado_del_juego, edificio_a_colocar = resultado  # e.g. ("colocando_edificio", "casa")
            else:
                estado_del_juego = resultado
        elif estado_del_juego == "colocando_edificio":
            if not edificio_a_colocar:
                estado_del_juego = "construccion"
            else:
                estado_del_juego = escena_colocacion(pantalla, eventos, fuente_normal, edificio_a_colocar)
                if estado_del_juego != "colocando_edificio":
                    edificio_a_colocar = None
        elif estado_del_juego == "gameover":
            estado_del_juego = gameover(pantalla, eventos)

        show_alert(pantalla)

        mouseDown = False
        if pygame.mouse.get_pressed()[0]:
            mouseDown = True

        pygame.display.flip()
        reloj.tick(60)
 
    if logged_in_username:
        guardar_progreso(logged_in_username)
    pygame.quit()
    sys.exit()


# SCRIPT ENTRY POINT
if __name__ == '__main__':
    from terminal import terminalbeggining
    terminalbeggining()