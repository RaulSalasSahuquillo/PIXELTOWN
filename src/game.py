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
from spaceship import run_spaceship
from pyvidplayer2 import Video
from characters import bipo, daemon, person, arrow, bipo_welcome
from text import title, info_text_1, info_text_2
from localization import _, get_language
from pixeltown_titlescreen import render_title_background

# PATH CONFIGURATION (Don't mess with these!)
# When running as a PyInstaller bundle, files are extracted to sys._MEIPASS
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")
PIXELTOWN_OST_DIR = os.path.join(BASE_DIR, "assets", "PIXELTOWN_OST")
VISUAL_DIR = os.path.join(BASE_DIR, "assets", "visual")

# width and height of screen
w = 1200
h = 600

# Display scaling globals
real_screen = None
real_width = 1200
real_height = 600

money = 10000  # Initial money (Don't spend it all in one place!)
population = 10  # Initial population (Small, but it will grow)
buildings = []  # List of dicts: {"tipo": str, "pos": (x, y)}
happiness = 50  # Initial happiness (We really need to cheer them up)
experience = 0  # Initial experience
money_per_inhabitant = 1000 # Each inhabitant brings in 1000 money
time_days = 1 # Time in days
debt = 0 # Your debt
level = 1 # Your level
sound_on = 1 # Volume toggle (0 for off, 1 for on)
mouseDown = False # if mouse is down in the previous frame, it is True
alert = ["", 0] # [message, timer]

# SESSION AND SAVES STATE
logged_in_username = None
last_saved_time = 0
save_message = ""
player_data = {"nombre_usuario": "", "nombre_ciudad": "", "current_mission": 0, "completed_missions": []}
current_mission = 0
completed_missions = []

# Configuration of buildings and decorations
BUILDINGS_CONFIG = {
    "house": {
        "imagen": os.path.join(IMAGES_DIR, "house.png"),
        "costo": 100,
        "experiencia": 10,
        "nombre_clave": "simple_house"
    },
    "mailoffice": {
        "imagen": os.path.join(IMAGES_DIR, "mailoffice.png"),
        "costo": 400,
        "experiencia": 25,
        "nombre_clave": "mailoffice"
    },
    "supermarket": {
        "imagen": os.path.join(IMAGES_DIR, "supermarket.png"),
        "costo": 500,
        "experiencia": 30,
        "nombre_clave": "supermarket"
    },
    "restaurant": {
        "imagen": os.path.join(IMAGES_DIR, "restaurant.png"),
        "costo": 600,
        "experiencia": 40,
        "nombre_clave": "restaurant"
    },
    "gym": {
        "imagen": os.path.join(IMAGES_DIR, "gym.png"),
        "costo": 700,
        "experiencia": 45,
        "nombre_clave": "gym"
    },
    "tarraco": {
        "imagen": os.path.join(IMAGES_DIR, "tarraco.png"),
        "costo": 800,
        "experiencia": 50,
        "nombre_clave": "tarraco"
    },
    "school": {
        "imagen": os.path.join(IMAGES_DIR, "school.png"),
        "costo": 1000,
        "experiencia": 60,
        "nombre_clave": "school"
    },
    "policestation": {
        "imagen": os.path.join(IMAGES_DIR, "policestation.png"),
        "costo": 1200,
        "experiencia": 75,
        "nombre_clave": "policestation"
    },
    "townhall": {
        "imagen": os.path.join(IMAGES_DIR, "townhall.png"),
        "costo": 2000,
        "experiencia": 120,
        "nombre_clave": "townhall"
    },
    "farola": {
        "imagen": os.path.join(IMAGES_DIR, "streetlamp.png"),
        "costo": 20,
        "experiencia": 2,
        "nombre_clave": "streetlamp"
    },
    "my_town_my_rules": {
        "imagen": os.path.join(IMAGES_DIR, "ornament_mytownmyrules.png"),
        "costo": 50,
        "experiencia": 5,
        "nombre_clave": "my_town_my_rules"
    },
    "arbusto": {
        "imagen": os.path.join(IMAGES_DIR, "bush.png"),
        "costo": 10,
        "experiencia": 1,
        "nombre_clave": "bush"
    },
    "fountain": {
        "imagen": os.path.join(IMAGES_DIR, "fountain.png"),
        "costo": 150,
        "experiencia": 15,
        "nombre_clave": "fountain"
    },
    "tree": {
        "imagen": os.path.join(IMAGES_DIR, "tree.png"),
        "costo": 30,
        "experiencia": 3,
        "nombre_clave": "tree"
    },
    "statue": {
        "imagen": os.path.join(IMAGES_DIR, "statue.png"),
        "costo": 200,
        "experiencia": 20,
        "nombre_clave": "statue"
    },
    "water_feature": {
        "imagen": os.path.join(IMAGES_DIR, "water_feature.png"),
        "costo": 120,
        "experiencia": 12,
        "nombre_clave": "water_feature"
    },
    "trashcan": {
        "imagen": os.path.join(IMAGES_DIR, "trashcan.png"),
        "costo": 15,
        "experiencia": 1,
        "nombre_clave": "trashcan"
    },
    "sewer": {
        "imagen": os.path.join(IMAGES_DIR, "sewer.png"),
        "costo": 25,
        "experiencia": 2,
        "nombre_clave": "sewer"
    }
}

BUILDING_KEYS = [
    "house", "mailoffice", "supermarket", 
    "restaurant", "gym", "tarraco", 
    "school", "policestation", "townhall"
]

ORNAMENT_KEYS = [
    "farola", "arbusto", "my_town_my_rules",
    "fountain", "tree", "statue",
    "water_feature", "trashcan", "sewer"
]

def get_sell_price(building_type):
    return BUILDINGS_CONFIG.get(building_type, {}).get("costo", 0) // 2

def get_sell_experience(building_type):
    return BUILDINGS_CONFIG.get(building_type, {}).get("experiencia", 0) // 2

def get_building_name(building_type):
    cfg = BUILDINGS_CONFIG.get(building_type, {})
    key = cfg.get("nombre_clave") or cfg.get("nombre_key") or building_type
    return _(key)

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

MISSIONS_CONFIG = [
    {
        "id": 1,
        "title_key": "mission_1_title",
        "desc_key": "mission_1_desc",
        "dialogue_key": "mission_1_dialogue",
        "target_type": "building_type",
        "target_name": "house",
        "target_amount": 1,
        "reward_money": 100,
        "reward_exp": 50
    },
    {
        "id": 2,
        "title_key": "mission_2_title",
        "desc_key": "mission_2_desc",
        "dialogue_key": "mission_2_dialogue",
        "target_type": "money",
        "target_name": None,
        "target_amount": 1500,
        "reward_money": 200,
        "reward_exp": 50
    },
    {
        "id": 3,
        "title_key": "mission_3_title",
        "desc_key": "mission_3_desc",
        "dialogue_key": "mission_3_dialogue",
        "target_type": "building_type",
        "target_name": "supermarket",
        "target_amount": 1,
        "reward_money": 300,
        "reward_exp": 100
    },
    {
        "id": 4,
        "title_key": "mission_4_title",
        "desc_key": "mission_4_desc",
        "dialogue_key": "mission_4_dialogue",
        "target_type": "level",
        "target_name": None,
        "target_amount": 2,
        "reward_money": 500,
        "reward_exp": 150
    },
    {
        "id": 5,
        "title_key": "mission_5_title",
        "desc_key": "mission_5_desc",
        "dialogue_key": "mission_5_dialogue",
        "target_type": "total_buildings",
        "target_name": None,
        "target_amount": 3,
        "reward_money": 400,
        "reward_exp": 100
    }
]

def check_mission_progress(mission):
    target_type = mission["target_type"]
    target_amount = mission["target_amount"]

    if target_type == "building_type":
        current = sum(1 for b in buildings if b.get("tipo") == mission["target_name"])
    elif target_type == "total_buildings":
        current = len(buildings)
    elif target_type == "money":
        current = money
    elif target_type == "experience":
        current = experience
    elif target_type == "level":
        current = level
    else:
        current = 0

    completed = current >= target_amount
    return current, target_amount, completed

def save_progress(username):
    if not username:
        return False
    path = get_save_path(username)
    state = {
        "dinero": money,
        "poblacion": population,
        "edificios": buildings,
        "felicidad": happiness,
        "experiencia": experience,
        "dineroporhabitante": money_per_inhabitant,
        "tiempo": time_days,
        "deuda": debt,
        "nivel": level,
        "current_mission": current_mission,
        "completed_missions": completed_missions,
        "datos_jugador": player_data
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
        print(f"Progreso guardado para {username} en {path}")
        return True
    except Exception as e:
        print(f"Error al guardar progreso: {e}")
        return False

def load_progress(username):
    global money, population, buildings, happiness, experience, money_per_inhabitant, time_days, debt, level, current_mission, completed_missions, player_data
    if not username:
        return False
    path = get_save_path(username)
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
        
        money = state.get("dinero", 10000)
        population = state.get("poblacion", 10)
        
        raw_buildings = state.get("edificios", [])
        buildings = []
        for ed in raw_buildings:
            pos = ed.get("pos", [0, 0])
            buildings.append({
                "tipo": ed.get("tipo", "house"),
                "pos": (pos[0], pos[1])
            })
            
        happiness = state.get("felicidad", 50)
        experience = state.get("experiencia", 0)
        money_per_inhabitant = state.get("dineroporhabitante", 1000)
        time_days = state.get("tiempo", 1)
        debt = state.get("deuda", 0)
        level = state.get("nivel", 1)
        current_mission = state.get("current_mission", 0)
        completed_missions = state.get("completed_missions", [])
        
        loaded_player_data = state.get("datos_jugador", {})
        player_data["nombre_usuario"] = loaded_player_data.get("nombre_usuario", username)
        player_data["nombre_ciudad"] = loaded_player_data.get("nombre_ciudad", "PixelTown")
        player_data["current_mission"] = current_mission
        player_data["completed_missions"] = completed_missions
        
        print(f"Progreso cargado con éxito para {username} desde {path}")
        return True
    except Exception as e:
        print(f"Error al cargar progreso: {e}")
        return False

def add_reward(money_amount, exp_amount):
    global money, experience, alert
    money += money_amount
    experience += exp_amount
    msg = f"+{money_amount} Money  +{exp_amount} XP"
    alert = [msg, 90]
    print(msg)

_IMAGE_CACHE = {}

def get_cached_image(filename, size=None):
    """Retrieve an image from cache, loading and scaling it only once for smooth 60 FPS performance."""
    key = (filename, size)
    if key not in _IMAGE_CACHE:
        full_path = filename if os.path.isabs(filename) else os.path.join(IMAGES_DIR, filename)
        img = pygame.image.load(full_path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        _IMAGE_CACHE[key] = img
    return _IMAGE_CACHE[key]

def sound_button(screen):
    global sound_on, mouseDown

    # load image and setup rect
    sound_imgs = [get_cached_image("soundoff.png", (50, 50)), 
                  get_cached_image("soundon.png", (50, 50))]
    sound_rect = pygame.Rect(50, 500, 50, 50)

    # checking for sound button pressed
    if sound_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not mouseDown:
        sound_on = (sound_on + 1) % 2 # 1 -> 0, 0 -> 1
        if sound_on == 0:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(1)

    # draw the button
    screen.blit(sound_imgs[sound_on], (sound_rect.x, sound_rect.y))

def show_alert(screen):
    global alert, w, h

    if alert and alert[1] > 0:
        font = pygame.font.Font(None, 28)
        text_surf = font.render(alert[0], True, (255, 255, 255))
        padding_x, padding_y = 18, 8
        box_w = text_surf.get_width() + padding_x * 2
        box_h = text_surf.get_height() + padding_y * 2

        bg_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (20, 20, 20, 220), (0, 0, box_w, box_h), border_radius=8)
        pygame.draw.rect(bg_surf, (255, 215, 0, 255), (0, 0, box_w, box_h), width=2, border_radius=8)

        box_rect = bg_surf.get_rect(center=(w / 2, h * 0.9))
        screen.blit(bg_surf, box_rect.topleft)

        text_rect = text_surf.get_rect(center=box_rect.center)
        screen.blit(text_surf, text_rect)

        alert[1] -= 1

# SCENE DEFINITION
def intro_scene(screen, clock):
    try:
        video_path = os.path.join(VISUAL_DIR, 'intro.mp4')
        video = Video(video_path)
        
        # Same dimensions as the pygame screen
        screen_dimensions = screen.get_size()
        video.resize(screen.get_size())

        while video.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    video.close()
                    return "salir"
            video.draw(screen, (0, 0), screen_dimensions)
            pygame.display.flip()
            clock.tick(video.frame_rate) 

        video.close()

    except FileNotFoundError:
        print("Error: No se encontró el archivo de video 'intro.mp4'. Saltando intro.")
    except Exception as e:
        print(f"Ocurrió un error al reproducir el video con pyvidplayer2: {e}. Saltando intro.")

    try:
        pygame.mixer.music.load(os.path.join(PIXELTOWN_OST_DIR, "anewbegining.mp3"))
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"No se pudo cargar el archivo de música: {e}")

    return "menu"

def menu_scene(screen, title_font, button_font, events): # menu_scene
    global w, h
    play_button = pygame.Rect(900, 500, 200, 50) # play button

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"
        if event.type == pygame.MOUSEBUTTONUP:
            if play_button.collidepoint(event.pos):
                print("Cambiando a la escena del juego...")
                return "jugando"

    render_title_background(screen, w, h)

    # Drawing the PLAY button
    mouse_pos = pygame.mouse.get_pos()
    button_color = (100, 180, 255) if play_button.collidepoint(mouse_pos) else (0, 128, 255)
    pygame.draw.rect(screen, button_color, play_button)
    text_surf = button_font.render(_("play"), True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=play_button.center)
    screen.blit(text_surf, text_rect)

    sound_button(screen)

    return "menu"


def game_scene(screen, button_font, events, title_font):
    back_button = pygame.Rect(50, 500, 250, 50)
    continue_button = pygame.Rect(900, 500, 250, 50)

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"
        if event.type == pygame.MOUSEBUTTONUP:
            if back_button.collidepoint(event.pos):
                print("Volviendo al menú...")
                return "menu"
            elif continue_button.collidepoint(event.pos):
                print("Continuando a la escena de pregunta...")
                return "preguntando"

    screen.fill((200, 255, 200))  # Light green background
    try:
        welcome_img_name = 'welcome-en.png' if get_language() == 'en' else 'welcome.png'
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, welcome_img_name)).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (400, 400))
        screen.blit(player_image_scaled, (400, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")

    mouse_pos = pygame.mouse.get_pos()
    color_volver = (255, 100, 100) if back_button.collidepoint(mouse_pos) else (200, 50, 50)
    color_continuar = (100, 180, 255) if continue_button.collidepoint(mouse_pos) else (0, 128, 255)

    pygame.draw.rect(screen, color_volver, back_button)
    texto_surf_volver = button_font.render(_("back_to_menu"), True, (255, 255, 255))
    texto_rect_volver = texto_surf_volver.get_rect(center=back_button.center)
    screen.blit(texto_surf_volver, texto_rect_volver)

    pygame.draw.rect(screen, color_continuar, continue_button)
    texto_surf_continuar = button_font.render(_("continue"), True, (255, 255, 255))
    texto_rect_continuar = texto_surf_continuar.get_rect(center=continue_button.center)
    screen.blit(texto_surf_continuar, texto_rect_continuar)

    return "jugando"


def ask_name_scene(screen, title_font, normal_font, events, textbox_state, player_data):
    input_box = pygame.Rect(screen.get_width() // 2 - 200, 300, 400, 40)
    inactive_color = pygame.Color('lightskyblue3')
    active_color = pygame.Color('dodgerblue2')

    user_text = textbox_state['texto']
    active = textbox_state['activo']
    color = active_color if active else inactive_color

    back_button = pygame.Rect(screen.get_width() // 2 - 125, 500, 250, 50)

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                return "menu"
            active = input_box.collidepoint(event.pos)

        if active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(f"Respuesta enviada: {user_text}")
                player_data['nombre_usuario'] = user_text
                textbox_state['texto'] = ""
                user_text = ""
                active = False
                return "preguntando2"
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    textbox_state['texto'] = user_text
    textbox_state['activo'] = active

    screen.fill((220, 220, 255))
    texto_pregunta_surf = title_font.render(_("what_is_your_name"), True, (0, 0, 0))
    texto_pregunta_rect = texto_pregunta_surf.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(texto_pregunta_surf, texto_pregunta_rect)

    text_surf = normal_font.render(user_text, True, (0, 0, 0))
    input_box.w = max(400, text_surf.get_width() + 20)
    pygame.draw.rect(screen, color, input_box, 2)
    screen.blit(text_surf, (input_box.x + 10, input_box.y + 10))

    mouse_pos = pygame.mouse.get_pos()
    button_color = (255, 100, 100) if back_button.collidepoint(mouse_pos) else (200, 50, 50)
    pygame.draw.rect(screen, button_color, back_button)
    texto_surf_boton = normal_font.render(_("back_to_menu"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=back_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)

    return "preguntando"


def ask_city_name_scene(screen, title_font, normal_font, events, textbox_state, player_data):
    global logged_in_username
    input_box = pygame.Rect(screen.get_width() // 2 - 200, 300, 400, 40)
    inactive_color = pygame.Color('lightskyblue3')
    active_color = pygame.Color('dodgerblue2')

    user_text = textbox_state['texto']
    active = textbox_state['activo']
    color = active_color if active else inactive_color

    back_button = pygame.Rect(screen.get_width() // 2 - 125, 500, 250, 50)

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                return "menu"
            active = input_box.collidepoint(event.pos)

        if active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(f"Respuesta enviada: {user_text}")
                player_data['nombre_ciudad'] = user_text
                user_text = ""
                active = False
                if logged_in_username:
                    save_progress(logged_in_username)
                return "cargamapa"
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    textbox_state['texto'] = user_text
    textbox_state['activo'] = active

    screen.fill((220, 220, 255))
    user_name = player_data.get('nombre_usuario', 'Tú')
    texto_pregunta_surf = title_font.render(
        _("welcome_city_name").format(username=user_name), True, (0, 0, 0))
    texto_pregunta_rect = texto_pregunta_surf.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(texto_pregunta_surf, texto_pregunta_rect)

    text_surf = normal_font.render(user_text, True, (0, 0, 0))
    input_box.w = max(400, text_surf.get_width() + 20)
    pygame.draw.rect(screen, color, input_box, 2)
    screen.blit(text_surf, (input_box.x + 10, input_box.y + 10))

    mouse_pos = pygame.mouse.get_pos()
    button_color = (255, 100, 100) if back_button.collidepoint(mouse_pos) else (200, 50, 50)
    pygame.draw.rect(screen, button_color, back_button)
    texto_surf_boton = normal_font.render(_("back_to_menu"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=back_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)

    return "preguntando2"


def map_loader_scene(screen, title_font, button_font, events, normal_font):
    pygame.mixer.music.stop()
    screen.fill((220, 220, 255))  # Light lilac background (Soothing, right?)

    view_map_button = pygame.Rect(screen.get_width() // 2 - 125, 500, 250, 50)

    title_text_surf = title_font.render(_("loading_map"), True, (0, 0, 0))
    title_text_rect = title_text_surf.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(title_text_surf, title_text_rect)

    mouse_pos = pygame.mouse.get_pos()
    button_color = (255, 100, 100) if view_map_button.collidepoint(mouse_pos) else (200, 50, 50)
    pygame.draw.rect(screen, button_color, view_map_button)
    texto_surf_boton = normal_font.render(_("back_to_menu"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=view_map_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"

    pygame.display.flip()
    return "mapainicial"


def display_text(screen, font, text, x, y, color=(0, 0, 0), line_spacing=5):
    lines = text.split("\n")
    current_y = y
    for line in lines:
        # Render the actual lines
        text_surface = font.render(line, True, color)
        # Draw it on the screen
        screen.blit(text_surface, (x, current_y))
        current_y += text_surface.get_height() + line_spacing


def initial_map_scene(screen, title_font, button_font, events, normal_font, player_data):
    global level, experience, logged_in_username, last_saved_time, save_message, alert
    screen.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    actions_button = pygame.Rect(900, 500, 250, 50)
    save_button = pygame.Rect(125, 500, 250, 50)
    mouse_pos = pygame.mouse.get_pos()
    
    if experience >= 100 and level < 5:
        experience = 0
        level += 1
    elif experience >= 1000 and (level >= 5 and level < 10):
        experience = 0
        level += 1
    button_color = (255, 100, 100) if actions_button.collidepoint(mouse_pos) else (200, 50, 50)
    pygame.draw.rect(screen, button_color, actions_button)
    texto_surf_boton = normal_font.render(_("actions"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=actions_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)

    # Save button drawing
    if logged_in_username:
        save_button_color = (100, 200, 100) if save_button.collidepoint(mouse_pos) else (50, 150, 50)
        save_text = _("save_progress")
    else:
        save_button_color = (180, 180, 180)
        save_text = _("guest_cannot_save")
        
    pygame.draw.rect(screen, save_button_color, save_button)
    texto_surf_guardar = normal_font.render(save_text, True, (255, 255, 255))
    texto_rect_guardar = texto_surf_guardar.get_rect(center=save_button.center)
    screen.blit(texto_surf_guardar, texto_rect_guardar)

    # Success/Warning message
    if time.time() - last_saved_time < 3:
        text_color = (0, 128, 0) if logged_in_username else (200, 0, 0)
        display_text(screen, normal_font, save_message, 50, 460, color=text_color)

    user_name = player_data.get('nombre_usuario', 'Tú')
    city_name = player_data.get('nombre_ciudad', 'PixelTown')
    view_stats_button = pygame.Rect(screen.get_width() - 170, 15, 150, 35)
    mouse_pos = pygame.mouse.get_pos()
    button_color = (255, 100, 100) if view_stats_button.collidepoint(mouse_pos) else (200, 50, 50)
    pygame.draw.rect(screen, button_color, view_stats_button)
    texto_surf_boton = normal_font.render(_("view_stats"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=view_stats_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    if view_stats_button.collidepoint(mouse_pos):
        display_text(screen, normal_font, _("leader").format(username=user_name), 10, 10)
        display_text(screen, normal_font, _("city").format(cityname=city_name), 10, 50)
        display_text(screen, normal_font, _("money").format(money=money), 10, 90)
        display_text(screen, normal_font, _("population").format(population=population), 10, 130)
        display_text(screen, normal_font, _("happiness").format(happiness=happiness), 10, 170)
        display_text(screen, normal_font, _("buildings").format(count=len(buildings)), 10, 210)
        display_text(screen, normal_font, _("experience").format(experience=experience), 10, 250)
        display_text(screen, normal_font, _("debt").format(debt=debt), 10, 290)
        display_text(screen, normal_font, _("level").format(level=level), 10, 330)

    # Image dictionary dynamically built from BUILDINGS_CONFIG
    building_images = {}
    for b_type, b_cfg in BUILDINGS_CONFIG.items():
        try:
            building_images[b_type] = get_cached_image(os.path.basename(b_cfg["imagen"]), (64, 64))
        except pygame.error:
            pass

    # Draw existing buildings (The real estate)
    for building in buildings:
        tipo = building["tipo"]
        pos = building["pos"]
        if tipo in building_images:
            screen.blit(building_images[tipo], pos)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (*pos, 64, 64), 2)

    try:
        rio_img = get_cached_image('river.png', (300, 300))
        screen.blit(rio_img, (450, 200))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    if happiness < 10:
        print(_("citizens_unhappy"))
        print(_("coup_started"))
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(os.path.join(PIXELTOWN_OST_DIR, "efectodestruccion.mp3"))
                pygame.mixer.music.play()
        except pygame.error as e:
            print(f"No se pudo cargar el archivo de música: {e}")
        finally:
            print(_("game_over"))
            return "gameover"
    for event in events:
        if event.type == pygame.QUIT:
            return "salir"
        if event.type == pygame.MOUSEBUTTONUP:
            if actions_button.collidepoint(event.pos):
                print("Cambiando a la escena de acciones...")
                return "acciones"
            if save_button.collidepoint(event.pos):
                if logged_in_username:
                    if save_progress(logged_in_username):
                        last_saved_time = time.time()
                        save_message = _("progress_saved")
                else:
                    last_saved_time = time.time()
                    save_message = _("guest_cannot_save")
    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(os.path.join(PIXELTOWN_OST_DIR, "Aldea_soundtrack.mp3"))
            pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"No se pudo cargar el archivo de música: {e}")

    sound_button(screen)
    
    return "mapainicial"


def actions_scene(screen, title_font, button_font, events, normal_font):
    screen.fill((255, 255, 255))  # White background
    display_text(screen, title_font, _("actions"), 10, 10)
    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"

    # BUY (Shop)
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'shop.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (190, 190))
        screen.blit(player_image_scaled, (90, 30))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    buy_button = pygame.Rect(60, 230, 250, 45)
    button_color = (200, 200, 100) if buy_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, buy_button, border_radius=6)
    texto_surf = normal_font.render(_("buy"), True, (255, 255, 255))
    texto_rect = texto_surf.get_rect(center=buy_button.center)
    screen.blit(texto_surf, texto_rect)

    # INVOICE (Sell / Earn money)
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'earn_money.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (190, 190))
        screen.blit(player_image_scaled, (505, 30))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    earn_money_button = pygame.Rect(475, 230, 250, 45)
    button_color = (200, 200, 100) if earn_money_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, earn_money_button, border_radius=6)
    texto_surf = normal_font.render(_("invoice"), True, (255, 255, 255))
    texto_rect = texto_surf.get_rect(center=earn_money_button.center)
    screen.blit(texto_surf, texto_rect)

    # INFORMATION
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'info.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (190, 190))
        screen.blit(player_image_scaled, (895, 30))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    info_button = pygame.Rect(865, 230, 250, 45)
    button_color = (200, 200, 100) if info_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, info_button, border_radius=6)
    texto_surf = normal_font.render(_("information"), True, (255, 255, 255))
    texto_rect = texto_surf.get_rect(center=info_button.center)
    screen.blit(texto_surf, texto_rect)

    # MINIGAMES
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'minigames.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (190, 190))
        screen.blit(player_image_scaled, (90, 290))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    minigames_button = pygame.Rect(60, 490, 250, 45)
    button_color = (200, 200, 100) if minigames_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, minigames_button, border_radius=6)
    texto_surf = normal_font.render(_("minigames"), True, (255, 255, 255))
    texto_rect = texto_surf.get_rect(center=minigames_button.center)
    screen.blit(texto_surf, texto_rect)

    # MISSIONS
    try:
        player_image = get_cached_image('mission.png', (190, 190))
        screen.blit(player_image, (505, 290))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    missions_button = pygame.Rect(475, 490, 250, 45)
    button_color = (200, 200, 100) if missions_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, missions_button, border_radius=6)
    texto_surf = normal_font.render(_("missions"), True, (255, 255, 255))
    texto_rect = texto_surf.get_rect(center=missions_button.center)
    screen.blit(texto_surf, texto_rect)

    # BACK BUTTON
    back_button = pygame.Rect(865, 490, 250, 45)
    button_color = (200, 200, 100) if back_button.collidepoint(mouse_pos) else (97, 175, 14)
    pygame.draw.rect(screen, button_color, back_button, border_radius=6)
    texto_surf = normal_font.render(_("back"), True, (255, 255, 255))
    texto_rect = texto_surf.get_rect(center=back_button.center)
    screen.blit(texto_surf, texto_rect)

    # Click Handling
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if buy_button.collidepoint(event.pos):
                print("Cambiando a la escena de tienda...")
                return "tienda"
            elif earn_money_button.collidepoint(event.pos):
                print("Cambiando a la escena facturar...")
                return "facturar"
            elif info_button.collidepoint(event.pos):
                print("Cambiando a la escena de información...")
                return "info"
            elif minigames_button.collidepoint(event.pos):
                print("Cambiando a la escena de minijuegos")
                return "minijuegos"
            elif missions_button.collidepoint(event.pos):
                print("Cambiando a la escena de misiones...")
                return "misiones"
            elif back_button.collidepoint(event.pos):
                print("Volviendo al mapa inicial...")
                return "mapainicial"

    return "acciones"

_missions_helper_x = -300.0
_missions_char_index = 0.0
_missions_last_mission_id = -1

def missions_scene(screen, title_font, button_font, events, normal_font):
    global current_mission, completed_missions, _missions_helper_x, _missions_char_index, _missions_last_mission_id, player_data

    screen.fill((245, 247, 252))

    # Top Header Bar
    header_rect = pygame.Rect(0, 0, screen.get_width(), 70)
    pygame.draw.rect(screen, (230, 236, 248), header_rect)
    pygame.draw.line(screen, (200, 210, 230), (0, 70), (screen.get_width(), 70), width=2)

    display_text(screen, title_font, _("missions"), 180, 22)

    # Header icon mission.png
    try:
        mission_img = get_cached_image("mission.png", (60, 60))
        screen.blit(mission_img, (screen.get_width() - 80, 5))
    except pygame.error:
        pass

    # Back Button at top-left
    back_btn = pygame.Rect(20, 15, 130, 40)
    mouse_pos = pygame.mouse.get_pos()
    btn_color = (200, 200, 100) if back_btn.collidepoint(mouse_pos) else (97, 175, 14)
    pygame.draw.rect(screen, btn_color, back_btn, border_radius=8)
    back_surf = normal_font.render(_("back"), True, (255, 255, 255))
    back_rect = back_surf.get_rect(center=back_btn.center)
    screen.blit(back_surf, back_rect)

    # Helper entrance sliding animation (smooth lerp from -250 to 35)
    _missions_helper_x += (35 - _missions_helper_x) * 0.15

    # Check active mission index
    if current_mission < len(MISSIONS_CONFIG):
        active_mission = MISSIONS_CONFIG[current_mission]

        # Reset typewriter if mission changed
        if _missions_last_mission_id != active_mission["id"]:
            _missions_char_index = 0.0
            _missions_last_mission_id = active_mission["id"]

        full_dialogue = _(active_mission["dialogue_key"])
        text_length = len(full_dialogue)

        # Advance typewriter index
        if _missions_char_index < text_length:
            _missions_char_index += 0.6
            is_speaking = True
        else:
            is_speaking = False

        visible_dialogue = full_dialogue[:int(_missions_char_index)]

        # Helper sprite (toy.png vs toyspeaking.png) - PRESERVING EXACT 1.068 ASPECT RATIO (200x187)
        sprite_name = "toyspeaking.png" if is_speaking else "toy.png"
        try:
            toy_img = get_cached_image(sprite_name, (200, 187))
            screen.blit(toy_img, (int(_missions_helper_x), 85))
        except pygame.error:
            pass

        # Dialogue Speech Bubble next to Toy (bubble_x = int(_missions_helper_x) + 220, y = 85, w = 890, h = 185)
        bubble_x = int(_missions_helper_x) + 220
        bubble_y = 85
        bubble_w = 890
        bubble_h = 185

        if bubble_x > 50:
            # Draw speech bubble box
            bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_w, bubble_h)
            pygame.draw.rect(screen, (255, 255, 255), bubble_rect, border_radius=14)
            pygame.draw.rect(screen, (70, 130, 220), bubble_rect, width=3, border_radius=14)

            # Draw tail pointing left to Toy's mouth
            tail_points = [(bubble_x, bubble_y + 45), (bubble_x - 16, bubble_y + 60), (bubble_x, bubble_y + 75)]
            pygame.draw.polygon(screen, (255, 255, 255), tail_points)
            pygame.draw.lines(screen, (70, 130, 220), False, tail_points, width=3)

            # Render multiline visible text inside bubble
            words = visible_dialogue.split(" ")
            lines = []
            cur_line = ""
            for word in words:
                test_line = cur_line + (" " if cur_line else "") + word
                if normal_font.size(test_line)[0] <= bubble_w - 35:
                    cur_line = test_line
                else:
                    lines.append(cur_line)
                    cur_line = word
            if cur_line:
                lines.append(cur_line)

            line_y = bubble_y + 20
            for line in lines[:5]:
                t_surf = normal_font.render(line, True, (30, 35, 50))
                screen.blit(t_surf, (bubble_x + 20, line_y))
                line_y += 30

        # Mission Details Card (Bottom Section: card_x = 35, y = 295, w = 1130, h = 280)
        card_x = 35
        card_y = 295
        card_w = 1130
        card_h = 280
        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)
        pygame.draw.rect(screen, (255, 255, 255), card_rect, border_radius=16)
        pygame.draw.rect(screen, (100, 149, 237), card_rect, width=3, border_radius=16)

        # Progress Calculation
        current_val, target_val, is_complete = check_mission_progress(active_mission)
        progress_pct = min(1.0, current_val / max(1, target_val))

        # LEFT COLUMN OF CARD (x = card_x + 30)
        m_title = f"{active_mission['id']}. {_(active_mission['title_key'])}"
        m_desc = _(active_mission["desc_key"])

        title_surf = title_font.render(m_title, True, (25, 25, 112))
        screen.blit(title_surf, (card_x + 30, card_y + 25))

        desc_surf = normal_font.render(m_desc, True, (60, 60, 70))
        screen.blit(desc_surf, (card_x + 30, card_y + 80))

        # Status Tag Box
        tag_box = pygame.Rect(card_x + 30, card_y + 140, 480, 45)
        tag_bg = (235, 250, 240) if is_complete else (240, 244, 252)
        tag_border = (46, 139, 87) if is_complete else (100, 149, 237)
        pygame.draw.rect(screen, tag_bg, tag_box, border_radius=8)
        pygame.draw.rect(screen, tag_border, tag_box, width=2, border_radius=8)

        status_txt = f"STATUS: {_('completed')}" if is_complete else f"STATUS: {_('in_progress').format(current=current_val, target=target_val)}"
        status_surf = button_font.render(status_txt, True, (46, 139, 87) if is_complete else (70, 110, 180))
        status_rect = status_surf.get_rect(center=tag_box.center)
        screen.blit(status_surf, status_rect)

        # RIGHT COLUMN OF CARD (x = card_x + 570)
        right_x = card_x + 570
        right_w = card_w - 600

        # Progress Bar Header & Bar
        progress_str = _("progress").format(current=current_val, target=target_val)
        prog_surf = normal_font.render(progress_str, True, (0, 100, 0) if is_complete else (80, 80, 90))
        screen.blit(prog_surf, (right_x, card_y + 25))

        bar_y = card_y + 60
        bar_h = 24
        pygame.draw.rect(screen, (220, 225, 235), (right_x, bar_y, right_w, bar_h), border_radius=8)
        fill_w = int(right_w * progress_pct)
        if fill_w > 0:
            fill_color = (60, 179, 113) if is_complete else (70, 130, 220)
            pygame.draw.rect(screen, fill_color, (right_x, bar_y, fill_w, bar_h), border_radius=8)
        pygame.draw.rect(screen, (140, 150, 170), (right_x, bar_y, right_w, bar_h), width=2, border_radius=8)

        # Reward Badge
        rew_box = pygame.Rect(right_x, card_y + 105, right_w, 48)
        pygame.draw.rect(screen, (255, 252, 235), rew_box, border_radius=10)
        pygame.draw.rect(screen, (218, 165, 32), rew_box, width=2, border_radius=10)

        rew_str = f"{_('reward')}: +{active_mission['reward_money']}$   +{active_mission['reward_exp']} XP"
        rew_surf = button_font.render(rew_str, True, (180, 120, 0))
        rew_rect = rew_surf.get_rect(center=rew_box.center)
        screen.blit(rew_surf, rew_rect)

        # Action / Claim Button
        claim_btn = pygame.Rect(right_x, card_y + 175, right_w, 65)
        if is_complete:
            btn_color = (60, 179, 113) if claim_btn.collidepoint(mouse_pos) else (46, 139, 87)
            btn_txt = _("claim_reward")
        else:
            btn_color = (175, 180, 190)
            btn_txt = _("in_progress").format(current=current_val, target=target_val)

        pygame.draw.rect(screen, btn_color, claim_btn, border_radius=12)
        btn_surf = button_font.render(btn_txt, True, (255, 255, 255))
        btn_rect = btn_surf.get_rect(center=claim_btn.center)
        screen.blit(btn_surf, btn_rect)

        # Handle events for Claim Button
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if is_complete and claim_btn.collidepoint(event.pos):
                    add_reward(active_mission['reward_money'], active_mission['reward_exp'])
                    if active_mission['id'] not in completed_missions:
                        completed_missions.append(active_mission['id'])
                    current_mission += 1
                    _missions_char_index = 0.0
                    if player_data.get("nombre_usuario"):
                        save_progress(player_data["nombre_usuario"])
                    return "misiones"
    else:
        # All missions completed
        completed_surf = title_font.render(_("all_missions_completed"), True, (46, 139, 87))
        screen.blit(completed_surf, (400, 200))

        try:
            toy_img = get_cached_image("toy.png", (200, 187))
            screen.blit(toy_img, (int(_missions_helper_x), 150))
        except pygame.error:
            pass

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if back_btn.collidepoint(event.pos):
                _missions_helper_x = -250.0  # Reset entrance animation for next visit
                return "acciones"

    return "misiones"

def snakegame(screen):
    global _minigame_active, real_screen, real_width, real_height
    _minigame_active = True
    try:
        result = run_snake(screen)
    finally:
        _minigame_active = False
        # Restore the PIXELTOWN virtual-surface display system
        real_screen = pygame.display._original_set_mode((real_width, real_height), pygame.RESIZABLE)
        pygame.display.set_caption("PIXELTOWN")
    return result

def tetrisgame(screen):
    global _minigame_active, real_screen, real_width, real_height
    _minigame_active = True
    try:
        result = run_tetris(screen)
    finally:
        _minigame_active = False
        real_screen = pygame.display._original_set_mode((real_width, real_height), pygame.RESIZABLE)
        pygame.display.set_caption("PIXELTOWN")
    return result

def solarsystem(screen):
    global _minigame_active, real_screen, real_width, real_height
    _minigame_active = True
    try:
        result = run_solarsystem(screen)
    finally:
        _minigame_active = False
        real_screen = pygame.display._original_set_mode((real_width, real_height), pygame.RESIZABLE)
        pygame.display.set_caption("PIXELTOWN")
    return result

def spaceshipgame(screen):
    global _minigame_active, real_screen, real_width, real_height
    _minigame_active = True
    try:
        result = run_spaceship(screen)
    finally:
        _minigame_active = False
        real_screen = pygame.display._original_set_mode((real_width, real_height), pygame.RESIZABLE)
        pygame.display.set_caption("PIXELTOWN")
    return result

def shop_scene(screen, title_font, button_font, events, normal_font):
    screen.fill((255, 255, 255))  # White background
    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"

    # CONSTRUCTION (Bob the builder vibes)
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'construction.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        screen.blit(player_image_scaled, (40, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    construction_button = pygame.Rect(60, 380, 250, 50)
    button_color = (200, 200, 100) if construction_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, construction_button)
    texto_surf = normal_font.render(_("construction"), True, (255, 255, 255))
    texto_rect = texto_surf.get_rect(center=construction_button.center)
    screen.blit(texto_surf, texto_rect)

    # PRODUCTS
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'products.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        screen.blit(player_image_scaled, (440, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    products_button = pygame.Rect(460, 380, 250, 50)
    button_color = (200, 200, 100) if products_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, products_button)
    texto_surf = normal_font.render(_("products"), True, (255, 255, 255))
    texto_rect = texto_surf.get_rect(center=products_button.center)
    screen.blit(texto_surf, texto_rect)

    # DECORATIONS (Make it pretty)
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'decoration.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        screen.blit(player_image_scaled, (840, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    decoration_button = pygame.Rect(860, 380, 250, 50)
    button_color = (200, 200, 100) if decoration_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, decoration_button)
    texto_surf = normal_font.render(_("decorations"), True, (255, 255, 255))
    texto_rect = texto_surf.get_rect(center=decoration_button.center)
    screen.blit(texto_surf, texto_rect)

    # BACK BUTTON
    back_button = pygame.Rect(10, 500, 250, 50)
    button_color = (200, 200, 100) if back_button.collidepoint(mouse_pos) else (97, 175, 14)
    pygame.draw.rect(screen, button_color, back_button)
    texto_surf = normal_font.render(_("back"), True, (255, 255, 255))
    texto_rect = texto_surf.get_rect(center=back_button.center)
    screen.blit(texto_surf, texto_rect)

    # Click Handling
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if construction_button.collidepoint(event.pos):
                print("Cambiando a la escena de construcción...")
                return "construccion"
            elif products_button.collidepoint(event.pos):
                print("Cambiando a la escena de productos...")
                return "productos"
            elif decoration_button.collidepoint(event.pos):
                print("Cambiando a la escena de adornos...")
                return "adorno"
            elif back_button.collidepoint(event.pos):
                return "acciones"

    return "tienda"

def decoration_scene(screen, title_font, button_font, events, normal_font):
    global money, buildings, alert

    screen.fill((245, 247, 252))

    # Top Header Bar
    header_rect = pygame.Rect(0, 0, screen.get_width(), 65)
    pygame.draw.rect(screen, (230, 236, 248), header_rect)
    pygame.draw.line(screen, (200, 210, 230), (0, 65), (screen.get_width(), 65), width=2)

    display_text(screen, title_font, _("decorations"), 170, 18)

    # Player money display in header
    money_str = _("money").format(money=money)
    money_surf = button_font.render(money_str, True, (46, 139, 87))
    screen.blit(money_surf, (screen.get_width() - 250, 18))

    # Back button at top-left
    back_btn = pygame.Rect(20, 12, 130, 40)
    mouse_pos = pygame.mouse.get_pos()
    btn_color = (200, 200, 100) if back_btn.collidepoint(mouse_pos) else (97, 175, 14)
    pygame.draw.rect(screen, btn_color, back_btn, border_radius=8)
    back_surf = normal_font.render(_("back"), True, (255, 255, 255))
    back_rect = back_surf.get_rect(center=back_btn.center)
    screen.blit(back_surf, back_rect)

    # 9 Ornament Keys
    ornament_keys = [
        "farola", "arbusto", "my_town_my_rules",
        "fountain", "tree", "statue",
        "water_feature", "trashcan", "sewer"
    ]

    cols = 3
    col_x = [35, 415, 795]
    row_y = [80, 250, 420]
    card_w = 370
    card_h = 155

    for idx, o_key in enumerate(ornament_keys):
        if o_key not in BUILDINGS_CONFIG:
            continue
        cfg = BUILDINGS_CONFIG[o_key]

        c = idx % cols
        r = idx // cols

        cx = col_x[c]
        cy = row_y[r]

        card_rect = pygame.Rect(cx, cy, card_w, card_h)
        is_hover = card_rect.collidepoint(mouse_pos)

        # Card Background
        pygame.draw.rect(screen, (255, 255, 255), card_rect, border_radius=12)
        border_col = (100, 149, 237) if is_hover else (200, 210, 230)
        pygame.draw.rect(screen, border_col, card_rect, width=2, border_radius=12)

        # Left Side: Ornament Image Box (95x95)
        img_box = pygame.Rect(cx + 12, cy + 30, 95, 95)
        pygame.draw.rect(screen, (245, 248, 255), img_box, border_radius=8)
        pygame.draw.rect(screen, (220, 230, 245), img_box, width=1, border_radius=8)

        try:
            o_img = get_cached_image(os.path.basename(cfg["imagen"]), (85, 85))
            img_rect = o_img.get_rect(center=img_box.center)
            screen.blit(o_img, img_rect)
        except pygame.error:
            pass

        # Right Side Information
        text_x = cx + 118
        o_name = get_building_name(o_key)
        cost = cfg["costo"]
        exp = cfg["experiencia"]

        # Title
        t_surf = title_font.render(o_name, True, (25, 25, 100))
        screen.blit(t_surf, (text_x, cy + 12))

        # Price Badge
        cost_txt = _("cost_amount").format(cost=cost)
        cost_surf = normal_font.render(cost_txt, True, (200, 140, 0))
        screen.blit(cost_surf, (text_x, cy + 45))

        # EXP Reward Badge
        exp_txt = f"+{exp} XP"
        exp_surf = normal_font.render(exp_txt, True, (46, 139, 87))
        screen.blit(exp_surf, (text_x, cy + 74))

        # Count Badge (e.g. 0/5)
        current_count = sum(1 for b in buildings if b.get("tipo") == o_key)
        count_txt = f"{current_count}/5"
        count_col = (200, 40, 40) if current_count >= 5 else (100, 110, 140)
        count_surf = normal_font.render(count_txt, True, count_col)
        screen.blit(count_surf, (cx + 310, cy + 45))

        # Action / Build Button (cx + 118, cy + 104, w = 240, h = 38)
        build_btn = pygame.Rect(text_x, cy + 104, 240, 38)
        is_limit_reached = current_count >= 5
        can_afford = money >= cost

        if is_limit_reached:
            btn_col = (180, 185, 195)
            b_txt = _("limit_reached")
        elif can_afford:
            btn_col = (60, 179, 113) if build_btn.collidepoint(mouse_pos) else (46, 139, 87)
            b_txt = _("build_action")
        else:
            btn_col = (180, 185, 195)
            b_txt = _("build_action")

        pygame.draw.rect(screen, btn_col, build_btn, border_radius=8)
        b_surf = normal_font.render(b_txt, True, (255, 255, 255))
        b_rect = b_surf.get_rect(center=build_btn.center)
        screen.blit(b_surf, b_rect)

        # Click handling for this ornament
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if build_btn.collidepoint(event.pos):
                    if is_limit_reached:
                        alert = [_("ornament_limit_reached"), 60]
                        print(_("ornament_limit_reached"))
                    elif not can_afford:
                        alert = [_("not_enough_money"), 60]
                        print(_("not_enough_money"))
                    else:
                        return "colocando_edificio", o_key

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if back_btn.collidepoint(event.pos):
                return "tienda"

    return "adorno"

def info_scene(screen, title_font, button_font, events, normal_font):
    screen.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    info_text_1(screen, title_font, 20, 20)

    mouse_pos = pygame.mouse.get_pos()

    next_button = pygame.Rect(930, 520, 250, 45)
    button_color = (200, 200, 100) if next_button.collidepoint(mouse_pos) else (97, 175, 14)
    pygame.draw.rect(screen, button_color, next_button, border_radius=6)
    texto_surf_boton = normal_font.render(_("next"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=next_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)

    back_button = pygame.Rect(20, 520, 250, 45)
    button_color = (200, 200, 100) if back_button.collidepoint(mouse_pos) else (97, 175, 14)
    pygame.draw.rect(screen, button_color, back_button, border_radius=6)
    texto_surf_boton = normal_font.render(_("back"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=back_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if next_button.collidepoint(event.pos):
                print("Cambiando a la escena infodos...")
                return "infodos"
            elif back_button.collidepoint(event.pos):
                print("Cambiando a mapa inicial")
                return "mapainicial"

    return "info"


def info_two_scene(screen, title_font, button_font, events, normal_font):
    screen.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    info_text_2(screen, title_font, 20, 20)

    mouse_pos = pygame.mouse.get_pos()

    # Back button to previous info page
    back_button = pygame.Rect(20, 520, 250, 45)
    back_color = (200, 200, 100) if back_button.collidepoint(mouse_pos) else (97, 175, 14)
    pygame.draw.rect(screen, back_color, back_button, border_radius=6)
    texto_surf_volver = normal_font.render(_("back"), True, (255, 255, 255))
    texto_rect_volver = texto_surf_volver.get_rect(center=back_button.center)
    screen.blit(texto_surf_volver, texto_rect_volver)

    # Discord button (opens https://discord.gg/fdPHVKyWC3)
    discord_button = pygame.Rect(450, 520, 300, 45)
    discord_color = (114, 137, 218) if discord_button.collidepoint(mouse_pos) else (88, 101, 242)
    pygame.draw.rect(screen, discord_color, discord_button, border_radius=6)
    discord_text_surf = normal_font.render(_("discord_button"), True, (255, 255, 255))
    discord_text_rect = discord_text_surf.get_rect(center=discord_button.center)
    screen.blit(discord_text_surf, discord_text_rect)

    # Back to city button
    city_button = pygame.Rect(930, 520, 250, 45)
    city_color = (200, 200, 100) if city_button.collidepoint(mouse_pos) else (97, 175, 14)
    pygame.draw.rect(screen, city_color, city_button, border_radius=6)
    city_surf = normal_font.render(_("back_to_city"), True, (255, 255, 255))
    city_rect = city_surf.get_rect(center=city_button.center)
    screen.blit(city_surf, city_rect)

    # Exit button 'X' at top right
    exit_button = pygame.Rect(1130, 20, 50, 50)
    exit_hover = exit_button.collidepoint(mouse_pos)
    pygame.draw.rect(screen, (255, 80, 80) if exit_hover else (255, 100, 100), exit_button, border_radius=6)
    x_font = pygame.font.Font(None, 38 if exit_hover else 30)
    x_surf = x_font.render("X", True, (255, 255, 255))
    x_rect = x_surf.get_rect(center=exit_button.center)
    screen.blit(x_surf, x_rect)

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if exit_button.collidepoint(event.pos) or city_button.collidepoint(event.pos):
                return "mapainicial"
            elif back_button.collidepoint(event.pos):
                return "info"
            elif discord_button.collidepoint(event.pos):
                import webbrowser
                webbrowser.open("https://discord.gg/fdPHVKyWC3")

    return "infodos"


def products_scene(screen, title_font, button_font, events, normal_font):
    global money, happiness, experience, alert, buildings

    has_tarraco = any(b.get("tipo") == "tarraco" for b in buildings)

    screen.fill((255, 255, 255))  # White background
    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"

    # Warning banner if Tarraco is not built yet
    if not has_tarraco:
        warn_rect = pygame.Rect(40, 20, screen.get_width() - 80, 50)
        pygame.draw.rect(screen, (255, 235, 235), warn_rect, border_radius=8)
        pygame.draw.rect(screen, (220, 50, 50), warn_rect, width=2, border_radius=8)
        warn_surf = normal_font.render(_("tarraco_required_warning"), True, (200, 30, 30))
        warn_rect_inner = warn_surf.get_rect(center=warn_rect.center)
        screen.blit(warn_surf, warn_rect_inner)

    # HAND SOAP (Clean hands are happy hands)
    buy_button = pygame.Rect(100, 390, 310, 50)
    if has_tarraco:
        button_color = (200, 200, 100) if buy_button.collidepoint(mouse_pos) else (200, 200, 50)
    else:
        button_color = (180, 180, 180)

    pygame.draw.rect(screen, button_color, buy_button, border_radius=8)
    texto_surf_boton = normal_font.render(_("hand_soap"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=buy_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if buy_button.collidepoint(event.pos):
                if not has_tarraco:
                    alert = [ _("tarraco_required_warning"), 3 ]
                    print(_("tarraco_required_warning"))
                else:
                    print("Comprando producto...")
                    if money >= 250:
                        money -= 250
                        happiness += 5
                        experience += 10
                        print(_("purchase_success"))
                        return "mapainicial"
                    else:
                        print(_("insufficient_money"))
                        return "mapainicial"
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'lovyc.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (500, 300))
        screen.blit(player_image_scaled, (10, 100))
    except pygame.error:
        print("Error cargando imagen")
        pass

    # FACE MASK IMAGE
    mask_button = pygame.Rect(700, 390, 310, 50)
    if has_tarraco:
        button_color = (200, 200, 100) if mask_button.collidepoint(mouse_pos) else (200, 200, 50)
    else:
        button_color = (180, 180, 180)

    pygame.draw.rect(screen, button_color, mask_button, border_radius=8)
    texto_surf_boton = normal_font.render(_("face_mask"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=mask_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if mask_button.collidepoint(event.pos):
                if not has_tarraco:
                    alert = [ _("tarraco_required_warning"), 3 ]
                    print(_("tarraco_required_warning"))
                else:
                    print("Comprando producto...")
                    if money >= 150:
                        money -= 150
                        happiness += 5
                        experience += 10
                        print(_("purchase_success"))
                        return "mapainicial"
                    else:
                        print(_("insufficient_money"))
                        return "mapainicial"
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'lovyc_mask.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        screen.blit(player_image_scaled, (700, 100))
    except pygame.error:
        pass
    
    # EXIT / BACK BUTTON
    back_button = pygame.Rect(50, 500, 250, 50)
    button_color = (200, 200, 100) if back_button.collidepoint(mouse_pos) else (97, 175, 14)
    pygame.draw.rect(screen, button_color, back_button, border_radius=8)
    texto_surf_boton = normal_font.render(_("back"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=back_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if back_button.collidepoint(event.pos):
                return "tienda"

    # NEXT BUTTON
    next_button = pygame.Rect(900, 500, 250, 50)
    button_color = (200, 200, 100) if next_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, next_button, border_radius=8)
    texto_surf_boton = normal_font.render(_("next"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=next_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if next_button.collidepoint(event.pos):
                return "productos2"
    
    return "productos"

def products_two_scene(screen, title_font, button_font, events, normal_font):
    global money, happiness, experience, alert, buildings

    has_tarraco = any(b.get("tipo") == "tarraco" for b in buildings)

    screen.fill((255, 255, 255))
    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"

    # Warning banner if Tarraco is not built yet
    if not has_tarraco:
        warn_rect = pygame.Rect(40, 20, screen.get_width() - 80, 50)
        pygame.draw.rect(screen, (255, 235, 235), warn_rect, border_radius=8)
        pygame.draw.rect(screen, (220, 50, 50), warn_rect, width=2, border_radius=8)
        warn_surf = normal_font.render(_("tarraco_required_warning"), True, (200, 30, 30))
        warn_rect_inner = warn_surf.get_rect(center=warn_rect.center)
        screen.blit(warn_surf, warn_rect_inner)
    
    # SHAMPOO IMAGE
    shampoo_button = pygame.Rect(700, 390, 310, 50)
    if has_tarraco:
        button_color = (200, 200, 100) if shampoo_button.collidepoint(mouse_pos) else (200, 200, 50)
    else:
        button_color = (180, 180, 180)

    pygame.draw.rect(screen, button_color, shampoo_button, border_radius=8)
    texto_surf_boton = normal_font.render(_("shampoo"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=shampoo_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if shampoo_button.collidepoint(event.pos):
                if not has_tarraco:
                    alert = [ _("tarraco_required_warning"), 3 ]
                    print(_("tarraco_required_warning"))
                else:
                    print("Comprando producto...")
                    if money >= 200:
                        money -= 200
                        happiness += 10
                        experience += 10
                        print(_("purchase_success"))
                        return "mapainicial"
                    else:
                        print(_("insufficient_money"))
                        return "mapainicial"
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'lovyc_shampoo.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        screen.blit(player_image_scaled, (700, 100))
    except pygame.error:
        pass

    # WIPES IMAGE
    buy_button = pygame.Rect(100, 390, 310, 50)
    if has_tarraco:
        button_color = (200, 200, 100) if buy_button.collidepoint(mouse_pos) else (200, 200, 50)
    else:
        button_color = (180, 180, 180)

    pygame.draw.rect(screen, button_color, buy_button, border_radius=8)
    texto_surf_boton = normal_font.render(_("wipes"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=buy_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if buy_button.collidepoint(event.pos):
                if not has_tarraco:
                    alert = [ _("tarraco_required_warning"), 3 ]
                    print(_("tarraco_required_warning"))
                else:
                    print("Comprando producto...")
                    if money >= 100:
                        money -= 100
                        happiness += 5
                        experience += 10
                        print(_("purchase_success"))
                        return "mapainicial"
                    else:
                        print(_("insufficient_money"))
                        return "mapainicial"
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'lovyc_wipes.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (500, 300))
        screen.blit(player_image_scaled, (10, 100))
    except pygame.error:
        pass

    # BACK BUTTON (to previous products page)
    back_button = pygame.Rect(50, 500, 250, 50)
    button_color = (200, 200, 100) if back_button.collidepoint(mouse_pos) else (97, 175, 14)
    pygame.draw.rect(screen, button_color, back_button, border_radius=8)
    texto_surf_boton = normal_font.render(_("back"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=back_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if back_button.collidepoint(event.pos):
                return "productos"

    # EXIT / RETURN TO SHOP BUTTON
    exit_button = pygame.Rect(900, 500, 250, 50)
    button_color = (200, 200, 100) if exit_button.collidepoint(mouse_pos) else (97, 175, 14)
    pygame.draw.rect(screen, button_color, exit_button, border_radius=8)
    texto_surf_boton = normal_font.render(_("back_to_menu"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=exit_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if exit_button.collidepoint(event.pos):
                return "tienda"
    
    return "productos2"

def construction_scene(screen, title_font, button_font, events, normal_font):
    global money

    screen.fill((245, 247, 252))

    # Top Header Bar
    header_rect = pygame.Rect(0, 0, screen.get_width(), 65)
    pygame.draw.rect(screen, (230, 236, 248), header_rect)
    pygame.draw.line(screen, (200, 210, 230), (0, 65), (screen.get_width(), 65), width=2)

    display_text(screen, title_font, _("construction"), 170, 18)

    # Player money display in header
    money_str = _("money").format(money=money)
    money_surf = button_font.render(money_str, True, (46, 139, 87))
    screen.blit(money_surf, (screen.get_width() - 250, 18))

    # Back button at top-left
    back_btn = pygame.Rect(20, 12, 130, 40)
    mouse_pos = pygame.mouse.get_pos()
    btn_color = (200, 200, 100) if back_btn.collidepoint(mouse_pos) else (97, 175, 14)
    pygame.draw.rect(screen, btn_color, back_btn, border_radius=8)
    back_surf = normal_font.render(_("back"), True, (255, 255, 255))
    back_rect = back_surf.get_rect(center=back_btn.center)
    screen.blit(back_surf, back_rect)

    # 9 Building Keys
    building_keys = [
        "house", "mailoffice", "supermarket", 
        "restaurant", "gym", "tarraco", 
        "school", "policestation", "townhall"
    ]

    cols = 3
    col_x = [35, 415, 795]
    row_y = [80, 250, 420]
    card_w = 370
    card_h = 155

    for idx, b_key in enumerate(building_keys):
        if b_key not in BUILDINGS_CONFIG:
            continue
        cfg = BUILDINGS_CONFIG[b_key]

        c = idx % cols
        r = idx // cols

        cx = col_x[c]
        cy = row_y[r]

        card_rect = pygame.Rect(cx, cy, card_w, card_h)
        is_hover = card_rect.collidepoint(mouse_pos)

        # Card Background
        pygame.draw.rect(screen, (255, 255, 255), card_rect, border_radius=12)
        border_col = (100, 149, 237) if is_hover else (200, 210, 230)
        pygame.draw.rect(screen, border_col, card_rect, width=2, border_radius=12)

        # Left Side: Building Image Box (95x95)
        img_box = pygame.Rect(cx + 12, cy + 30, 95, 95)
        pygame.draw.rect(screen, (245, 248, 255), img_box, border_radius=8)
        pygame.draw.rect(screen, (220, 230, 245), img_box, width=1, border_radius=8)

        try:
            b_img = get_cached_image(os.path.basename(cfg["imagen"]), (85, 85))
            img_rect = b_img.get_rect(center=img_box.center)
            screen.blit(b_img, img_rect)
        except pygame.error:
            pass

        # Right Side Information
        text_x = cx + 118
        b_name = get_building_name(b_key)
        cost = cfg["costo"]
        exp = cfg["experiencia"]

        # Title
        t_surf = title_font.render(b_name, True, (25, 25, 100))
        screen.blit(t_surf, (text_x, cy + 12))

        # Price Badge
        cost_txt = _("cost_amount").format(cost=cost)
        cost_surf = normal_font.render(cost_txt, True, (200, 140, 0))
        screen.blit(cost_surf, (text_x, cy + 45))

        # EXP Reward Badge
        exp_txt = f"+{exp} XP"
        exp_surf = normal_font.render(exp_txt, True, (46, 139, 87))
        screen.blit(exp_surf, (text_x, cy + 74))

        # Action / Build Button (cx + 118, cy + 104, w = 240, h = 38)
        build_btn = pygame.Rect(text_x, cy + 104, 240, 38)
        can_afford = money >= cost
        if can_afford:
            btn_col = (60, 179, 113) if build_btn.collidepoint(mouse_pos) else (46, 139, 87)
        else:
            btn_col = (180, 185, 195)

        pygame.draw.rect(screen, btn_col, build_btn, border_radius=8)
        b_txt = _("build_action")
        b_surf = normal_font.render(b_txt, True, (255, 255, 255))
        b_rect = b_surf.get_rect(center=build_btn.center)
        screen.blit(b_surf, b_rect)

        # Click handling for this building
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if build_btn.collidepoint(event.pos):
                    return "colocando_edificio", b_key

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if back_btn.collidepoint(event.pos):
                return "tienda"

    return "construccion"


def placement_scene(screen, events, normal_font, building_type):
    global buildings, money, experience, alert

    if building_type not in BUILDINGS_CONFIG:
        print(f"Error: Tipo de edificio '{building_type}' desconocido.")
        return "construccion"

    is_ornament = building_type in ORNAMENT_KEYS
    cancel_scene = "adorno" if is_ornament else "construccion"

    config = BUILDINGS_CONFIG[building_type]
    image_path = config["imagen"]
    cost = config["costo"]
    exp_reward = config["experiencia"]

    # background/map
    screen.fill((255, 255, 255))
    try:
        rio_img = get_cached_image('river.png', (300, 300))
        screen.blit(rio_img, (450, 200))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")

    # River zone — buildings cannot be placed here
    RIO_RECT = pygame.Rect(488, 223, 250, 265)

    display_text(screen, normal_font, _("money").format(money=money), 10, 10)
    display_text(screen, normal_font, _("buildings_short").format(count=len(buildings)), 10, 40)
    display_text(screen, normal_font, _("experience").format(experience=experience), 10, 70)
    display_text(screen, normal_font, _("debt").format(debt=debt), 10, 100)
    display_text(screen, normal_font, _("level").format(level=level), 10, 130)

    # Dynamic image dictionary from BUILDINGS_CONFIG
    building_images = {}
    for b_type, b_cfg in BUILDINGS_CONFIG.items():
        try:
            building_images[b_type] = get_cached_image(os.path.basename(b_cfg["imagen"]), (64, 64))
        except pygame.error:
            pass

    for ed in buildings:
        if ed["tipo"] in building_images:
            screen.blit(building_images[ed["tipo"]], ed["pos"])

    # Ghost building preview with fluid tracking & placement validity indicator
    mouse_pos = pygame.mouse.get_pos()
    ghost_pos = (mouse_pos[0] - 32, mouse_pos[1] - 32)
    building_rect = pygame.Rect(ghost_pos[0], ghost_pos[1], 64, 64)
    is_invalid = building_rect.colliderect(RIO_RECT)

    try:
        base_ghost = get_cached_image(image_path, (64, 64))
        ghost = base_ghost.copy()
        if is_invalid:
            # Soft red tint when hovering over invalid terrain (river)
            red_overlay = pygame.Surface((64, 64), pygame.SRCALPHA)
            red_overlay.fill((255, 50, 50, 120))
            ghost.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            ghost.set_alpha(190)
        else:
            ghost.set_alpha(180)
        screen.blit(ghost, ghost_pos)
    except pygame.error:
        pass

    display_text(screen, normal_font,
                 _("placement_hint").format(cost=cost),
                 10, screen.get_height() - 30)

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if is_ornament and sum(1 for b in buildings if b.get("tipo") == building_type) >= 5:
                    print(_("ornament_limit_reached"))
                    alert = [_("ornament_limit_reached"), 60]
                    return "adorno"
                if money >= cost:
                    final_pos = ghost_pos
                    if is_invalid:
                        print(_("cannot_build_on_river"))
                        alert = [_("cannot_build_on_river"), 60]
                    else:
                        buildings.append({"tipo": building_type, "pos": final_pos})
                        money -= cost
                        experience += exp_reward
                        print(_("building_built").format(type=get_building_name(building_type), pos=final_pos, exp=exp_reward))
                        return "mapainicial"
                else:
                    print(_("not_enough_money"))
                    return cancel_scene
            if event.button == 3:
                print(_("placement_cancelled"))
                return cancel_scene
    return "colocando_edificio"

def billing_scene(screen, title_font, button_font, events, normal_font, player_data):
    global money, experience, happiness, population
    screen.fill((255, 255, 255))  # White background (Maybe a bit too bright?)
    # COLLECT TAXES
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'taxes.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        screen.blit(player_image_scaled, (40, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    taxes_button = pygame.Rect(60, 380, 250, 50)
    mouse_pos = pygame.mouse.get_pos()
    button_color = (200, 200, 100) if taxes_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, taxes_button)
    texto_surf_boton = normal_font.render(_("collect_taxes"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=taxes_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            if taxes_button.collidepoint(event.pos):
                print("Cambiando a la escena de cobrar impuestos...")
                return "impuestos"

    # SELL
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'sell_building.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        screen.blit(player_image_scaled, (440, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    sell_building_button = pygame.Rect(460, 380, 250, 50)
    button_color = (200, 200, 100) if sell_building_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, sell_building_button)
    texto_surf_boton = normal_font.render(_("sell_building"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=sell_building_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            if sell_building_button.collidepoint(event.pos):
                print("Cambiando a la escena de vender edificio...")
                return "vender_edificio"

    # ASK FOR A LOAN (Please don't go bankrupt)
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'loan.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (300, 300))
        screen.blit(player_image_scaled, (840, 100))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    loan_button = pygame.Rect(860, 380, 250, 50)
    button_color = (200, 200, 100) if loan_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, loan_button)
    texto_surf_boton = normal_font.render(_("ask_loan"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=loan_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            if loan_button.collidepoint(event.pos):
                print("Cambiando a la escena de pedir préstamo...")
                return "prestamo"

    return "facturar"

def sell_building_scene(screen, title_font, button_font, events, normal_font):
    global money, experience, buildings, debt
    screen.fill((255, 255, 255))
    display_text(screen, title_font, _("sell_building"), 10, 10)
    display_text(screen, normal_font, _("click_building_to_sell"), 10, 44)

    mouse_pos = pygame.mouse.get_pos()
    building_rects = []
    y_list = 90
    display_text(screen, normal_font, _("available_buildings"), 10, y_list)
    y_list += 30

    # Load building images for the sell screen
    building_images = {}
    for tipo, config in BUILDINGS_CONFIG.items():
        try:
            building_images[tipo] = pygame.transform.scale(
                pygame.image.load(config["imagen"]).convert_alpha(),
                (64, 64)
            )
        except pygame.error:
            building_images[tipo] = None

    for idx, ed in enumerate(buildings):
        tipo = ed["tipo"]
        pos = ed["pos"]
        rect = pygame.Rect(pos[0], pos[1], 64, 64)
        building_rects.append((rect, ed))

        if tipo in building_images and building_images[tipo] is not None:
            screen.blit(building_images[tipo], pos)
        else:
            pygame.draw.rect(screen, (200, 200, 200), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        precio_venta = get_sell_price(tipo)
        nombre = get_building_name(tipo)
        texto_info = _("sells_for").format(name=nombre, price=precio_venta)
        texto_surf = normal_font.render(texto_info, True, (0, 0, 0))
        screen.blit(texto_surf, (pos[0], pos[1] + 70))

        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 0, 0), rect, 3)
            sell_msg = _("click_to_sell").format(name=nombre, price=precio_venta)
            display_text(screen, normal_font, sell_msg, 10, 70)

        lista_texto = f"{idx + 1}. {nombre}: {precio_venta}"
        texto_surf = normal_font.render(lista_texto, True, (0, 0, 0))
        screen.blit(texto_surf, (10, y_list + idx * 28))

    if not buildings:
        display_text(screen, normal_font, _("no_buildings_to_sell"), 10, 120)

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos_click = event.pos
            for rect, ed in building_rects:
                if rect.collidepoint(pos_click):
                    building_type = ed["tipo"]
                    if building_type in BUILDINGS_CONFIG:
                        precio_venta = get_sell_price(building_type)
                        if debt > 0:
                            if precio_venta >= debt:
                                money += (precio_venta - debt)
                                print(_("loan_repaid").format(amount=debt))
                                debt = 0
                            else:
                                debt -= precio_venta
                                print(_("loan_partially_repaid").format(amount=precio_venta, remaining=debt))
                        else:
                            money += precio_venta
                        experience += get_sell_experience(building_type)
                        buildings.remove(ed)
                        print(_("building_sold").format(type=get_building_name(building_type), price=precio_venta))
                        return "mapainicial"
                    else:
                        print(f"Error: Tipo de edificio '{building_type}' desconocido.")
    return "vender_edificio"

def minigames_scene(screen, title_font, button_font, events, normal_font):
    screen.fill((255, 255, 255))  # White background
    display_text(screen, title_font, _("minigames"), 10, 10)
    mouse_pos = pygame.mouse.get_pos()

    # SNAKE GAME
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'snakelogo.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (240, 240))
        screen.blit(player_image_scaled, (40, 90))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    snake_button = pygame.Rect(40, 350, 240, 45)
    button_color = (200, 200, 100) if snake_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, snake_button)
    texto_surf_boton = normal_font.render(_("snakegame"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=snake_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            if snake_button.collidepoint(event.pos):
                print("Cargando el juego de la serpiente...")
                return "snakegame"
        if event.type == pygame.QUIT:
            return "salir"

    # TETRIS GAME
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'tetrislogo.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (240, 240))
        screen.blit(player_image_scaled, (330, 90))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    tetris_button = pygame.Rect(330, 350, 240, 45)
    button_color = (200, 200, 100) if tetris_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, tetris_button)
    texto_surf_boton = normal_font.render(_("tetrisgame"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=tetris_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            if tetris_button.collidepoint(event.pos):
                print("Cargando tetris...")
                return "tetrisgame"
        if event.type == pygame.QUIT:
            return "salir"

    # SOLAR SYSTEM SIMULATOR
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'solarsystemlogo.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (240, 240))
        screen.blit(player_image_scaled, (620, 90))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    solarsystem_button = pygame.Rect(620, 350, 240, 45)
    button_color = (200, 200, 100) if solarsystem_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, solarsystem_button)
    texto_surf_boton = normal_font.render(_("solarsystem"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=solarsystem_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            if solarsystem_button.collidepoint(event.pos):
                print("Cargando simulador del sistema solar...")
                return "solarsystem"

    # SPACESHIP GAME
    try:
        player_image = pygame.image.load(os.path.join(IMAGES_DIR, 'spaceshiplogo.png')).convert_alpha()
        player_image_scaled = pygame.transform.scale(player_image, (240, 240))
        screen.blit(player_image_scaled, (910, 90))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
    spaceship_button = pygame.Rect(910, 350, 240, 45)
    button_color = (200, 200, 100) if spaceship_button.collidepoint(mouse_pos) else (200, 200, 50)
    pygame.draw.rect(screen, button_color, spaceship_button)
    texto_surf_boton = normal_font.render(_("spaceshipgame"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=spaceship_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            if spaceship_button.collidepoint(event.pos):
                print("Cargando batalla espacial...")
                return "spaceshipgame"

    back_button = pygame.Rect(40, 490, 240, 45)
    button_color = (200, 200, 100) if back_button.collidepoint(mouse_pos) else (97, 175, 14)
    pygame.draw.rect(screen, button_color, back_button)
    texto_surf_boton = normal_font.render(_("back"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=back_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            if back_button.collidepoint(event.pos):
                print("Cambiando a mapa inicial")
                return "mapainicial"

    return "minijuegos"

def loan_scene(screen, title_font, normal_font, events, player_data, textbox_state, loan_data):
    global money, happiness, experience, debt
    
    input_box = pygame.Rect(screen.get_width() // 2 - 200, 300, 400, 40)
    inactive_color = pygame.Color('lightskyblue3')
    active_color = pygame.Color('dodgerblue2')

    user_text = textbox_state['texto']
    active = textbox_state['activo']
    color = active_color if active else inactive_color

    back_button = pygame.Rect(screen.get_width() // 2 - 125, 500, 250, 50)

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                return "menu"
            active = input_box.collidepoint(event.pos)
        if active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_text.isdigit(): 
                    amount_int = int(user_text)
                    
                    print(f"Respuesta enviada: {amount_int}")
                    if amount_int > money * 1.3:
                        debt_limit_msg = _("debt_limit")
                        print(debt_limit_msg)
                        return "mapainicial"
                    loan_data['cantidad'] = amount_int
                    loan_data['deuda'] = loan_data.get('deuda', 0) + amount_int
                    
                    money += amount_int
                    experience += 15
                    debt += amount_int
                    user_text = ""
                    active = False
                    return "mapainicial"
                else:
                    print("Por favor, introduce un número válido.")
                    
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                # Avoid characters
                if event.unicode.isdigit(): 
                    user_text += event.unicode

    textbox_state['texto'] = user_text
    textbox_state['activo'] = active

    screen.fill((220, 220, 255))
    
    # render 'user_text'
    question_lines = _("borrow_question").split('\n') # Pygame doesn't know about \n by itself
    current_y = 180
    for line in question_lines:
        texto_pregunta_surf = title_font.render(line, True, (0, 0, 0))
        texto_pregunta_rect = texto_pregunta_surf.get_rect(center=(screen.get_width() // 2, current_y))
        screen.blit(texto_pregunta_surf, texto_pregunta_rect)
        current_y += texto_pregunta_surf.get_height() + 5

    text_surf = normal_font.render(user_text, True, (0, 0, 0))
    input_box.w = max(400, text_surf.get_width() + 20)
    pygame.draw.rect(screen, color, input_box, 2)
    screen.blit(text_surf, (input_box.x + 10, input_box.y + 10))

    mouse_pos = pygame.mouse.get_pos()
    button_color = (255, 100, 100) if back_button.collidepoint(mouse_pos) else (200, 50, 50)
    pygame.draw.rect(screen, button_color, back_button)
    texto_surf_boton = normal_font.render(_("back_to_menu"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=back_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    return "prestamo"

def taxes_scene(screen, title_font, normal_font, events, player_data, textbox_state, tax_data):
    global money, happiness, experience, debt
    input_box = pygame.Rect(screen.get_width() // 2 - 200, 300, 400, 40)
    inactive_color = pygame.Color('lightskyblue3')
    active_color = pygame.Color('dodgerblue2')

    user_text = textbox_state['texto']
    active = textbox_state['activo']
    color = active_color if active else inactive_color

    back_button = pygame.Rect(screen.get_width() // 2 - 125, 500, 250, 50)

    for event in events:
        if event.type == pygame.QUIT:
            return "salir"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                return "menu"
            active = input_box.collidepoint(event.pos)

        if active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(f"Respuesta enviada: {user_text}")
                tax_data['porcentaje'] = user_text
                user_text = ""
                tax_to_pay = population * money_per_inhabitant * (int(tax_data['porcentaje']) / 100)
                print(_("tax_collected").format(amount=tax_to_pay))
                int_tax_to_pay = int(tax_to_pay)
                if (debt > 0):
                    for i in range(int(tax_to_pay)):
                        debt -= 1
                        int_tax_to_pay -= 1
                money += int_tax_to_pay
                happiness -= 10
                experience += 15
                active = False
                return "mapainicial"
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    textbox_state['texto'] = user_text
    textbox_state['activo'] = active

    screen.fill((220, 220, 255))
    porcentaje = tax_data.get('porcentaje', '0')
    texto_pregunta_surf = title_font.render(_("tax_question"), True, (0, 0, 0))
    texto_pregunta_rect = texto_pregunta_surf.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(texto_pregunta_surf, texto_pregunta_rect)

    text_surf = normal_font.render(user_text, True, (0, 0, 0))
    input_box.w = max(400, text_surf.get_width() + 20)
    pygame.draw.rect(screen, color, input_box, 2)
    screen.blit(text_surf, (input_box.x + 10, input_box.y + 10))

    mouse_pos = pygame.mouse.get_pos()
    button_color = (255, 100, 100) if back_button.collidepoint(mouse_pos) else (200, 50, 50)
    pygame.draw.rect(screen, button_color, back_button)
    texto_surf_boton = normal_font.render(_("back_to_menu"), True, (255, 255, 255))
    texto_rect_boton = texto_surf_boton.get_rect(center=back_button.center)
    screen.blit(texto_surf_boton, texto_rect_boton)
    return "impuestos"

def gameover_scene(screen, events):
    global mouseDown, w, h

    screen.fill((180,0,0))

    text = pygame.font.Font(None, 128).render("GAME OVER", True, (255,255,255))
    textpos = text.get_rect(centerx=w*0.5, centery=h*0.4)
    screen.blit(text, textpos)

    text = pygame.font.Font(None, 32).render(_("citizens_unhappy"), True, (255,255,255))
    textpos = text.get_rect(centerx=w*0.5, centery=h*0.5)
    screen.blit(text, textpos)

    text = pygame.font.Font(None, 32).render(_("coup_started"), True, (255,255,255))
    textpos = text.get_rect(centerx=w*0.5, centery=h*0.6)
    screen.blit(text, textpos)

    quit_button = pygame.Rect(w*0.4, h*0.7, w*0.2, h*0.2)
    pygame.draw.rect(screen, (255, 100, 100), quit_button)

    text = pygame.font.Font(None, 30).render("Quit", True, (255,255,255))

    if quit_button.collidepoint(pygame.mouse.get_pos()):
        text = pygame.font.Font(None, 38).render("Quit", True, (255,255,255))

        if pygame.mouse.get_pressed()[0] and not mouseDown:
            return "salir"

    textpos = text.get_rect(centerx=quit_button.centerx, centery=quit_button.centery)
    screen.blit(text, textpos)

    for event in events:
        if event.type == pygame.QUIT:
            print("hi")
            return "salir"

    pygame.display.flip()

   # MAIN FUNCTION
def main(username=None):
    global logged_in_username, player_data, mouseDown, w, h
    logged_in_username = username

    progress_loaded = False
    if username:
        progress_loaded = load_progress(username)

    if not progress_loaded:
        player_data.clear()
        player_data.update({"nombre_usuario": "", "nombre_ciudad": ""})

    pygame.init()

    # PIXELTOWN logo, only visible for Windows users (I'm an x11/Wayland Ubuntu user, so I blindly trust in this process)
    if sys.platform.startswith('win32'):
        try:
            icon_path = os.path.join(IMAGES_DIR, 'pixeltown_logo.png')
            icon = pygame.image.load(icon_path)
            scaled_icon = pygame.transform.scale(icon, (32, 32))
            pygame.display.set_icon(scaled_icon)
        except pygame.error:
            print("No se pudo encontrar el logo, se usará el de por defecto.")

    global real_screen, real_width, real_height
    virtual_surface = pygame.Surface((w, h))

    _original_set_mode = pygame.display.set_mode
    _original_flip = pygame.display.flip
    _original_update = pygame.display.update
    _original_get_pos = pygame.mouse.get_pos
    _original_event_get = pygame.event.get

    global _minigame_active
    _minigame_active = False
    initial_setup = True
    pending_size = None
    last_resize_time = 0

    def custom_set_mode(size, flags=0, *args, **kwargs):
        global real_screen, real_width, real_height
        nonlocal initial_setup
        if _minigame_active:
            return _original_set_mode(size, flags, *args, **kwargs)
        if size == (w, h) and initial_setup:
            initial_setup = False
            real_screen = _original_set_mode((w, h), flags | pygame.RESIZABLE, *args, **kwargs)
            real_width, real_height = w, h
            return virtual_surface
        elif size == (w, h) and not initial_setup:
            real_screen = _original_set_mode((real_width, real_height), flags | pygame.RESIZABLE, *args, **kwargs)
            return real_screen
        else:
            return _original_set_mode(size, flags, *args, **kwargs)

    def custom_flip():
        global real_screen, real_width, real_height
        nonlocal pending_size, last_resize_time
        if _minigame_active:
            _original_flip()
            return
        if pending_size is not None and (time.time() - last_resize_time) > 0.15:
            real_screen = _original_set_mode(pending_size, pygame.RESIZABLE)
            real_width, real_height = pending_size
            pending_size = None
        if pygame.display.get_surface() == real_screen and real_screen is not None:
            pygame.transform.scale(virtual_surface, real_screen.get_size(), real_screen)
        _original_flip()

    def custom_update(*args, **kwargs):
        global real_screen, real_width, real_height
        nonlocal pending_size, last_resize_time
        if _minigame_active:
            _original_update(*args, **kwargs)
            return
        if pending_size is not None and (time.time() - last_resize_time) > 0.15:
            real_screen = _original_set_mode(pending_size, pygame.RESIZABLE)
            real_width, real_height = pending_size
            pending_size = None
        if pygame.display.get_surface() == real_screen and real_screen is not None:
            pygame.transform.scale(virtual_surface, real_screen.get_size(), real_screen)
        _original_update(*args, **kwargs)

    def custom_get_pos():
        global real_screen
        x, y = _original_get_pos()
        if _minigame_active:
            return (x, y)
        if pygame.display.get_surface() == real_screen and real_screen is not None:
            w_disp, h_disp = real_screen.get_size()
            return (int(x * 1200 / w_disp), int(y * 600 / h_disp))
        return (x, y)

    def custom_event_get(*args, **kwargs):
        global real_screen, real_width, real_height, w, h
        nonlocal pending_size, last_resize_time
        events = _original_event_get(*args, **kwargs)
        if _minigame_active:
            return events
        modified_events = []
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                if pygame.display.get_surface() == real_screen and real_screen is not None:
                    pending_size = event.size
                    last_resize_time = time.time()
            
            if pygame.display.get_surface() == real_screen and real_screen is not None:
                w_disp, h_disp = real_screen.get_size()
                
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    pos_x = int(event.pos[0] * 1200 / w_disp)
                    pos_y = int(event.pos[1] * 600 / h_disp)
                    event_dict = dict(event.__dict__)
                    event_dict['pos'] = (pos_x, pos_y)
                    modified_events.append(pygame.event.Event(event.type, event_dict))
                elif event.type == pygame.MOUSEMOTION:
                    pos_x = int(event.pos[0] * 1200 / w_disp)
                    pos_y = int(event.pos[1] * 600 / h_disp)
                    rel_x = int(event.rel[0] * 1200 / w_disp)
                    rel_y = int(event.rel[1] * 600 / h_disp)
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

    screen_surface = pygame.display.set_mode((w, h))
    pygame.display.set_caption("PIXELTOWN")
    clock = pygame.time.Clock()

    # Fonts
    button_font = pygame.font.Font(None, 35)
    title_font = pygame.font.SysFont('monospace', 25, bold=True)
    normal_font = pygame.font.Font(None, 32)

    # State variables (Keeping track of everything)
    game_state = "intro"

    # Text box state and player data
    textbox_state = {"texto": username if (username and not progress_loaded) else "", "activo": False}
    tax_data = {"porcentaje": ""}
    loan_data = {"cantidad": 0, "deuda": 0}

    # Selected building type to place
    building_to_place = None

    # MAIN GAME LOOP im literally learning spanish rn while doing this :)
    while game_state != "salir": # quit
        events = pygame.event.get()

        if game_state == "intro":
            game_state = intro_scene(screen_surface, clock)
        elif game_state == "menu":
            game_state = menu_scene(screen_surface, title_font, button_font, events)
        elif game_state == "jugando": # playing
            if progress_loaded:
                game_state = "mapainicial"
            else:
                game_state = game_scene(screen_surface, button_font, events, title_font) # game scene
        elif game_state == "preguntando": # ask
            game_state = ask_name_scene(screen_surface, title_font, normal_font, events, textbox_state, player_data)
        elif game_state == "preguntando2": # ask 2
            game_state = ask_city_name_scene(screen_surface, title_font, normal_font, events, textbox_state, player_data)
        elif game_state == "cargamapa": # map loader
            game_state = map_loader_scene(screen_surface, title_font, button_font, events, normal_font)
        elif game_state == "mapainicial": # initial map
            game_state = initial_map_scene(screen_surface, title_font, button_font, events, normal_font, player_data)
        elif game_state == "acciones": # actions
            game_state = actions_scene(screen_surface, title_font, button_font, events, normal_font)
        elif game_state == "misiones":
            game_state = missions_scene(screen_surface, title_font, button_font, events, normal_font)
        elif game_state == "tienda": # store
            game_state = shop_scene(screen_surface, title_font, button_font, events, normal_font)
        elif game_state == "info":
            game_state = info_scene(screen_surface, title_font, button_font, events, normal_font)
        elif game_state == "infodos": # info2
            game_state = info_two_scene(screen_surface, title_font, button_font, events, normal_font)
        elif game_state == "minijuegos": # minigame
            game_state = minigames_scene(screen_surface, title_font, button_font, events, normal_font)
        elif game_state == "snakegame":
            game_state = snakegame(screen_surface)
        elif game_state == "tetrisgame":
            game_state = tetrisgame(screen_surface)
        elif game_state == "solarsystem":
            game_state = solarsystem(screen_surface)
        elif game_state in ("spaceshipgame", "spaceship"):
            game_state = spaceshipgame(screen_surface)
        elif game_state == "productos": # products
            game_state = products_scene(screen_surface, title_font, button_font, events, normal_font)
        elif game_state == "prestamo":
            game_state = loan_scene(screen_surface, title_font, normal_font, events, player_data, textbox_state, loan_data)
        elif game_state == "facturar":
            game_state = billing_scene(screen_surface, title_font, button_font, events, normal_font, player_data)
        elif game_state == "impuestos":
            game_state = taxes_scene(screen_surface, title_font, normal_font, events, player_data, textbox_state, tax_data)
        elif game_state == "productos2":
            game_state = products_two_scene(screen_surface, title_font, button_font, events, normal_font)
        elif game_state == "vender_edificio":
            game_state = sell_building_scene(screen_surface, title_font, button_font, events, normal_font)
        elif game_state == "adorno":
            result = decoration_scene(screen_surface, title_font, button_font, events, normal_font)
            if isinstance(result, tuple):
                game_state, building_to_place = result
            else:
                game_state = result
        elif game_state == "construccion":
            result = construction_scene(screen_surface, title_font, button_font, events, normal_font)
            if isinstance(result, tuple):
                game_state, building_to_place = result  # e.g. ("colocando_edificio", "casa")
            else:
                game_state = result
        elif game_state == "colocando_edificio":
            if not building_to_place:
                game_state = "construccion"
            else:
                game_state = placement_scene(screen_surface, events, normal_font, building_to_place)
                if game_state != "colocando_edificio":
                    building_to_place = None
        elif game_state == "gameover":
            game_state = gameover_scene(screen_surface, events)

        show_alert(screen_surface)

        mouseDown = False
        if pygame.mouse.get_pressed()[0]:
            mouseDown = True

        pygame.display.flip()
        clock.tick(60)

    if logged_in_username:
        save_progress(logged_in_username)
    pygame.quit()
    sys.exit()


# SCRIPT ENTRY POINT
if __name__ == '__main__':
    from terminal import terminal_beginning
    terminal_beginning()