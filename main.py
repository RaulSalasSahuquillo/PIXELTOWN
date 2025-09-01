# PIXELTOWN - ARCHIVO PRINCIPAL DEL Juego
# Este archivo contiene el bucle principal y la lógica para ejecutar el juego.

# --- IMPORTACIÓN DE LIBRERÍAS Y MÓDULOS ---
import pygame
import time
import sys
from moviepy import VideoFileClip  # <- corregido
from ciudad.ciudad import Ciudad
from personaje import bipo, daemon, persona, flecha, bipobienvenida
from texto import titulo, informaciontexto1, informaciontexto2
from bloquegrafico import rio, edificio1

dinero = 10000  # Dinero inicial
poblacion = 10  # Población inicial
edificios = []  # Lista de dicts: {"tipo": str, "pos": (x, y)}
felicidad = 50  # Felicidad inicial
experiencia = 0  # Experiencia inicial
dineroporhabitante = 1000 # Cada habitante aporta 1000 de dinero

    # Aquí podrías implementar lógica adicional, como mostrar un mensaje en pantalla

# --- DEFINICIÓN DE ESCENAS ---

def escena_intro(pantalla, reloj):  # Necesitamos el reloj para controlar la velocidad
    try:
        clip = VideoFileClip('intro.mp4')
        # Iteramos sobre cada fotograma del vídeo
        for frame in clip.iter_frames(fps=clip.fps, dtype='uint8'):
            # Manejo de eventos DENTRO del bucle
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    clip.close()  # Cierra el archivo de video
                    return "salir"

            # Convierte el fotograma (de numpy a surface de Pygame)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            # Redimensiona el fotograma al tamaño de tu pantalla
            frame_scaled = pygame.transform.scale(frame_surface, pantalla.get_size())

            # Dibuja el fotograma en la pantalla principal
            pantalla.blit(frame_scaled, (0, 0))

            # Actualiza la pantalla para mostrar el fotograma
            pygame.display.flip()

            # Controla la velocidad para que coincida con los FPS del vídeo
            reloj.tick(clip.fps)

        clip.close()  # Cierra el archivo de video cuando termine

    except FileNotFoundError:
        print("Error: No se encontró el archivo de video 'intro.mp4'. Saltando intro.")
    except Exception as e:
        print(f"Ocurrió un error al reproducir el video: {e}. Saltando intro.")

    try:
        time.sleep(7)
        pygame.mixer.music.load("anewbegining.mp3")
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"No se pudo cargar el archivo de música: {e}")

    # Cuando el video termina (o falla), pasamos al menú
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

    pantalla.fill((220, 220, 255))  # Fondo lila claro    
    try:
        player_image = pygame.image.load('PIXELTOWN_portada.png').convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (1200, 600))
        pantalla.blit(player_image_scaled, (0, 0))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")

    # --- Dibujo del botón JUGAR ---
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

    pantalla.fill((200, 255, 200))  # Fondo verde claro
    try:
        player_image = pygame.image.load('BIENVENIDO.png').convert_alpha()
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
    pantalla.fill((220, 220, 255))  # Fondo lila claro

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
    pantalla.fill((255, 255, 255))  # Fondo blanco
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
    mostrar_texto(pantalla, fuente_normal, f"Edificios: {len(edificios)}", 10, 210)
    mostrar_texto(pantalla, fuente_normal, f"Experiencia: {experiencia}", 10, 250)

    try:
        casa_img = pygame.transform.scale(pygame.image.load('Casa.png').convert_alpha(), (64, 64))
        supermercado_img = pygame.transform.scale(pygame.image.load('supermercado.png').convert_alpha(), (64, 64))
        tarraco_img = pygame.transform.scale(pygame.image.load('tarraco.png').convert_alpha(), (64, 64))
    except pygame.error as e:
        print(f"Error al cargar imágenes de edificios: {e}")
        return "menu"  # Salir al menú si no se encuentran las imágenes

    # Diccionario de imágenes
    imagenes_edificios = {
        "casa": casa_img,
        "supermercado": supermercado_img,
        "tarraco": tarraco_img
    }

    # Dibujado de edificios existentes (usando tipo y pos correctos)
    for edificio in edificios:
        tipo = edificio["tipo"]
        pos = edificio["pos"]
        if tipo in imagenes_edificios:
            pantalla.blit(imagenes_edificios[tipo], pos)
        else:
            pygame.draw.rect(pantalla, (255, 0, 0), (*pos, 64, 64), 2)

    try:
        player_image = pygame.image.load('rio.png').convert_alpha()
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
                pygame.mixer.music.load("efectodestruccion.mp3")
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
            pygame.mixer.music.load("Aldea_soundtrack.mp3")
            pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"No se pudo cargar el archivo de música: {e}")
    return "mapainicial"


def acciones(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    pantalla.fill((255, 255, 255))  # Fondo blanco
    mostrar_texto(pantalla, fuente_titulo, "Acciones", 10, 10)

    # COMPRAR
    try:
        player_image = pygame.image.load('tienda.png').convert_alpha()
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

    # VENDER
    try:
        player_image = pygame.image.load('ganar_dinero.png').convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (440, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    boton_ganar_dinero = pygame.Rect(460, 380, 250, 50)
    color_boton = (200, 200, 100) if boton_ganar_dinero.collidepoint(pos_raton) else (200, 200, 50)
    pygame.draw.rect(pantalla, color_boton, boton_ganar_dinero)
    texto_surf_boton = fuente_normal.render("Facturar", True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=boton_ganar_dinero.center)
    pantalla.blit(texto_surf_boton, texto_rect_boton)
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONUP:
            if boton_ganar_dinero.collidepoint(evento.pos):
                print("Cambiando a la escena facturar...")
                return "facturar"

    # INFORMACIÓN
    try:
        player_image = pygame.image.load('info.png').convert_alpha()
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
    pantalla.fill((255, 255, 255))  # Fondo blanco
    # CONSTRUCCIÓN
    try:
        player_image = pygame.image.load('construccion.png').convert_alpha()
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

    # PRODUCTOS
    try:
        player_image = pygame.image.load('productos.png').convert_alpha()
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

    # ADORNOS
    try:
        player_image = pygame.image.load('adorno.png').convert_alpha()
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


def info(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    pantalla.fill((255, 255, 255))  # Fondo blanco
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
    pantalla.fill((255, 255, 255))  # Fondo blanco
    informaciontexto2(pantalla, fuente_titulo, 10, 10)
    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
    return "infodos"


def productos(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    global dinero, felicidad, experiencia
    
    # JABÓN DE MANOS
    pantalla.fill((255, 255, 255))  # Fondo blanco
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
        player_image = pygame.image.load('lovyc.png').convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (500, 300))
        pantalla.blit(player_image_scaled, (10, 100))
    except pygame.error:
        print("Error cargando imagen")
        pass

    # IMAGEN MASCARILLA
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
        player_image = pygame.image.load('lovyc_mascarilla.png').convert_alpha()
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
    
    # IMAGEN CHAMPÚ
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
        player_image = pygame.image.load('lovyc_champú.png').convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (700, 100))
    except pygame.error:
        pass

    # IMAGEN TOALLITAS
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
        player_image = pygame.image.load('lovyc_toallitas.png').convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (500, 300))
        pantalla.blit(player_image_scaled, (10, 100))
    except pygame.error:
        pass
    
    for evento in eventos:
        if evento.type == pygame.QUIT:
            return "salir"
    return "productos2"




def construccion(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal):
    pantalla.fill((255, 255, 255))  # Fondo blanco

    # Botón casa
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

    # Imagen y botón supermercado
    try:
        player_image = pygame.image.load('supermercado.png').convert_alpha()
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

    # Imagen casa (decorativa)
    try:
        player_image = pygame.image.load('Casa.png').convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        pantalla.blit(player_image_scaled, (30, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen 'Casa.png': {e}")

    # Tarraco Import Export
    try:
        player_image = pygame.image.load('tarraco.png').convert_alpha()
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
        "casa": {"imagen": "Casa.png", "costo": 500, "experiencia": 100},
        "supermercado": {"imagen": "supermercado.png", "costo": 1500, "experiencia": 300},
        "tarraco": {"imagen": "tarraco.png", "costo": 10000, "experiencia": 900}
    }

    if tipo_edificio not in config_edificios:
        print(f"Error: Tipo de edificio '{tipo_edificio}' desconocido.")
        return "construccion"

    config = config_edificios[tipo_edificio]
    ruta_imagen = config["imagen"]
    costo = config["costo"]
    recompensa_exp = config["experiencia"]

    # fondo/mapa
    pantalla.fill((255, 255, 255))
    try:
        rio_img = pygame.image.load('rio.png').convert_alpha()
        pantalla.blit(pygame.transform.scale(rio_img, (300, 300)), (450, 200))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")

    mostrar_texto(pantalla, fuente_normal, f"Dinero: {dinero}", 10, 10)
    mostrar_texto(pantalla, fuente_normal, f"Edificios: {len(edificios)}", 10, 40)
    mostrar_texto(pantalla, fuente_normal, f"Experiencia: {experiencia}", 10, 70)

    # cargar sprites
    try:
        casa_img = pygame.transform.scale(pygame.image.load('Casa.png').convert_alpha(), (64, 64))
        supermercado_img = pygame.transform.scale(pygame.image.load('supermercado.png').convert_alpha(), (64, 64))
        tarraco_img = pygame.transform.scale(pygame.image.load('tarraco.png').convert_alpha(), (64, 64))
    except pygame.error as e:
        print(f"Error cargando imágenes de edificios: {e}")
        return "construccion"

    imagenes_edificios = {"casa": casa_img, "supermercado": supermercado_img, "tarraco": tarraco_img}

    for ed in edificios:
        if ed["tipo"] in imagenes_edificios:
            pantalla.blit(imagenes_edificios[ed["tipo"]], ed["pos"])

    # fantasma
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
    pantalla.fill((255, 255, 255))  # Fondo blanco
    # COBRAR IMPUESTOS
    try:
        player_image = pygame.image.load('impuestos.png').convert_alpha()
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

    # VENDER
    try:
        player_image = pygame.image.load('venderedificio.png').convert_alpha()
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

    # PEDIR PRÉSTAMO
    try:
        player_image = pygame.image.load('prestamo.png').convert_alpha()
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

# --- FUNCIÓN PRINCIPAL (main) ---
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("PIXELTOWN")
    reloj = pygame.time.Clock()

    # --- Fuentes ---
    fuente_boton = pygame.font.Font(None, 35)
    fuente_titulo = pygame.font.SysFont('monospace', 25, bold=True)
    fuente_normal = pygame.font.Font(None, 32)

    # --- Variables de estado ---
    estado_del_juego = "intro"

    # Estado caja de texto y datos jugador
    estado_caja_texto = {"texto": "", "activo": False}
    datos_jugador = {"nombre_usuario": "", "nombre_ciudad": ""}
    datos_impuestos = {"porcentaje": ""}

    # NUEVO: tipo de edificio seleccionado para colocar
    edificio_a_colocar = None

    # --- BUCLE PRINCIPAL DEL JUEGO ---
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
        elif estado_del_juego == "construccion":
            resultado = construccion(pantalla, fuente_titulo, fuente_boton, eventos, fuente_normal)
            if isinstance(resultado, tuple):
                estado_del_juego, edificio_a_colocar = resultado  # p.ej. ("colocando_edificio", "casa")
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


# --- PUNTO DE ENTRADA DEL SCRIPT ---
if __name__ == '__main__':
    main()
