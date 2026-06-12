"""
PIXELTOWN - Solar System Simulator minigame.
Merged from solarsystem.py (planet data) and simulator.py (simulation logic).
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

import pygame, sys, math, copy, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_IMAGENES = os.path.join(BASE_DIR, "assets", "imagenes")

_images = {}  # filled at runtime

planets = [{
    "name" : "mercury",
    "radius" : 15.0,
    "mass" : 0.6,
    "velocity" : [0,0],
    "position" : [0,0]
},
{
    "name" : "venus",
    "radius" : 23.0,
    "mass" : 0.95,
    "velocity" : [0,0],
    "position" : [0,0]
},
{
    "name" : "earth",
    "radius" : 24.0,
    "mass" : 1.0,
    "velocity" : [0,0],
    "position" : [0,0]
},
{
    "name" : "mars",
    "radius" : 15.0,
    "mass" : 0.4,
    "velocity" : [0,0],
    "position" : [0,0]
},
{
    "name" : "jupiter",
    "radius" : 37.0,
    "mass" : 15.0,
    "velocity" : [0,0],
    "position" : [0,0]
},
{
    "name" : "saturn",
    "radius" : 30.0,
    "mass" : 4,
    "velocity" : [0,0],
    "position" : [0,0]
},
{
    "name" : "neptune",
    "radius" : 30.0,
    "mass" : 4.2,
    "velocity" : [0,0],
    "position" : [0,0]
},
{
    "name" : "uranus",
    "radius" : 30.0,
    "mass" : 3.8,
    "velocity" : [0,0],
    "position" : [0,0]
}]


def makeNewPlanet(which):
    for pieceOfRock in planets:
        if pieceOfRock["name"] == which:
            return copy.deepcopy(pieceOfRock)
    return False


def _load_images():
    """Load planet and UI images from the correct assets directory."""
    global _images
    _images = {
        "mercury"    : pygame.image.load(os.path.join(DIR_IMAGENES, "mercury.png")).convert_alpha(),
        "venus"      : pygame.image.load(os.path.join(DIR_IMAGENES, "venus.png")).convert_alpha(),
        "earth"      : pygame.image.load(os.path.join(DIR_IMAGENES, "earth.png")).convert_alpha(),
        "mars"       : pygame.image.load(os.path.join(DIR_IMAGENES, "mars.png")).convert_alpha(),
        "jupiter"    : pygame.image.load(os.path.join(DIR_IMAGENES, "jupiter.png")).convert_alpha(),
        "saturn"     : pygame.image.load(os.path.join(DIR_IMAGENES, "saturn.png")).convert_alpha(),
        "neptune"    : pygame.image.load(os.path.join(DIR_IMAGENES, "neptune.png")).convert_alpha(),
        "uranus"     : pygame.image.load(os.path.join(DIR_IMAGENES, "uranus.png")).convert_alpha(),
        "background" : pygame.image.load(os.path.join(DIR_IMAGENES, "background.jpg")).convert(),
        "logo"       : pygame.image.load(os.path.join(DIR_IMAGENES, "logo.png")).convert_alpha(),
        "tabs"       : pygame.image.load(os.path.join(DIR_IMAGENES, "tabs.png")).convert_alpha(),
    }


# Simulator logic 

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

UICoordinates = [
    {"name": "mercury",  "coordinates": (132, 687)},
    {"name": "venus",    "coordinates": (229, 687)},
    {"name": "earth",    "coordinates": (326, 687)},
    {"name": "mars",     "coordinates": (423, 687)},
    {"name": "jupiter",  "coordinates": (520, 687)},
    {"name": "saturn",   "coordinates": (617, 687)},
    {"name": "neptune",  "coordinates": (713, 687)},
    {"name": "uranus",   "coordinates": (810, 687)},
]

gravity = 10.0


def _drawUI(surface):
    surface.blit(_images["tabs"], (131, 687))
    surface.blit(_images["mercury"], (158, 714))
    surface.blit(_images["venus"],   (247, 706))
    surface.blit(_images["earth"],   (344, 704))
    surface.blit(_images["mars"],    (451, 714))
    surface.blit(_images["jupiter"], (524, 692))
    surface.blit(_images["saturn"],  (620, 695))
    surface.blit(_images["neptune"], (724, 697))
    surface.blit(_images["uranus"],  (822, 697))

    # EXIT button (top-right corner)
    font = pygame.font.Font(None, 30)
    boton_salir = pygame.Rect(WINDOW_WIDTH - 110, 10, 100, 36)
    pos_raton = pygame.mouse.get_pos()
    color = (220, 60, 60) if boton_salir.collidepoint(pos_raton) else (180, 40, 40)
    pygame.draw.rect(surface, color, boton_salir, border_radius=6)
    texto = font.render("EXIT", True, (255, 255, 255))
    surface.blit(texto, texto.get_rect(center=boton_salir.center))
    return boton_salir


def _drawPlanets(surface, celestialBodies):
    for planet in celestialBodies:
        planet["position"][0] += planet["velocity"][0]
        planet["position"][1] += planet["velocity"][1]
        surface.blit(_images[planet["name"]],
                     (planet["position"][0] - planet["radius"],
                      planet["position"][1] - planet["radius"]))


def _drawCurrentBody(surface, currentBody, mousePosition):
    currentBody["position"][0] = mousePosition[0]
    currentBody["position"][1] = mousePosition[1]
    surface.blit(_images[currentBody["name"]],
                 (currentBody["position"][0] - currentBody["radius"],
                  currentBody["position"][1] - currentBody["radius"]))


def _calculateMovement(surface, celestialBodies, drawAttractions):
    for planet in celestialBodies:
        for otherPlanet in celestialBodies:
            if otherPlanet is not planet:
                direction = (otherPlanet["position"][0] - planet["position"][0],
                             otherPlanet["position"][1] - planet["position"][1])
                magnitude = math.hypot(direction[0], direction[1])

                if magnitude == 0:
                    continue

                nDirection = (direction[0] / magnitude, direction[1] / magnitude)

                if magnitude < 5:
                    magnitude = 5
                elif magnitude > 30:
                    magnitude = 30

                strength = ((gravity * planet["mass"] * otherPlanet["mass"])
                            / (magnitude * magnitude)) / otherPlanet["mass"]

                appliedForce = (nDirection[0] * strength, nDirection[1] * strength)

                otherPlanet["velocity"][0] -= appliedForce[0]
                otherPlanet["velocity"][1] -= appliedForce[1]

                if drawAttractions:
                    pygame.draw.line(surface, (255, 255, 255),
                                    (planet["position"][0], planet["position"][1]),
                                    (otherPlanet["position"][0], otherPlanet["position"][1]), 1)


def _checkUIForClick(coordinates):
    for tab in UICoordinates:
        tabX = tab["coordinates"][0]
        if coordinates[0] > tabX and coordinates[0] < tabX + 82:
            return tab["name"]
    return False


def run_solarsystem(pantalla):
    """Run the Solar System Simulator inside the existing PIXELTOWN window.
    Returns the next scene name to transition to when the game ends."""

    # Save original display state
    original_size = pantalla.get_size()
    original_caption = pygame.display.get_caption()

    # Resize display for the simulator
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Solar System Simulator")
    clock = pygame.time.Clock()

    # Load images now that the display is ready
    _load_images()

    celestialBodies = []
    currentBody = None
    mouseDown = False
    previousMousePosition = [0, 0]
    drawAttractions = True
    start_ticks = pygame.time.get_ticks()

    running = True
    return_scene = "minijuegos"

    while running:
        mousePosition = pygame.mouse.get_pos()
        surface.blit(_images["background"], (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.display.set_mode(original_size)
                pygame.display.set_caption(original_caption[0])
                return "salir"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    celestialBodies = []
                if event.key == pygame.K_a:
                    drawAttractions = not drawAttractions

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
                # Check if the EXIT button was clicked
                boton_salir = pygame.Rect(WINDOW_WIDTH - 110, 10, 100, 36)
                if boton_salir.collidepoint(mousePosition):
                    running = False
                    break
                # Check if a planet tab was clicked
                if mousePosition[1] >= 687:
                    newPlanet = _checkUIForClick(mousePosition)
                    if newPlanet is not False:
                        currentBody = makeNewPlanet(newPlanet)

            if event.type == pygame.MOUSEBUTTONUP:
                mouseDown = False

        if not running:
            break

        # Draw UI 
        _drawUI(surface)
        _calculateMovement(surface, celestialBodies, drawAttractions)
        _drawPlanets(surface, celestialBodies)

        # If the user is dragging a new planet, draw it at the cursor
        if currentBody is not None:
            _drawCurrentBody(surface, currentBody, mousePosition)

            if mouseDown is False:
                currentBody["velocity"][0] = (mousePosition[0] - previousMousePosition[0]) / 4
                currentBody["velocity"][1] = (mousePosition[1] - previousMousePosition[1]) / 4
                celestialBodies.append(currentBody)
                currentBody = None

        # Show the logo for the first 4 seconds
        elapsed = pygame.time.get_ticks() - start_ticks
        if elapsed < 4000:
            surface.blit(_images["logo"], (108, 77))

        previousMousePosition = mousePosition

        pygame.display.update()
        clock.tick(60)

    # Restore the original PIXELTOWN display
    pygame.display.set_mode(original_size)
    pygame.display.set_caption(original_caption[0])
    return return_scene