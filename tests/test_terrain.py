"""
Unit tests for Camera and TerrainManager in PIXELTOWN v3.2.0.
"""

import sys
import os
import pygame

# Add src to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

pygame.init()

from terrain import Camera, TerrainManager, WORLD_WIDTH, WORLD_HEIGHT

def test_camera_coordinates():
    cam = Camera(world_w=3600, world_h=2400, screen_w=1200, screen_h=600)
    assert cam.zoom == 1.0
    assert cam.x == 0.0 and cam.y == 0.0

    # Origin test
    sx, sy = cam.world_to_screen((0, 0))
    assert (sx, sy) == (0.0, 0.0)
    wx, wy = cam.screen_to_world((0, 0))
    assert (wx, wy) == (0.0, 0.0)

    # Point at center of starting screen
    wx, wy = cam.screen_to_world((600, 300))
    assert (wx, wy) == (600.0, 300.0)

    # Zoom in by 2.0x
    cam.zoom_at((600, 300), 2.0)
    assert abs(cam.zoom - 2.0) < 0.001
    # Point under cursor must remain identical
    wx_after, wy_after = cam.screen_to_world((600, 300))
    assert abs(wx - wx_after) < 0.01
    assert abs(wy - wy_after) < 0.01

    # Reset
    cam.reset_view()
    assert cam.zoom == 1.0
    assert cam.x == 0.0 and cam.y == 0.0
    print("test_camera_coordinates passed!")

def test_camera_drag():
    cam = Camera(world_w=3600, world_h=2400, screen_w=1200, screen_h=600)
    cam.start_drag((200, 200))
    # Slight movement under threshold
    cam.update_drag((202, 201))
    assert not cam.has_dragged

    # Movement beyond threshold
    cam.update_drag((150, 150))
    assert cam.has_dragged
    # Mouse moved 50px left/up -> camera offset shifts +50px right/down
    assert cam.x == 50.0 and cam.y == 50.0

    was_dragged = cam.end_drag()
    assert was_dragged
    assert not cam.is_dragging
    print("test_camera_drag passed!")

def test_camera_clamping():
    cam = Camera(world_w=3600, world_h=2400, screen_w=1200, screen_h=600)
    # Pan way off to the negative
    cam.x = -500.0
    cam.y = -500.0
    cam.clamp()
    assert cam.x == 0.0 and cam.y == 0.0

    # Pan way off to the positive
    cam.x = 9999.0
    cam.y = 9999.0
    cam.clamp()
    assert cam.x == 3600 - 1200
    assert cam.y == 2400 - 600
    print("test_camera_clamping passed!")

def test_terrain_manager_and_collision():
    tm = TerrainManager(world_w=3600, world_h=2400)
    assert tm.terrain_surface.get_size() == (3600, 2400)
    assert len(tm.river_points) > 100

    # Old save house at (259, 197) -> should NOT collide with river
    house_rect = pygame.Rect(259, 197, 64, 64)
    assert not tm.is_river_collision(house_rect)

    # Point directly in river at (650, 100) -> should collide
    river_rect = pygame.Rect(630, 90, 64, 64)
    assert tm.is_river_collision(river_rect)

    # Point in distant meadow at (1800, 600) -> should NOT collide
    meadow_rect = pygame.Rect(1800, 600, 64, 64)
    assert not tm.is_river_collision(meadow_rect)

    print("test_terrain_manager_and_collision passed!")

def test_terrain_rendering():
    tm = TerrainManager(world_w=3600, world_h=2400)
    cam = Camera(world_w=3600, world_h=2400, screen_w=1200, screen_h=600)
    screen = pygame.Surface((1200, 600))

    # Test rendering at zoom 1.0
    tm.render(screen, cam, frame_count=1)

    # Test rendering at zoom 0.5
    cam.zoom_at((600, 300), 0.5)
    tm.render(screen, cam, frame_count=2)

    # Test rendering at zoom 1.8
    cam.zoom_at((600, 300), 3.6)
    tm.render(screen, cam, frame_count=3)

    # Test minimap
    buildings = [{"tipo": "house", "pos": (259, 197)}]
    tm.draw_minimap(screen, cam, buildings, 10, 10)

    print("test_terrain_rendering passed!")

if __name__ == "__main__":
    test_camera_coordinates()
    test_camera_drag()
    test_camera_clamping()
    test_terrain_manager_and_collision()
    test_terrain_rendering()
    print("ALL TESTS PASSED")
