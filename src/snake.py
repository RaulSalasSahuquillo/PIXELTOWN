"""
PIXELTOWN - This is the code of the minigame of the classic snake, made when I was 10, I decided to bring it to PIXELTOWN.
Copyright (C) 2026  Raúl Salas Sahuquillo

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

from localization import _
import pygame
import random

# Tamaño de la serpiente y la comida
SIZE = 20

class Snake:
    def __init__(self):
        self.body = [(100, 100), (120, 100), (140, 100)]
        self.direction = "LEFT"

    def move(self):
        head_x, head_y = self.body[0]

        if self.direction == "LEFT":
            head_x -= SIZE
        elif self.direction == "RIGHT":
            head_x += SIZE
        elif self.direction == "UP":
            head_y -= SIZE
        elif self.direction == "DOWN":
            head_y += SIZE

        self.body.insert(0, (head_x, head_y))
        self.body.pop()

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], SIZE, SIZE))


def draw_food(screen, food):
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food[0], food[1], SIZE, SIZE))


def spawn_food():
    x = random.randrange(0, 800 // SIZE) * SIZE
    y = random.randrange(0, 600 // SIZE) * SIZE
    return (x, y)


def run_snake(screen_surface):
    """Run the snake minigame inside the existing PIXELTOWN window.
    Returns the next scene name to transition to when the game ends."""

    # Save original display size so we can restore it later
    original_size = screen_surface.get_size()
    original_caption = pygame.display.get_caption()

    # Resize display for the snake game
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(_("snakegame"))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    popup_font = pygame.font.Font(None, 34)

    snake = Snake()
    food = (200, 200)
    score = 0
    popup_timer = 0
    popup_pos = (400, 300)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Restore display before exiting
                pygame.display.set_mode(original_size)
                pygame.display.set_caption(original_caption[0])
                return "salir"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                if event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"
                elif event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"

        snake.move()
        screen.fill((0, 0, 0))
        snake.draw(screen)
        draw_food(screen, food)

        # Comprobar colisión con la comida
        if snake.body[0] == food:
            popup_pos = food
            food = spawn_food()
            snake.body.append((0, 0))
            score += 1
            popup_timer = 15
            import game
            game.add_reward(5, 5)

        # Draw HUD on top of screen
        hud_text = font.render(f"Score: {score}   |   PIXELTOWN: +{score * 5}$   +{score * 5} XP", True, (255, 215, 0))
        screen.blit(hud_text, (15, 12))

        # Floating popup message when eating food
        if popup_timer > 0:
            popup_surf = popup_font.render("+5 Money  +5 XP!", True, (50, 255, 50))
            popup_rect = popup_surf.get_rect(center=(popup_pos[0] + 10, max(40, popup_pos[1] - 15)))
            screen.blit(popup_surf, popup_rect)
            popup_timer -= 1

        # Comprobar colisión con el borde de la pantalla
        if not (0 <= snake.body[0][0] < 800 and 0 <= snake.body[0][1] < 600):
            running = False

        # Comprobar colisión con la serpiente
        if snake.body[0] in snake.body[1:]:
            running = False

        pygame.display.update()
        clock.tick(10)

    # Restore the original PIXELTOWN display
    pygame.display.set_mode(original_size)
    pygame.display.set_caption(original_caption[0])
    return "minijuegos"