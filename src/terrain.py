"""
PIXELTOWN - Authentic 16-bit Pixel Art Terrain, Meandering River, and Interactive Camera Engine
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

import math
import random
import os
import sys
import pygame

WORLD_WIDTH = 3600
WORLD_HEIGHT = 2400

# 16-BIT RETRO PIXEL ART COLOR PALETTE (Extracted from PIXELTOWN classic assets)
# Grass palette
GRASS_BASE   = (86, 158, 44)    # #569e2c
GRASS_LIGHT  = (118, 192, 58)   # #76c03a
GRASS_SHADE  = (58, 114, 28)    # #3a721c
GRASS_DARK   = (40, 82, 20)     # #285214

# Cliff & Earth undercut (2.5D elevation matching river.png)
CLIFF_EARTH  = (54, 34, 18)     # #362212
CLIFF_SHADOW = (34, 20, 10)     # #22140a

# River Water palette
WATER_DEEP   = (26, 68, 124)    # #1a447c
WATER_MID    = (42, 104, 164)   # #2a68a4
WATER_SHALLOW= (80, 158, 208)   # #509ed0
WATER_RIPPLE = (164, 220, 248)  # #a4dcf8
WATER_FOAM   = (232, 248, 255)  # #e8f8ff

# Sand & Shoreline palette
SAND_BASE    = (218, 194, 140)  # #dac28c
SAND_LIGHT   = (242, 222, 172)  # #f2deac
SAND_SHADE   = (182, 154, 102)  # #b69a66
SAND_WET     = (146, 118, 76)   # #92764c

# Stone / Boulder palette
COBBLE_SHADE = (108, 112, 118)
COBBLE_BASE  = (154, 158, 164)
COBBLE_LIGHT = (200, 206, 212)


def _find_asset_file(filename):
    """Locate an asset file across possible relative run paths."""
    candidates = [
        os.path.join("assets", "images", filename),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", filename),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images", filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


class Camera:
    """
    Smooth 2D Camera supporting mouse-drag panning, mouse-wheel zooming centered on cursor,
    keyboard navigation, view clamping, and world/screen coordinate transformations.
    """
    def __init__(self, world_w=WORLD_WIDTH, world_h=WORLD_HEIGHT, screen_w=1200, screen_h=600):
        self.world_w = world_w
        self.world_h = world_h
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.min_zoom = 0.35
        self.max_zoom = 2.2
        self.zoom = 1.0

        # Camera offset in world coordinates (top-left corner of the viewport)
        self.x = 0.0
        self.y = 0.0

        # Mouse dragging state
        self.is_dragging = False
        self.drag_start_screen = (0, 0)
        self.drag_start_cam = (0.0, 0.0)
        self.drag_threshold = 4
        self.has_dragged = False

        self.clamp()

    def reset_view(self):
        """Reset camera zoom to 1.0 and view to the starting settlement origin."""
        self.zoom = 1.0
        self.x = 0.0
        self.y = 0.0
        self.clamp()

    def screen_to_world(self, screen_pos):
        """Convert screen pixel coordinates (sx, sy) to world coordinates (wx, wy)."""
        sx, sy = screen_pos
        wx = self.x + sx / self.zoom
        wy = self.y + sy / self.zoom
        return (wx, wy)

    def world_to_screen(self, world_pos):
        """Convert world coordinates (wx, wy) to screen pixel coordinates (sx, sy)."""
        wx, wy = world_pos
        sx = (wx - self.x) * self.zoom
        sy = (wy - self.y) * self.zoom
        return (sx, sy)

    def zoom_at(self, screen_pos, factor):
        """
        Zoom by factor centered exactly on the given screen position (typically mouse cursor).
        The world point currently underneath screen_pos remains stationary after zooming.
        """
        mx, my = screen_pos
        wx, wy = self.screen_to_world((mx, my))

        new_zoom = max(self.min_zoom, min(self.max_zoom, self.zoom * factor))
        if abs(new_zoom - self.zoom) < 0.001:
            return

        self.zoom = new_zoom
        self.x = wx - mx / self.zoom
        self.y = wy - my / self.zoom
        self.clamp()

    def clamp(self):
        """Keep the camera viewport within world bounds."""
        view_w = self.screen_w / self.zoom
        view_h = self.screen_h / self.zoom

        if view_w >= self.world_w:
            self.x = (self.world_w - view_w) / 2.0
        else:
            self.x = max(0.0, min(float(self.world_w - view_w), self.x))

        if view_h >= self.world_h:
            self.y = (self.world_h - view_h) / 2.0
        else:
            self.y = max(0.0, min(float(self.world_h - view_h), self.y))

    def start_drag(self, screen_pos):
        """Begin a mouse drag tracking gesture."""
        self.is_dragging = True
        self.drag_start_screen = screen_pos
        self.drag_start_cam = (self.x, self.y)
        self.has_dragged = False

    def update_drag(self, screen_pos):
        """Update viewport position based on current mouse position during drag."""
        if not self.is_dragging:
            return
        dx = screen_pos[0] - self.drag_start_screen[0]
        dy = screen_pos[1] - self.drag_start_screen[1]
        if abs(dx) > self.drag_threshold or abs(dy) > self.drag_threshold:
            self.has_dragged = True
        if self.has_dragged:
            self.x = self.drag_start_cam[0] - dx / self.zoom
            self.y = self.drag_start_cam[1] - dy / self.zoom
            self.clamp()

    def end_drag(self):
        """Conclude drag operation; returns True if the mouse actually moved enough to count as a drag."""
        was_dragged = self.has_dragged
        self.is_dragging = False
        self.has_dragged = False
        return was_dragged

    def handle_keyboard(self, keys, dt_factor=1.0):
        """Pan camera via arrow keys or WASD."""
        pan_speed = (18.0 * dt_factor) / self.zoom
        moved = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= pan_speed
            moved = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += pan_speed
            moved = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= pan_speed
            moved = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += pan_speed
            moved = True
        if moved:
            self.clamp()


class TerrainManager:
    """
    Manages empty, pristine 16-bit pixel art terrain generation,
    natural meandering river spline, water collision detection, animated waves,
    and viewport/minimap rendering.
    """
    def __init__(self, world_w=WORLD_WIDTH, world_h=WORLD_HEIGHT):
        self.world_w = world_w
        self.world_h = world_h
        self.terrain_surface = None
        self.river_points = []
        self.collision_mask = None
        self.mask_scale = 8  # Scale factor for fast O(1) collision mask
        self._minimap_surface = None

        self.init_river_points()
        self.generate_terrain()
        self.generate_collision_mask()
        self.generate_minimap_base()

    def init_river_points(self):
        """Calculate Catmull-Rom spline waypoints for natural river flow across 3600x2400 valley."""
        keypoints = [
            (740, -50),
            (725, 200),
            (710, 450),
            (730, 750),
            (820, 1050),
            (1050, 1320),
            (1380, 1530),
            (1780, 1680),
            (2200, 1800),
            (2580, 1950),
            (2920, 2150),
            (3250, 2450)
        ]
        num_samples = 1200
        res = []
        n = len(keypoints) - 1
        for i in range(n):
            p0 = keypoints[max(0, i - 1)]
            p1 = keypoints[i]
            p2 = keypoints[i + 1]
            p3 = keypoints[min(n, i + 2)]
            steps = num_samples // n
            for s in range(steps):
                t = s / steps
                t2 = t * t
                t3 = t2 * t
                x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                           (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                           (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
                y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
                res.append((x, y))
        res.append(keypoints[-1])
        self.river_points = res

    def generate_terrain(self):
        """Generate completely empty, pristine 16-bit pixel-art terrain ready for village development."""
        surf = pygame.Surface((self.world_w, self.world_h))
        surf.fill(GRASS_BASE)

        # Seamless 16-bit Dithered Grass Texture (128x128)
        g_tile = pygame.Surface((128, 128))
        g_tile.fill(GRASS_BASE)
        rng = random.Random(2026)
        for _ in range(380):
            gx = rng.randint(0, 126)
            gy = rng.randint(0, 126)
            g_tile.set_at((gx, gy), GRASS_LIGHT)
            g_tile.set_at((gx + 1, gy), GRASS_LIGHT)
            g_tile.set_at((gx, gy + 1), GRASS_SHADE)
            g_tile.set_at((gx + 1, gy + 1), GRASS_SHADE)
        # Subtle wildflowers
        for _ in range(16):
            fx = rng.randint(4, 120)
            fy = rng.randint(4, 120)
            col = rng.choice([(255, 255, 255), (255, 225, 45), (240, 55, 55), (145, 218, 65)])
            g_tile.set_at((fx, fy), col)
            g_tile.set_at((fx + 1, fy), col)

        for ty in range(0, self.world_h, 128):
            for tx in range(0, self.world_w, 128):
                surf.blit(g_tile, (tx, ty))

        # Build River Centerline Lookup
        river_center = [740.0] * self.world_h
        pts = self.river_points
        for i in range(len(pts) - 1):
            p1 = pts[i]
            p2 = pts[i + 1]
            y_start = max(0, min(self.world_h - 1, int(round(p1[1]))))
            y_end = max(0, min(self.world_h - 1, int(round(p2[1]))))
            if y_start == y_end:
                river_center[y_start] = p1[0]
            else:
                step = 1 if y_end > y_start else -1
                for y in range(y_start, y_end + step, step):
                    t = (y - p1[1]) / (p2[1] - p1[1]) if p2[1] != p1[1] else 0.0
                    river_center[y] = p1[0] + (p2[0] - p1[0]) * t

        def river_hw(y):
            return 74.0 + 12.0 * math.sin(y * 0.007)

        # Sand Beach & Shoreline
        for y in range(0, self.world_h, 2):
            rc = river_center[y]
            hw = river_hw(y)
            sand_hw = hw + 34.0 + 6.0 * math.sin(y * 0.02)
            pygame.draw.line(surf, SAND_BASE, (int(rc - sand_hw), y), (int(rc + sand_hw), y), 2)
            wet_hw = hw + 10.0
            pygame.draw.line(surf, SAND_WET, (int(rc - wet_hw), y), (int(rc + wet_hw), y), 2)

        # Cliff Undercut on Grass Banks (2.5D depth matching river.png)
        for y in range(0, self.world_h, 2):
            rc = river_center[y]
            hw = river_hw(y)
            sand_hw = hw + 34.0 + 6.0 * math.sin(y * 0.02)
            wx = int(rc - sand_hw)
            pygame.draw.line(surf, CLIFF_EARTH, (wx - 6, y), (wx, y), 2)
            pygame.draw.line(surf, CLIFF_SHADOW, (wx - 2, y + 1), (wx, y + 1), 1)
            ex = int(rc + sand_hw)
            pygame.draw.line(surf, CLIFF_EARTH, (ex, y), (ex + 6, y), 2)
            pygame.draw.line(surf, CLIFF_SHADOW, (ex, y + 1), (ex + 2, y + 1), 1)

        # Water Channels
        for y in range(0, self.world_h, 2):
            rc = river_center[y]
            hw = river_hw(y)
            pygame.draw.line(surf, WATER_SHALLOW, (int(rc - hw), y), (int(rc + hw), y), 2)
            mid_hw = hw * 0.78
            pygame.draw.line(surf, WATER_MID, (int(rc - mid_hw), y), (int(rc + mid_hw), y), 2)
            deep_hw = hw * 0.50
            pygame.draw.line(surf, WATER_DEEP, (int(rc - deep_hw), y), (int(rc + deep_hw), y), 2)

        # Horizontal Wave Highlights (Pixel Ripples)
        rng = random.Random(777)
        for y in range(8, self.world_h - 8, 14):
            rc = river_center[y]
            hw = river_hw(y) * 0.7
            for _ in range(rng.randint(2, 4)):
                wx = int(rc + rng.uniform(-hw, hw))
                w_len = rng.randint(14, 30)
                pygame.draw.line(surf, WATER_SHALLOW, (wx, y), (wx + w_len, y), 2)
                pygame.draw.line(surf, WATER_RIPPLE, (wx + 3, y), (wx + w_len - 3, y), 1)
                pygame.draw.line(surf, WATER_FOAM, (wx + 6, y), (wx + 11, y), 1)

        # South-East Natural Pond / Lake
        lake_cx, lake_cy = 2850, 1850
        lake_rx, lake_ry = 220, 150
        for a in range(0, 360, 2):
            rad = math.radians(a)
            for d in range(lake_rx - 8, lake_rx + 42, 2):
                px = int(lake_cx + math.cos(rad) * d)
                py = int(lake_cy + math.sin(rad) * (d * lake_ry / lake_rx))
                if 0 <= px < self.world_w and 0 <= py < self.world_h:
                    surf.set_at((px, py), SAND_BASE)
        pygame.draw.ellipse(surf, WATER_SHALLOW, (lake_cx - lake_rx, lake_cy - lake_ry, lake_rx * 2, lake_ry * 2))
        pygame.draw.ellipse(surf, WATER_MID, (lake_cx - int(lake_rx * 0.8), lake_cy - int(lake_ry * 0.8), int(lake_rx * 1.6), int(lake_ry * 1.6)))
        pygame.draw.ellipse(surf, WATER_DEEP, (lake_cx - int(lake_rx * 0.55), lake_cy - int(lake_ry * 0.55), int(lake_rx * 1.1), int(lake_ry * 1.1)))

        # 4. Natural Lily Pads on River & Lake
        def draw_lily(lx, ly):
            pygame.draw.circle(surf, (36, 114, 44), (lx, ly), 5)
            pygame.draw.circle(surf, (72, 172, 60), (lx - 1, ly - 1), 3)
            surf.set_at((lx, ly), (255, 185, 215))

        for lx, ly in [(715, 180), (730, 220), (705, 470), (725, 510),
                       (1350, 1480), (1420, 1580),
                       (2800, 1820), (2880, 1870), (2860, 1910)]:
            draw_lily(lx, ly)

        # Natural Mossy Field Boulders
        def draw_boulder(rx, ry, w=16, h=12):
            pygame.draw.ellipse(surf, (20, 40, 18), (rx, ry + 2, w, h))
            pygame.draw.ellipse(surf, COBBLE_SHADE, (rx, ry, w, h))
            pygame.draw.ellipse(surf, COBBLE_BASE, (rx + 2, ry + 1, w - 4, h - 3))
            pygame.draw.ellipse(surf, COBBLE_LIGHT, (rx + 4, ry + 2, w // 2, h // 2))
            pygame.draw.line(surf, (76, 148, 44), (rx + 3, ry + 2), (rx + w - 4, ry + 2), 2)

        for rx, ry in [(180, 80), (520, 480), (840, 390), (1010, 180),
                       (1500, 320), (2200, 850), (1650, 1450), (2500, 1400)]:
            draw_boulder(rx, ry)

        # Natural Trees and Bushes framing the borders
        tree_path = _find_asset_file("tree.png")
        bush_path = _find_asset_file("bush.png")

        if tree_path and os.path.exists(tree_path):
            tree_img = pygame.image.load(tree_path)
            TREE_SPRITE = pygame.transform.scale(tree_img, (84, 100))
        else:
            TREE_SPRITE = pygame.Surface((84, 100), pygame.SRCALPHA)
            pygame.draw.circle(TREE_SPRITE, GRASS_DARK, (42, 45), 36)
            pygame.draw.circle(TREE_SPRITE, GRASS_BASE, (42, 42), 34)

        if bush_path and os.path.exists(bush_path):
            bush_img = pygame.image.load(bush_path)
            BUSH_SPRITE = pygame.transform.scale(bush_img, (38, 38))
        else:
            BUSH_SPRITE = pygame.Surface((38, 38), pygame.SRCALPHA)
            pygame.draw.circle(BUSH_SPRITE, GRASS_BASE, (19, 19), 18)

        t_shadow = pygame.Surface((76, 32), pygame.SRCALPHA)
        pygame.draw.ellipse(t_shadow, (20, 42, 16, 95), (0, 0, 76, 32))

        b_shadow = pygame.Surface((36, 18), pygame.SRCALPHA)
        pygame.draw.ellipse(b_shadow, (20, 42, 16, 85), (0, 0, 36, 18))

        def blit_tree(x, y):
            surf.blit(t_shadow, (x + 4, y + 72))
            surf.blit(TREE_SPRITE, (x, y))

        def blit_bush(x, y):
            surf.blit(b_shadow, (x + 1, y + 22))
            surf.blit(BUSH_SPRITE, (x, y))

        # Border Woodland along world borders
        for x in range(0, self.world_w, 60):
            rc_top = river_center[0]
            if abs(x - rc_top) > 140:
                blit_tree(x - 20, -20)
                if random.random() < 0.5:
                    blit_bush(x + 15, 45)
            rc_bot = river_center[self.world_h - 1]
            if abs(x - rc_bot) > 160:
                blit_tree(x - 20, self.world_h - 90)

        for y in range(0, self.world_h, 60):
            blit_tree(-20, y - 20)
            blit_tree(self.world_w - 70, y - 20)

        # Sparse perimeter groves, leaving vast, flat, 100% EMPTY building meadows!
        perimeter_groves = [
            [(60, 40), (120, 30)],
            [(60, 520), (120, 550)],
            [(860, 60), (940, 80)],
            [(1120, 110), (1200, 90)],
            [(1750, 350), (1850, 400)],
            [(2200, 450), (2300, 500)],
            [(2650, 1750), (2700, 1820)],
        ]
        for grp in perimeter_groves:
            for gx, gy in grp:
                blit_tree(gx, gy)
                if random.random() < 0.65:
                    blit_bush(gx + random.randint(25, 45), gy + random.randint(40, 65))

        self.terrain_surface = surf

    def generate_collision_mask(self):
        """Generate scaled down 1-bit collision mask for the river and lake water bodies."""
        mw = self.world_w // self.mask_scale
        mh = self.world_h // self.mask_scale
        mask_surf = pygame.Surface((mw, mh), pygame.SRCALPHA)
        mask_surf.fill((0, 0, 0, 0))

        # River water collision channel
        river_pts = self.river_points
        for i in range(len(river_pts) - 1):
            p1 = (river_pts[i][0] / self.mask_scale, river_pts[i][1] / self.mask_scale)
            p2 = (river_pts[i + 1][0] / self.mask_scale, river_pts[i + 1][1] / self.mask_scale)
            w = int(148 / self.mask_scale)
            pygame.draw.line(mask_surf, (255, 255, 255), p1, p2, max(1, w))

        # Lake water collision
        lake_cx, lake_cy = 2850 // self.mask_scale, 1850 // self.mask_scale
        lake_rx, lake_ry = 220 // self.mask_scale, 150 // self.mask_scale
        pygame.draw.ellipse(mask_surf, (255, 255, 255),
                            (lake_cx - lake_rx, lake_cy - lake_ry, lake_rx * 2, lake_ry * 2))

        self.collision_mask = pygame.mask.from_surface(mask_surf)

    def is_river_collision(self, world_rect):
        """
        Check if a given world rectangle collides with the river or lake water.
        world_rect: pygame.Rect in world coordinates.
        """
        s = self.mask_scale
        sample_points = [
            (world_rect.left // s, world_rect.top // s),
            (world_rect.right // s, world_rect.top // s),
            (world_rect.left // s, world_rect.bottom // s),
            (world_rect.right // s, world_rect.bottom // s),
            (world_rect.centerx // s, world_rect.centery // s),
            ((world_rect.left + world_rect.centerx) // (2 * s), world_rect.centery // s),
            ((world_rect.right + world_rect.centerx) // (2 * s), world_rect.centery // s),
        ]
        mw, mh = self.world_w // s, self.world_h // s
        for px, py in sample_points:
            if 0 <= px < mw and 0 <= py < mh:
                if self.collision_mask.get_at((px, py)):
                    return True
        return False

    def generate_minimap_base(self):
        """Pre-scale world terrain into a compact minimap surface."""
        mm_w = 150
        mm_h = 100
        self._minimap_surface = pygame.transform.smoothscale(self.terrain_surface, (mm_w, mm_h))

    def render(self, screen, camera, frame_count=0):
        """
        Render the visible portion of the terrain through the camera viewport onto screen.
        Includes water current ripple animations.
        """
        view_w = camera.screen_w / camera.zoom
        view_h = camera.screen_h / camera.zoom

        if view_w >= camera.world_w or view_h >= camera.world_h:
            screen.fill((34, 68, 30))
            scaled_w = int(camera.world_w * camera.zoom)
            scaled_h = int(camera.world_h * camera.zoom)
            scaled = pygame.transform.scale(self.terrain_surface, (scaled_w, scaled_h))
            sx, sy = camera.world_to_screen((0, 0))
            screen.blit(scaled, (int(sx), int(sy)))
        else:
            vx = max(0, min(camera.world_w - int(view_w), int(camera.x)))
            vy = max(0, min(camera.world_h - int(view_h), int(camera.y)))
            vw = min(camera.world_w - vx, int(view_w) + 1)
            vh = min(camera.world_h - vy, int(view_h) + 1)

            sub = self.terrain_surface.subsurface((vx, vy, vw, vh))
            if abs(camera.zoom - 1.0) < 0.01:
                screen.blit(sub, (0, 0))
            else:
                scaled = pygame.transform.scale(sub, (camera.screen_w, camera.screen_h))
                screen.blit(scaled, (0, 0))

        # Animated water surface ripples along river flow
        self._render_water_ripples(screen, camera, frame_count)

    def _render_water_ripples(self, screen, camera, frame_count):
        """Render glistening water wavelets moving downstream."""
        river_pts = self.river_points
        step = 6
        flow_offset = int((frame_count * 0.4) % step)
        for i in range(8 + flow_offset, len(river_pts) - 8, step):
            p = river_pts[i]
            sx, sy = camera.world_to_screen(p)
            if -30 <= sx <= camera.screen_w + 30 and -30 <= sy <= camera.screen_h + 30:
                angle = math.atan2(river_pts[i+1][1] - river_pts[i-1][1],
                                   river_pts[i+1][0] - river_pts[i-1][0])
                offset_wave = math.sin((i + frame_count * 0.08) * 0.3) * 16 * camera.zoom
                length = (14 + (i % 7) * 2) * camera.zoom
                wx1 = sx + math.cos(angle) * length / 2 + math.cos(angle + math.pi/2) * offset_wave
                wy1 = sy + math.sin(angle) * length / 2 + math.sin(angle + math.pi/2) * offset_wave
                wx2 = sx - math.cos(angle) * length / 2 + math.cos(angle + math.pi/2) * offset_wave
                wy2 = sy - math.sin(angle) * length / 2 + math.sin(angle + math.pi/2) * offset_wave
                alpha = int(120 + 50 * math.sin(frame_count * 0.05 + i))
                rip_color = (210, 240, 255, max(40, min(200, alpha)))
                rip_surf = pygame.Surface((camera.screen_w, camera.screen_h), pygame.SRCALPHA)
                pygame.draw.line(rip_surf, rip_color, (wx1, wy1), (wx2, wy2), max(1, int(2 * camera.zoom)))
                screen.blit(rip_surf, (0, 0))

    def draw_minimap(self, screen, camera, buildings, x=10, y=10):
        """Render compact interactive minimap radar showing valley, buildings, and camera viewport."""
        mm_w = 150
        mm_h = 100
        frame_rect = pygame.Rect(x - 3, y - 3, mm_w + 6, mm_h + 6)
        pygame.draw.rect(screen, (20, 30, 20), frame_rect, border_radius=4)
        pygame.draw.rect(screen, (160, 150, 110), frame_rect, 2, border_radius=4)

        screen.blit(self._minimap_surface, (x, y))

        sx_scale = mm_w / self.world_w
        sy_scale = mm_h / self.world_h
        for b in buildings:
            bx, by = b["pos"]
            bmx = int(x + bx * sx_scale)
            bmy = int(y + by * sy_scale)
            pygame.draw.circle(screen, (255, 230, 80), (bmx, bmy), 2)

        vx = x + int(camera.x * sx_scale)
        vy = y + int(camera.y * sy_scale)
        vw = max(4, int((camera.screen_w / camera.zoom) * sx_scale))
        vh = max(4, int((camera.screen_h / camera.zoom) * sy_scale))
        cam_rect = pygame.Rect(vx, vy, vw, vh)
        cam_rect.clamp_ip(pygame.Rect(x, y, mm_w, mm_h))
        pygame.draw.rect(screen, (255, 255, 255), cam_rect, 1)


# Singleton instances
_terrain_instance = None
_camera_instance = None

def get_terrain():
    """Retrieve singleton TerrainManager instance."""
    global _terrain_instance
    if _terrain_instance is None:
        _terrain_instance = TerrainManager()
    return _terrain_instance

def get_camera():
    """Retrieve singleton Camera instance."""
    global _camera_instance
    if _camera_instance is None:
        _camera_instance = Camera()
    return _camera_instance
