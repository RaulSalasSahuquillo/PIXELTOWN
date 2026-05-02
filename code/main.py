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
from moviepy import VideoFileClip  # Dear programmer, good luck importing this trash library. Honestly, it took me hours, and I still have problems.
from characters import bipo, daemon, persona, flecha, bipobienvenida
from text import titulo, informaciontexto1, informaciontexto2

# PATH CONFIGURATION (Don't mess with these!)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_IMAGENES = os.path.join(BASE_DIR, "imagenes")
DIR_PIXELTOWN_OST = os.path.join(BASE_DIR, "PIXELTOWN_OST")
DIR_VISUAL = os.path.join(BASE_DIR, "visual")

dinero = 10000  # Initial money (Don't spend it all in one place!)
poblacion = 10  # Initial population (Small, but it will grow)
edificios = []  # List of dicts: {"tipo": str, "pos": (x, y)}
felicidad = 50  # Initial happiness (We really need to cheer them up)
experiencia = 0  # Initial experience
dineroporhabitante = 1000 # Each inhabitant brings in 1000 money
tiempo = 1 # Time in days


# SCENE DEFINITION
def escena_intro(pantalla, reloj):  # We need the clock to control the speed 
    try:
        ruta_video = os.path.join(DIR_VISUAL, 'intro.mp4')
        clip = VideoFileClip(ruta_video)
        if clip.audio is not None:
            temp_audio = "temp_intro_audio.mp3" # I create the audio file of the video so that moviepy doesn't reproduce the video without the sound
            clip.audio.write_audiofile(temp_audio, logger=None)
            pygame.mixer.music.load(temp_audio)
            pygame.mixer.music.play()
        # We iterate over each frame of the video
        for frame in clip.iter_frames(fps=clip.fps, dtype='uint8'):
            # Event handling INSIDE the loop
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    clip.close()  # Close the video file
                    return "salir"

            # Convert the frame (from numpy to Pygame surface)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            # Resize the frame to match the screen size
            frame_scaled = pygame.transform.scale(frame_surface, pantalla.get_size())

            # Draw the frame on the main screen
            pantalla.blit(frame_scaled, (0, 0))

            # Update the screen to show the frame
            pygame.display.flip()

            # Control the speed to match the video's FPS
            reloj.tick(clip.fps)

        clip.close()  # Close the video file when it finishes 

    except FileNotFoundError:
        print("Error: No se encontró el archivo de video 'intro.mp4' en la carpeta visual. Saltando intro.")
    except Exception as e:
        print(f"Ocurrió un error al reproducir el video: {e}. Saltando intro.")

    try:
        time.sleep(7)
        pygame.mixer.music.load(os.path.join(DIR_PIXELTOWN_OST, "anewbegining.mp3"))
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"No se pudo cargar el archivo de música: {e}")

    # When the video finishes (or fails, fingers crossed it doesn't), we move to the menu
    return "menu"


def escena_menu(pantalla, fuente_titulo, fuente_boton, eventos):
    boton_jugar = pygame.Rect(900, 500, 200, 50)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_jugar.collidepoint(evento.pos):
                print("Cambiando a la escena del juego...")
                return "jugando"

    pantalla.fill((220, 220, 255))  # Light lilac background (Soothing, right? It took me hours to find the perfect colour. Thank me later!)    
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'PIXELTOWN_portada.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (1200, 600))
        pantalla.blit(player_image_scaled, (0, 0))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")

    # Drawing the PLAY button
    pos_raton = pygame.mouse.get_pos()
    color_boton = (100, 180, 255) if boton_jugar.collidepoint(pos_raton) else (0, 128, 255)
    pygame.draw.rect(pantalla, color_boton, boton_jugar)
    texto_surf = fuente_boton.render("JUGAR", True, (0, 0, 0))
    texto_rect = texto_surf.get_rect(center=boton_jugar.center)
    pantalla.blit(texto_surf, texto_rect)

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
    texto_surf_volver = fuente_boton.render("Volver al Menú", True, (255, 255, 255))
    texto_rect_volver = texto_surf_volver.get_rect(center=boton_volver.center)
    pantalla.blit(texto_surf_volver, texto_rect_volver)

    pygame.draw.rect(pantalla, color_continuar, boton_continuar)
    texto_surf_continuar = fuente_boton.render("Continuar", True, (255, 255, 255))
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
    texto_pregunta_surf = fuente_titulo.render("¿Cómo te llamas?", True, (0, 0, 0))
    texto_pregunta_rect = texto_pregunta_surf.get_rect(center=(pantalla.get_width() // 2, 200))
    pantalla.blit(texto_pregunta_surf, texto_pregunta_rect)

    texto_surf = fuente_normal.render(texto_usuario, True, (0, 0, 0))
    input_box.w = max(400, texto_surf.get_width() + 20)
    pygame.draw.rect(pantalla, color, input_box, 2)
    pantalla.blit(texto_surf, (input_box.x + 10, input_box.y + 10))

    pos_raton = pygame.mouse.get_pos()
    color_boton = (255, 100, 100) if boton_volver.collidepoint(pos_raton) else (200, 50, 50)
    pygame.draw.rect(pantalla, color_boton, boton_volver)
    texto_surf_boton = fuente_normal.render("Volver al Menú", True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_volver.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)

    return "preguntando"


def pregunta2(pantalla, fuente_titulo, fuente_normal, eventos, caja_texto_estado, datos_jugador):
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
        f"Bienvenid@ a PIXELTOWN, {nombre_usuario} ¿Cómo se llama tu ciudad?", True, (0, 0, 0))
    texto_pregunta_rect = texto_pregunta_surf.get_rect(center=(pantalla.get_width() // 2, 200))
    pantalla.blit(texto_pregunta_surf, texto_pregunta_rect)

    texto_surf = fuente_normal.render(texto_usuario, True, (0, 0, 0))
    input_box.w = max(400, texto_surf.get_width() + 20)
    pygame.draw.rect(pantalla, color, input_box, 2)
    pantalla.blit(texto_surf, (input_box.x + 10, input_box.y + 10))

    pos_raton = pygame.mouse.get_pos()
    color_boton = (255, 100, 100) if boton_volver.collidepoint(pos_raton) else (200, 50, 50)
    pygame.draw.rect(pantalla, color_boton, boton_volver)
    texto_surf_boton = fuente_normal.render("Volver al Menú", True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_volver.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)

    return "preguntando2"


def cargamapa(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    pygame.mixer.music.stop()
    pantalla.fill((220, 220, 255))  # Light lilac background (Soothing, right?)

    boton_vermapa = pygame.Rect(pantalla.get_width() // 2 - 125, 500, 250, 50)

    texto_titulo_surf = fuente_titulo.render("Cargando Mapa...", True, (0, 0, 0))
    texto_titulo_rect = texto_titulo_surf.get_rect(center=(pantalla.get_width() // 2, 200))
    pantalla.blit(texto_titulo_surf, texto_titulo_rect)

    pos_raton = pygame.mouse.get_pos()
    color_boton = (255, 100, 100) if boton_vermapa.collidepoint(pos_raton) else (200, 50, 50)
    pygame.draw.rect(pantalla, color_boton, boton_vermapa)
    texto_surf_boton = fuente_normal.render("Volver al Menú", True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_vermapa.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"

    pygame.display.flip()
    return "mapainicial"


def mostrar_texto(pantalla, fuente, texto, x, y, color=(0, 0, 0)):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect()
    rect_texto.topleft = (x, y)
    pantalla.blit(superficie_texto, rect_texto)


def mapainicial(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal, datos_jugador):
    pantalla.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    boton_acciones = pygame.Rect(900, 500, 250, 50)
    pos_raton = pygame.mouse.get_pos()

    color_boton = (255, 100, 100) if boton_acciones.collidepoint(pos_raton) else (200, 50, 50)
    pygame.draw.rect(pantalla, color_boton, boton_acciones)
    texto_surf_boton = fuente_normal.render("Acciones", True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_acciones.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)

    nombre_usuario = datos_jugador.get('nombre_usuario', 'Tú')
    nombre_ciudad = datos_jugador.get('nombre_ciudad', 'PixelTown')
    mostrar_texto(pantalla, fuente_normal, f"Líder: {nombre_usuario}", 10, 10)
    mostrar_texto(pantalla, fuente_normal, f"Ciudad: {nombre_ciudad}", 10, 50)
    mostrar_texto(pantalla, fuente_normal, f"Dinero: {dinero}", 10, 90)
    mostrar_texto(pantalla, fuente_normal, f"Población: {poblacion}", 10, 130)
    mostrar_texto(pantalla, fuente_normal, f"Felicidad: {felicidad}%", 10, 170)
    mostrar_texto(pantalla, fuente_normal, f"Construcciones: {len(edificios)}", 10, 210)
    mostrar_texto(pantalla, fuente_normal, f"Experiencia: {experiencia}", 10, 250)

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
        print("¡Oh, no! Los ciudadanos no estan felices.")
        time.sleep(1)
        print("¡Ha empezado un golpe de estado!")
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(os.path.join(DIR_PIXELTOWN_OST, "efectodestruccion.mp3"))
                pygame.mixer.music.play()
        except pygame.error as e:
            print(f"No se pudo cargar el archivo de música: {e}")
        finally:
            print("¡La ciudad ha sido destruida!\nHAS PERDIDO")
            return "salir"

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_acciones.collidepoint(evento.pos):
                print("Cambiando a la escena de acciones...")
                return "acciones"

    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(os.path.join(DIR_PIXELTOWN_OST, "Aldea_soundtrack.mp3"))
            pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"No se pudo cargar el archivo de música: {e}")
    return "mapainicial"


def acciones(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    pantalla.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    mostrar_texto(pantalla, fuente_titulo, "Acciones", 10, 10)

    # BUY (Time to spend)
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'tienda.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (40, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_comprar = pygame.Rect(60, 380, 250, 50)
    pos_raton = pygame.mouse.get_pos()
    color_boton = (200, 200, 100) if boton_comprar.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_comprar)
    texto_surf_boton = fuente_normal.render("Comprar", True, (255, 255, 255))
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
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (440, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_ganar_dinero = pygame.Rect(460, 380, 250, 50)
    color_boton = (200, 200, 100) if boton_ganar_dinero.collidepoint(pos_raton) else (200, 50, 50) # R, G, B
    pygame.draw.rect(pantalla, color_boton, boton_ganar_dinero)
    texto_surf_boton = fuente_normal.render("Facturar", True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_ganar_dinero.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_ganar_dinero.collidepoint(evento.pos):
                print("Cambiando a la escena facturar...")
                return "facturar"

    # INFORMATION
    try:
        player_image = pygame.image.load(os.path.join(DIR_IMAGENES, 'info.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (840, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_info = pygame.Rect(860, 380, 250, 50)
    color_boton = (200, 200, 100) if boton_info.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_info)
    texto_surf_boton = fuente_normal.render("Información", True, (255, 255, 255))
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
    texto_surf_boton = fuente_normal.render("Construcción", True, (255, 255, 255))
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
    texto_surf_boton = fuente_normal.render("Productos", True, (255, 255, 255))
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
    texto_surf_boton = fuente_normal.render("Adornos", True, (255, 255, 255))
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
    texto_surf_boton = fuente_normal.render("My Town My Rules", True, (255, 255, 255))
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
    texto_surf_boton = fuente_normal.render("Farola", True, (255, 255, 255))
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
    texto_surf_boton = fuente_normal.render("Arbusto", True, (255, 255, 255))
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
    texto_surf_boton = fuente_normal.render("Siguiente", True, (255, 255, 255))
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
    texto_surf_boton = fuente_normal.render("Volver", True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_volver.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_volver.collidepoint(evento.pos):
                print("Cambiando a mapa inicial")
                return "mapainicial"

    return "info"


def infodos(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    pantalla.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    informaciontexto2(pantalla, fuente_titulo, 10, 10)
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
    texto_surf_boton = fuente_normal.render("Jabón de manos Lov'yc | 250", True, (255, 255, 255))
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
                    print("Compra exitosa.")
                    return "mapainicial"
                else:
                    print("Dinero insuficiente.")
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
    texto_surf_boton = fuente_normal.render("Mascarilla Gold Lov'yc | 150", True, (255, 255, 255))
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
                    print("Compra exitosa.")
                    return "mapainicial"
                else:
                    print("Dinero insuficiente.")
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
    texto_surf_boton = fuente_normal.render("Siguiente", True, (255, 255, 255))
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
    texto_surf_boton = fuente_normal.render("Champú Lov'yc | 200", True, (255, 255, 255))
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
                    print("Compra exitosa.")
                    return "mapainicial"
                else:
                    print("Dinero insuficiente.")
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
    texto_surf_boton = fuente_normal.render("Toallitas Lov'yc | 100", True, (255, 255, 255))
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
                    print("Compra exitosa.")
                    return "mapainicial"
                else:
                    print("Dinero insuficiente.")
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
    texto_surf_boton = fuente_normal.render("Casa Simple", True, (255, 255, 255))
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
    texto_surf_boton = fuente_normal.render("Supermercado", True, (255, 255, 255))
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
    texto_surf_boton = fuente_normal.render("Tarraco Import Export", True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_tarraco.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP and boton_tarraco.collidepoint(evento.pos):
            return "colocando_edificio", "tarraco"

    return "construccion"


def escena_colocacion(pantalla, eventos, fuente_normal, tipo_edificio):
    global edificios, dinero, experiencia

    config_edificios = {
        "casa": {"imagen": os.path.join(DIR_IMAGENES, "Casa.png"), "costo": 500, "experiencia": 100},
        "supermercado": {"imagen": os.path.join(DIR_IMAGENES, "supermercado.png"), "costo": 1500, "experiencia": 300},
        "tarraco": {"imagen": os.path.join(DIR_IMAGENES, "tarraco.png"), "costo": 10000, "experiencia": 900},
        "farola": {"imagen": os.path.join(DIR_IMAGENES, "farola.png"), "costo": 100, "experiencia": 25},
        "my_town_my_rules": {"imagen": os.path.join(DIR_IMAGENES, "AdornoMYTOWNMYRULES.png"), "costo": 250, "experiencia": 100},
        "arbusto": {"imagen":os.path.join(DIR_IMAGENES, "arbusto.png"), "costo": 50, "experiencia": 10}
    }

    if tipo_edificio not in config_edificios:
        print(f"Error: Tipo de edificio '{tipo_edificio}' desconocido.")
        return "construccion"

    config = config_edificios[tipo_edificio]
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

    mostrar_texto(pantalla, fuente_normal, f"Dinero: {dinero}", 10, 10)
    mostrar_texto(pantalla, fuente_normal, f"Edificios: {len(edificios)}", 10, 40)
    mostrar_texto(pantalla, fuente_normal, f"Experiencia: {experiencia}", 10, 70)

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
                  f"Costo: {costo} | Clic izq: construir | Clic der: cancelar",
                  10, pantalla.get_height() - 30)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if dinero >= costo:
                    final_pos = (pos_raton[0] - 32, pos_raton[1] - 32)
                    edificios.append({"tipo": tipo_edificio, "pos": final_pos})
                    dinero -= costo
                    experiencia += recompensa_exp
                    print(f"{tipo_edificio.capitalize()} construido en: {final_pos} | +{recompensa_exp} exp")
                    return "mapainicial"
                else:
                    print("¡No tienes suficiente dinero!")
                    return "construccion"
            if evento.button == 3:
                print("Colocación cancelada.")
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
    texto_surf_boton = fuente_normal.render("COBRAR IMPUESTOS", True, (255, 255, 255))
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
    texto_surf_boton = fuente_normal.render("VENDER EDIFICIO", True, (255, 255, 255))
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
    texto_surf_boton = fuente_normal.render("PEDIR PRÉSTAMO", True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_prestamo.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_prestamo.collidepoint(evento.pos):
                print("Cambiando a la escena de pedir préstamo...")
                return "prestamo"

    return "facturar"

def impuestos(pantalla, fuente_titulo, fuente_normal, eventos, datos_jugador, caja_texto_estado, datos_impuestos):
    global dinero, felicidad, experiencia
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
                print(f"Has cobrado {impuestoapagar} en impuestos.")
                dinero += int(impuestoapagar)
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
    texto_pregunta_surf = fuente_titulo.render("¿Qué % de impuestos quieres cobrar a los ciudadanos?", True, (0, 0, 0))
    texto_pregunta_rect = texto_pregunta_surf.get_rect(center=(pantalla.get_width() // 2, 200))
    pantalla.blit(texto_pregunta_surf, texto_pregunta_rect)

    texto_surf = fuente_normal.render(texto_usuario, True, (0, 0, 0))
    input_box.w = max(400, texto_surf.get_width() + 20)
    pygame.draw.rect(pantalla, color, input_box, 2)
    pantalla.blit(texto_surf, (input_box.x + 10, input_box.y + 10))

    pos_raton = pygame.mouse.get_pos()
    color_boton = (255, 100, 100) if boton_volver.collidepoint(pos_raton) else (200, 50, 50)
    pygame.draw.rect(pantalla, color_boton, boton_volver)
    texto_surf_boton = fuente_normal.render("Volver al Menú", True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_volver.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    return "impuestos"

# MAIN FUNCTION (The boss)
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("PIXELTOWN")
    reloj = pygame.time.Clock()

    # Fonts
    fuente_boton = pygame.font.Font(None, 35)
    fuente_titulo = pygame.font.SysFont('monospace', 25, bold=True)
    fuente_normal = pygame.font.Font(None, 32)

    # State variables (Keeping track of everything)
    estado_del_juego = "intro"

    # Text box state and player data
    estado_caja_texto = {"texto": "", "activo": False}
    datos_jugador = {"nombre_usuario": "", "nombre_ciudad": ""}
    datos_impuestos = {"porcentaje": ""}

    # Selected building type to place
    edificio_a_colocar = None

    # MAIN GAME LOOP
    while estado_del_juego != "salir":
        eventos = pygame.event.get()

        if estado_del_juego == "intro":
            estado_del_juego = escena_intro(pantalla, reloj)
        elif estado_del_juego == "menu":
            estado_del_juego = escena_menu(pantalla, fuente_titulo, fuente_boton, eventos)
        elif estado_del_juego == "jugando":
            estado_del_juego = escena_juego(pantalla, fuente_boton, eventos, fuente_titulo)
        elif estado_del_juego == "preguntando":
            estado_del_juego = pregunta(pantalla, fuente_titulo, fuente_normal, eventos, estado_caja_texto, datos_jugador)
        elif estado_del_juego == "preguntando2":
            estado_del_juego = pregunta2(pantalla, fuente_titulo, fuente_normal, eventos, estado_caja_texto, datos_jugador)
        elif estado_del_juego == "cargamapa":
            estado_del_juego = cargamapa(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "mapainicial":
            estado_del_juego = mapainicial(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal, datos_jugador)
        elif estado_del_juego == "acciones":
            estado_del_juego = acciones(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "tienda":
            estado_del_juego = tienda(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "info":
            estado_del_juego = info(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "infodos":
            estado_del_juego = infodos(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "productos":
            estado_del_juego = productos(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
        elif estado_del_juego == "facturar":
            estado_del_juego = facturar(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal, datos_jugador)
        elif estado_del_juego == "impuestos":
            estado_del_juego = impuestos(pantalla, fuente_titulo, fuente_normal, eventos, datos_jugador, estado_caja_texto, datos_impuestos)
        elif estado_del_juego == "productos2":
            estado_del_juego = productos2(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
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

        pygame.display.flip()
        reloj.tick(60)
 
    pygame.quit()
    sys.exit()


# SCRIPT ENTRY POINT
if __name__ == '__main__':
    print("""
██████╗ ██╗██╗  ██╗███████╗██╗  ████████╗ ██████╗ ██╗    ██╗███╗   ██╗
██╔══██╗██║╚██╗██╔╝██╔════╝██║  ╚══██╔══╝██╔═══██╗██║    ██║████╗  ██║
██████╔╝██║ ╚███╔╝ █████╗  ██║     ██║   ██║   ██║██║ █╗ ██║██╔██╗ ██║
██╔═══╝ ██║ ██╔██╗ ██╔══╝  ██║     ██║   ██║   ██║██║███╗██║██║╚██╗██║
██║     ██║██╔╝ ██╗███████╗███████╗██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
""")
    main()