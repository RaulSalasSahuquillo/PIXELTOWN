"""
PIXELTOWN - Spaceship Battle Minigame.
A classic retro spaceship combat minigame integrated into PIXELTOWN.
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

import os
import sys
import random
import pygame
from localization import _

# Path Configuration
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")

# Game Constants
WIDTH, HEIGHT = 900, 500
FPS = 60

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
VEL = 5
BULLET_VEL = 8
MAX_BULLETS = 4
MAX_HEALTH = 10

BORDER_WIDTH = 8
BORDER = pygame.Rect(WIDTH // 2 - BORDER_WIDTH // 2, 0, BORDER_WIDTH, HEIGHT)

# Custom Pygame Events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED_COLOR = (255, 60, 60)
YELLOW_COLOR = (255, 230, 40)
BORDER_COLOR = (40, 120, 200)
BORDER_GLOW = (80, 180, 255)


# Particle Effects System
class Particle:
    def __init__(self, x, y, color, vel_x=None, vel_y=None, lifetime=20, size=4):
        self.x = x
        self.y = y
        self.color = color
        self.vel_x = vel_x if vel_x is not None else random.uniform(-3, 3)
        self.vel_y = vel_y if vel_y is not None else random.uniform(-3, 3)
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.lifetime -= 1
        self.size = max(1, self.size * 0.95)

    def draw(self, surface):
        if self.lifetime > 0:
            alpha = max(0, min(255, int(255 * (self.lifetime / self.max_lifetime))))
            surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color[:3], alpha), (int(self.size), int(self.size)), int(self.size))
            surface.blit(surf, (self.x - self.size, self.y - self.size))


# Asset Loader Helper
def load_game_assets():
    """Safely loads images and sounds for the spaceship game."""
    assets = {}

    # Images
    try:
        bg_raw = pygame.image.load(os.path.join(IMAGES_DIR, "space.png")).convert()
        assets["bg"] = pygame.transform.scale(bg_raw, (WIDTH, HEIGHT))
    except Exception as e:
        print(f"[Spaceship] Warning: Could not load space.png: {e}")
        assets["bg"] = None

    try:
        y_raw = pygame.image.load(os.path.join(IMAGES_DIR, "spaceship_yellow.png")).convert_alpha()
        y_scaled = pygame.transform.scale(y_raw, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
        assets["yellow_ship"] = pygame.transform.rotate(y_scaled, 90)
    except Exception as e:
        print(f"[Spaceship] Warning: Could not load spaceship_yellow.png: {e}")
        assets["yellow_ship"] = None

    try:
        r_raw = pygame.image.load(os.path.join(IMAGES_DIR, "spaceship_red.png")).convert_alpha()
        r_scaled = pygame.transform.scale(r_raw, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
        assets["red_ship"] = pygame.transform.rotate(r_scaled, 270)
    except Exception as e:
        print(f"[Spaceship] Warning: Could not load spaceship_red.png: {e}")
        assets["red_ship"] = None

    # Sounds
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        assets["fire_sound"] = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Gun+Silencer.mp3"))
        assets["fire_sound"].set_volume(0.4)
    except Exception as e:
        print(f"[Spaceship] Warning: Could not load Gun+Silencer.mp3: {e}")
        assets["fire_sound"] = None

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        assets["hit_sound"] = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Grenade+1.mp3"))
        assets["hit_sound"].set_volume(0.5)
    except Exception as e:
        print(f"[Spaceship] Warning: Could not load Grenade+1.mp3: {e}")
        assets["hit_sound"] = None

    return assets


# Ship Movement & AI Logic
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 55:  # UP (leave room for HUD)
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 55:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10:  # DOWN
        red.y += VEL


def ai_handle_movement(red, yellow, red_bullets, yellow_bullets, ai_timer, fire_sound):
    """Simple AI bot for Player 2 in single-player mode."""
    # Dodge incoming bullets
    dodge = False
    for bullet in yellow_bullets:
        if bullet.x > BORDER.x and abs(bullet.y - red.centery) < 40:
            if bullet.y < red.centery and red.y + VEL + red.height < HEIGHT - 10:
                red.y += VEL
                dodge = True
                break
            elif bullet.y >= red.centery and red.y - VEL > 55:
                red.y -= VEL
                dodge = True
                break

    # Track Yellow ship vertically if not actively dodging
    if not dodge:
        if red.centery < yellow.centery - 10 and red.y + VEL + red.height < HEIGHT - 10:
            red.y += int(VEL * 0.7)
        elif red.centery > yellow.centery + 10 and red.y - VEL > 55:
            red.y -= int(VEL * 0.7)

    # Random horizontal movement within right half
    if random.random() < 0.05:
        target_x = random.randint(BORDER.x + BORDER.width + 40, WIDTH - 80)
        if red.x < target_x:
            red.x = min(target_x, red.x + VEL)
        elif red.x > target_x:
            red.x = max(target_x, red.x - VEL)

    # Shooting logic
    if len(red_bullets) < MAX_BULLETS and ai_timer <= 0:
        # Check alignment with Yellow ship
        if abs(red.centery - yellow.centery) < 50 or random.random() < 0.2:
            bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
            red_bullets.append(bullet)
            if fire_sound:
                fire_sound.play()
            return random.randint(30, 60)  # Next shoot cooldown

    return max(0, ai_timer - 1)


# Bullets & Collisions
def handle_bullets(yellow_bullets, red_bullets, yellow, red, particles):
    for bullet in list(yellow_bullets):
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            # Create spark particles
            for _ in range(12):
                particles.append(Particle(bullet.x, bullet.y, (255, 100, 50), size=4))
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in list(red_bullets):
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            # Create spark particles
            for _ in range(12):
                particles.append(Particle(bullet.x, bullet.y, (255, 200, 50), size=4))
        elif bullet.x < 0:
            red_bullets.remove(bullet)

    # Bullet vs bullet collision
    for y_b in list(yellow_bullets):
        for r_b in list(red_bullets):
            if y_b.colliderect(r_b):
                for _ in range(8):
                    particles.append(Particle((y_b.x + r_b.x) // 2, (y_b.y + r_b.y) // 2, (200, 200, 255), size=3))
                if y_b in yellow_bullets:
                    yellow_bullets.remove(y_b)
                if r_b in red_bullets:
                    red_bullets.remove(r_b)
                break


# Drawing Helpers
def draw_health_bar(surface, x, y, health, max_health, bar_color):
    """Draws a sleek health bar with outline."""
    bar_width = 160
    bar_height = 14
    ratio = max(0.0, health / max_health)
    fill_width = int(bar_width * ratio)

    # Background
    pygame.draw.rect(surface, (40, 40, 40), (x, y, bar_width, bar_height), border_radius=3)
    # Fill
    if fill_width > 0:
        pygame.draw.rect(surface, bar_color, (x, y, fill_width, bar_height), border_radius=3)
    # Border
    pygame.draw.rect(surface, (200, 200, 200), (x, y, bar_width, bar_height), 1, border_radius=3)


def draw_window(surface, assets, yellow, red, yellow_bullets, red_bullets,
                yellow_health, red_health, particles, font, small_font,
                vs_ai_mode, exit_rect, mode_rect, mouse_pos):
    # Background
    if assets["bg"]:
        surface.blit(assets["bg"], (0, 0))
    else:
        surface.fill(BLACK)

    # Middle Border with glow
    pygame.draw.rect(surface, BORDER_GLOW, (BORDER.x - 1, BORDER.y, BORDER.width + 2, BORDER.height))
    pygame.draw.rect(surface, BORDER_COLOR, BORDER)

    # Top HUD Bar Overlay
    hud_overlay = pygame.Surface((WIDTH, 52), pygame.SRCALPHA)
    hud_overlay.fill((10, 15, 25, 210))
    surface.blit(hud_overlay, (0, 0))
    pygame.draw.line(surface, (50, 80, 130), (0, 52), (WIDTH, 52), 1)

    # Yellow Player HUD (Top-Left: x = 20..180)
    yellow_text = font.render(f"P1 (YELLOW)  HP: {yellow_health}", True, YELLOW_COLOR)
    surface.blit(yellow_text, (20, 8))
    draw_health_bar(surface, 20, 30, yellow_health, MAX_HEALTH, YELLOW_COLOR)

    # Mode Button (Top-Center: x = 375..525)
    mode_hover = mode_rect.collidepoint(mouse_pos)
    mode_bg = (50, 90, 150) if mode_hover else (30, 60, 110)
    pygame.draw.rect(surface, mode_bg, mode_rect, border_radius=5)
    pygame.draw.rect(surface, (100, 160, 240), mode_rect, 1, border_radius=5)
    mode_text = small_font.render("Mode: 1P (vs AI)" if vs_ai_mode else "Mode: 2P (PvP)", True, WHITE)
    surface.blit(mode_text, mode_text.get_rect(center=mode_rect.center))

    # Red Player HUD (Top-Right: x = 590..750)
    p2_label = "CPU (RED)" if vs_ai_mode else "P2 (RED)"
    red_text = font.render(f"{p2_label}  HP: {red_health}", True, RED_COLOR)
    surface.blit(red_text, (590, 8))
    draw_health_bar(surface, 590, 30, red_health, MAX_HEALTH, RED_COLOR)

    # In-Game EXIT Button (Top-Right: x = 790..885)
    exit_hover = exit_rect.collidepoint(mouse_pos)
    exit_bg = (230, 45, 45) if exit_hover else (170, 25, 25)
    pygame.draw.rect(surface, exit_bg, exit_rect, border_radius=5)
    pygame.draw.rect(surface, (255, 120, 120), exit_rect, 1, border_radius=5)
    exit_text = font.render("EXIT", True, WHITE)
    surface.blit(exit_text, exit_text.get_rect(center=exit_rect.center))

    # Spaceships
    if assets["yellow_ship"]:
        surface.blit(assets["yellow_ship"], (yellow.x, yellow.y))
    else:
        pygame.draw.rect(surface, YELLOW_COLOR, yellow)

    if assets["red_ship"]:
        surface.blit(assets["red_ship"], (red.x, red.y))
    else:
        pygame.draw.rect(surface, RED_COLOR, red)

    # Bullets
    for bullet in yellow_bullets:
        pygame.draw.rect(surface, (255, 255, 120), bullet, border_radius=2)
        pygame.draw.rect(surface, (255, 160, 20), (bullet.x - 2, bullet.y + 1, bullet.width + 4, bullet.height - 2), border_radius=2)

    for bullet in red_bullets:
        pygame.draw.rect(surface, (255, 120, 120), bullet, border_radius=2)
        pygame.draw.rect(surface, (255, 40, 40), (bullet.x - 2, bullet.y + 1, bullet.width + 4, bullet.height - 2), border_radius=2)

    # Particles
    for p in particles:
        p.draw(surface)

    # Controls hint at bottom
    hint_surf = small_font.render("P1: WASD + K (Disparar)  |  P2: ARROWS + RCTRL  |  ESC: Salir", True, (160, 170, 190))
    surface.blit(hint_surf, hint_surf.get_rect(center=(WIDTH // 2, HEIGHT - 12)))


def draw_winner(surface, winner_text, reward_text, font, big_font, exit_rect, mouse_pos):
    """Draws a dramatic game over / winner overlay."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    surface.blit(overlay, (0, 0))

    # Winner Title
    title_surf = big_font.render(winner_text, True, (255, 220, 50))
    surface.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))

    # Reward Banner if won
    if reward_text:
        rew_surf = font.render(reward_text, True, (50, 255, 80))
        surface.blit(rew_surf, rew_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 5)))

    # Restart / Exit hint
    restart_surf = font.render("Press SPACE / R to Play Again  -  ESC or EXIT to Return", True, WHITE)
    surface.blit(restart_surf, restart_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 55)))

    # EXIT Button in overlay
    exit_hover = exit_rect.collidepoint(mouse_pos)
    exit_bg = (230, 45, 45) if exit_hover else (170, 25, 25)
    pygame.draw.rect(surface, exit_bg, exit_rect, border_radius=5)
    pygame.draw.rect(surface, (255, 120, 120), exit_rect, 1, border_radius=5)
    exit_text = font.render("EXIT", True, WHITE)
    surface.blit(exit_text, exit_text.get_rect(center=exit_rect.center))


# Main Minigame Runner
def run_spaceship(screen_surface):
    """Run the Spaceship minigame inside the existing PIXELTOWN window.
    Returns the next scene name ('minijuegos' or 'salir')."""

    # Save original display state so we can restore it cleanly
    original_size = screen_surface.get_size()
    original_caption = pygame.display.get_caption()

    # Set up minigame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game_title = _("spaceshipgame") if _("spaceshipgame") != "[spaceshipgame missing]" else "Spaceship Battle"
    pygame.display.set_caption(f"PIXELTOWN - {game_title}")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 20)
    big_font = pygame.font.Font(None, 64)

    assets = load_game_assets()

    # Buttons
    exit_rect = pygame.Rect(WIDTH - 105, 10, 95, 32)
    mode_rect = pygame.Rect(WIDTH // 2 - 75, 10, 150, 32)

    # Game State Variables
    yellow = pygame.Rect(100, HEIGHT // 2 - SPACESHIP_HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(WIDTH - 150, HEIGHT // 2 - SPACESHIP_HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []
    yellow_health = MAX_HEALTH
    red_health = MAX_HEALTH

    particles = []
    vs_ai_mode = True
    ai_timer = 0

    winner_text = ""
    reward_text = ""
    reward_granted = False

    running = True
    return_scene = "minijuegos"

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        # Engine particle trails behind spaceships
        if random.random() < 0.5:
            particles.append(Particle(yellow.x, yellow.centery, (255, 180, 40), vel_x=-random.uniform(1, 3), vel_y=random.uniform(-1, 1), lifetime=12, size=3))
        if random.random() < 0.5:
            particles.append(Particle(red.right, red.centery, (255, 60, 60), vel_x=random.uniform(1, 3), vel_y=random.uniform(-1, 1), lifetime=12, size=3))

        # Update particles
        for p in list(particles):
            p.update()
            if p.lifetime <= 0:
                particles.remove(p)

        # Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return_scene = "salir"
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if exit_rect.collidepoint(event.pos):
                        running = False
                        return_scene = "minijuegos"
                        break
                    elif mode_rect.collidepoint(event.pos) and not winner_text:
                        vs_ai_mode = not vs_ai_mode

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return_scene = "minijuegos"
                    break

                # Restart game if in game-over state
                if winner_text and event.key in (pygame.K_SPACE, pygame.K_r):
                    yellow.x, yellow.y = 100, HEIGHT // 2 - SPACESHIP_HEIGHT // 2
                    red.x, red.y = WIDTH - 150, HEIGHT // 2 - SPACESHIP_HEIGHT // 2
                    yellow_bullets.clear()
                    red_bullets.clear()
                    particles.clear()
                    yellow_health = MAX_HEALTH
                    red_health = MAX_HEALTH
                    winner_text = ""
                    reward_text = ""
                    reward_granted = False
                    continue

                # Player 1 Shooting (K, LCTRL, or SPACE)
                if not winner_text and event.key in (pygame.K_k, pygame.K_LCTRL, pygame.K_SPACE):
                    if len(yellow_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                        yellow_bullets.append(bullet)
                        if assets["fire_sound"]:
                            assets["fire_sound"].play()

                # Player 2 Shooting (RCTRL, RSHIFT, or RETURN) - Only if 2P mode or manual input
                if not winner_text and not vs_ai_mode and event.key in (pygame.K_RCTRL, pygame.K_RSHIFT, pygame.K_RETURN):
                    if len(red_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                        red_bullets.append(bullet)
                        if assets["fire_sound"]:
                            assets["fire_sound"].play()

            # Hit events
            if event.type == RED_HIT:
                red_health -= 1
                if assets["hit_sound"]:
                    assets["hit_sound"].play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                if assets["hit_sound"]:
                    assets["hit_sound"].play()

        if not running:
            break

        # Game State Update (when not game over)
        if not winner_text:
            keys_pressed = pygame.key.get_pressed()
            yellow_handle_movement(keys_pressed, yellow)

            if vs_ai_mode:
                ai_timer = ai_handle_movement(red, yellow, red_bullets, yellow_bullets, ai_timer, assets["fire_sound"])
            else:
                red_handle_movement(keys_pressed, red)

            handle_bullets(yellow_bullets, red_bullets, yellow, red, particles)

            # Check for Winner
            if red_health <= 0:
                winner_text = "YELLOW WINS!"
                if not reward_granted:
                    try:
                        import game
                        game.add_reward(25, 25)
                        reward_text = "+25 Money  +25 XP to PIXELTOWN!"
                    except Exception as e:
                        print(f"[Spaceship] Could not grant PIXELTOWN reward: {e}")
                    reward_granted = True

            elif yellow_health <= 0:
                winner_text = "RED WINS!"
                reward_text = "Better luck next time!"


        # Rendering
        draw_window(screen, assets, yellow, red, yellow_bullets, red_bullets,
                    yellow_health, red_health, particles, font, small_font,
                    vs_ai_mode, exit_rect, mode_rect, mouse_pos)

        if winner_text:
            draw_winner(screen, winner_text, reward_text, font, big_font, exit_rect, mouse_pos)

        pygame.display.update()

    # Restore the original PIXELTOWN display state
    pygame.display.set_mode(original_size)
    pygame.display.set_caption(original_caption[0])
    return return_scene


if __name__ == '__main__':
    pygame.init()
    mock_screen = pygame.display.set_mode((1200, 600))
    run_spaceship(mock_screen)
    pygame.quit()
