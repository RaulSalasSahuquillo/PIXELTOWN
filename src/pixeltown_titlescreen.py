"""
PIXELTOWN - 20-Photogram Retro Pixel-Art Animation Title Screen
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

20-frame procedural pixel-art animation of the Pink Monster (Toy)
building Pixeltown. Used as the animated background for the menu screen.
"""

import math
import time
import pygame

# CONSTANTS & RESOLUTION
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 300

# COLOR PALETTE — Vibrant 16-Bit Super
PALETTE = {
    "sky_top": (56, 189, 248),
    "sky_bottom": (186, 230, 253),
    "sun": (250, 204, 21),
    "cloud": (255, 255, 255),
    "cloud_shadow": (203, 213, 225),
    "mountains": (99, 102, 241),
    "hills": (34, 197, 94),
    "grass": (22, 163, 74),
    "grass_dark": (21, 128, 61),
    "wood_light": (245, 158, 11),
    "wood_dark": (180, 83, 9),
    "stone_light": (148, 163, 184),
    "stone_dark": (71, 85, 105),
    "brick_red": (239, 68, 68),
    "roof_tile": (249, 115, 22),
    "monster_body": (244, 114, 182),
    "monster_shade": (219, 39, 119),
    "monster_highlight": (251, 207, 232),
    "monster_eye_white": (255, 255, 255),
    "monster_iris": (124, 58, 237),
    "monster_mouth_dark": (76, 5, 25),
    "title_primary": (250, 204, 21),
    "title_secondary": (251, 146, 60),
    "title_border": (120, 53, 15),
    "accent_gold": (251, 191, 36),
}

# 20 PHOTOGRAM SEQUENCE DEFINITIONS
PHOTOGRAM_FRAMES = [
    {"id": 1, "progress": 5, "m_x": -60, "m_y": 0, "m_scale_x": 1.0, "m_scale_y": 1.0, "m_rot": 0,
     "eyes": "blink", "mouth": "smile", "arm_l": "spread", "arm_r": "wave", "item": "none",
     "scaffold": 1, "houses": 1, "roof": False, "crane_angle": -15, "banner": False},
    {"id": 2, "progress": 10, "m_x": -40, "m_y": 12, "m_scale_x": 1.15, "m_scale_y": 0.85, "m_rot": 2,
     "eyes": "wide", "mouth": "smile", "arm_l": "down", "arm_r": "down", "item": "none",
     "scaffold": 1, "houses": 1, "roof": False, "crane_angle": -10, "banner": False},
    {"id": 3, "progress": 15, "m_x": -20, "m_y": -45, "m_scale_x": 0.9, "m_scale_y": 1.15, "m_rot": -5,
     "eyes": "sparkle", "mouth": "open-cheer", "arm_l": "raised", "arm_r": "raised", "item": "none",
     "scaffold": 1, "houses": 1, "roof": False, "crane_angle": -5, "banner": False},
    {"id": 4, "progress": 20, "m_x": 0, "m_y": -75, "m_scale_x": 1.05, "m_scale_y": 0.95, "m_rot": 0,
     "eyes": "wide", "mouth": "laugh", "arm_l": "spread", "arm_r": "spread", "item": "none",
     "scaffold": 1, "houses": 1, "roof": False, "crane_angle": 0, "banner": False},
    {"id": 5, "progress": 25, "m_x": 15, "m_y": -30, "m_scale_x": 1.1, "m_scale_y": 0.9, "m_rot": 3,
     "eyes": "normal", "mouth": "smile", "arm_l": "down", "arm_r": "wave", "item": "none",
     "scaffold": 1, "houses": 1, "roof": False, "crane_angle": 5, "banner": False},
    {"id": 6, "progress": 30, "m_x": 25, "m_y": -20, "m_scale_x": 1.0, "m_scale_y": 1.0, "m_rot": 0,
     "eyes": "look-up", "mouth": "smile", "arm_l": "down", "arm_r": "holding-hammer", "item": "hammer",
     "scaffold": 2, "houses": 1, "roof": True, "crane_angle": 10, "banner": False},
    {"id": 7, "progress": 35, "m_x": 30, "m_y": -22, "m_scale_x": 0.95, "m_scale_y": 1.05, "m_rot": -4,
     "eyes": "wide", "mouth": "wide-grin", "arm_l": "raised", "arm_r": "holding-hammer", "item": "hammer",
     "scaffold": 2, "houses": 1, "roof": True, "crane_angle": 15, "banner": False},
    {"id": 8, "progress": 40, "m_x": 32, "m_y": -24, "m_scale_x": 1.05, "m_scale_y": 0.95, "m_rot": 2,
     "eyes": "sparkle", "mouth": "laugh", "arm_l": "spread", "arm_r": "holding-hammer", "item": "hammer",
     "scaffold": 2, "houses": 2, "roof": True, "crane_angle": 20, "banner": False},
    {"id": 9, "progress": 45, "m_x": -10, "m_y": 5, "m_scale_x": 0.98, "m_scale_y": 1.02, "m_rot": -2,
     "eyes": "look-up", "mouth": "smile", "arm_l": "spread", "arm_r": "spread", "item": "block",
     "scaffold": 2, "houses": 2, "roof": True, "crane_angle": 15, "banner": False},
    {"id": 10, "progress": 50, "m_x": -5, "m_y": -8, "m_scale_x": 1.02, "m_scale_y": 0.98, "m_rot": 4,
     "eyes": "wink", "mouth": "wide-grin", "arm_l": "wave", "arm_r": "wave", "item": "none",
     "scaffold": 2, "houses": 2, "roof": True, "crane_angle": 10, "banner": False},
    {"id": 11, "progress": 55, "m_x": 40, "m_y": -60, "m_scale_x": 0.95, "m_scale_y": 1.05, "m_rot": 6,
     "eyes": "wide", "mouth": "open-cheer", "arm_l": "raised", "arm_r": "raised", "item": "none",
     "scaffold": 3, "houses": 2, "roof": True, "crane_angle": 5, "banner": False},
    {"id": 12, "progress": 60, "m_x": 10, "m_y": -70, "m_scale_x": 1.05, "m_scale_y": 0.95, "m_rot": -15,
     "eyes": "sparkle", "mouth": "laugh", "arm_l": "holding-rope", "arm_r": "holding-rope", "item": "none",
     "scaffold": 3, "houses": 2, "roof": True, "crane_angle": -15, "banner": False},
    {"id": 13, "progress": 65, "m_x": -25, "m_y": -80, "m_scale_x": 0.9, "m_scale_y": 1.1, "m_rot": 10,
     "eyes": "wide", "mouth": "open-cheer", "arm_l": "spread", "arm_r": "spread", "item": "none",
     "scaffold": 3, "houses": 2, "roof": True, "crane_angle": 0, "banner": False},
    {"id": 14, "progress": 70, "m_x": -15, "m_y": -40, "m_scale_x": 0.95, "m_scale_y": 1.05, "m_rot": -4,
     "eyes": "normal", "mouth": "smile", "arm_l": "down", "arm_r": "holding-balloon", "item": "balloon",
     "scaffold": 3, "houses": 3, "roof": True, "crane_angle": 5, "banner": True},
    {"id": 15, "progress": 75, "m_x": 0, "m_y": 0, "m_scale_x": 1.1, "m_scale_y": 0.9, "m_rot": 0,
     "eyes": "blink", "mouth": "smile", "arm_l": "wave", "arm_r": "wave", "item": "none",
     "scaffold": 3, "houses": 3, "roof": True, "crane_angle": 10, "banner": True},
    {"id": 16, "progress": 80, "m_x": 0, "m_y": -5, "m_scale_x": 1.0, "m_scale_y": 1.0, "m_rot": 0,
     "eyes": "wide", "mouth": "smile", "arm_l": "down", "arm_r": "raised", "item": "lantern",
     "scaffold": 3, "houses": 3, "roof": True, "crane_angle": 15, "banner": True},
    {"id": 17, "progress": 85, "m_x": 0, "m_y": -10, "m_scale_x": 0.98, "m_scale_y": 1.02, "m_rot": 0,
     "eyes": "sparkle", "mouth": "open-cheer", "arm_l": "raised", "arm_r": "raised", "item": "star",
     "scaffold": 3, "houses": 3, "roof": True, "crane_angle": 20, "banner": True},
    {"id": 18, "progress": 90, "m_x": 0, "m_y": -5, "m_scale_x": 1.02, "m_scale_y": 0.98, "m_rot": 2,
     "eyes": "normal", "mouth": "laugh", "arm_l": "spread", "arm_r": "wave", "item": "none",
     "scaffold": 3, "houses": 3, "roof": True, "crane_angle": 15, "banner": True},
    {"id": 19, "progress": 95, "m_x": 0, "m_y": -12, "m_scale_x": 1.05, "m_scale_y": 0.95, "m_rot": -2,
     "eyes": "sparkle", "mouth": "wide-grin", "arm_l": "wave", "arm_r": "wave", "item": "none",
     "scaffold": 3, "houses": 3, "roof": True, "crane_angle": 10, "banner": True},
    {"id": 20, "progress": 100, "m_x": 0, "m_y": -6, "m_scale_x": 1.0, "m_scale_y": 1.0, "m_rot": 0,
     "eyes": "sparkle", "mouth": "wide-grin", "arm_l": "down", "arm_r": "wave", "item": "none",
     "scaffold": 3, "houses": 3, "roof": True, "crane_angle": 0, "banner": True},
]


# PIXEL-ART RENDERING ENGINE
class PixeltownRenderer:
    def __init__(self):
        pygame.font.init()
        self.font_title = pygame.font.SysFont("Courier", 22, bold=True)
        self.font_subtitle = pygame.font.SysFont("Courier", 12, bold=True)

    def render_frame(self, surface, frame_data, palette, time_sec):
        p = palette
        surface.fill(p["sky_top"])

        # Sky Gradient (Pixel Bands)
        sky_bands = 8
        band_h = 160 // sky_bands
        for i in range(sky_bands):
            t = i / (sky_bands - 1)
            r = int(p["sky_top"][0] + t * (p["sky_bottom"][0] - p["sky_top"][0]))
            g = int(p["sky_top"][1] + t * (p["sky_bottom"][1] - p["sky_top"][1]))
            b = int(p["sky_top"][2] + t * (p["sky_bottom"][2] - p["sky_top"][2]))
            pygame.draw.rect(surface, (r, g, b), (0, i * band_h, CANVAS_WIDTH, band_h + 1))

        # Sun & Glow
        sun_x, sun_y = 65, 55
        self._draw_pixel_circle(surface, sun_x, sun_y, 22, (p["sun"][0], p["sun"][1], p["sun"][2], 80))
        self._draw_pixel_circle(surface, sun_x, sun_y, 16, p["sun"])

        # Parallax Floating Clouds
        cloud_shift = (time_sec * 8) % (CANVAS_WIDTH + 100)
        self._draw_cloud(surface, (40 + cloud_shift * 0.8) % (CANVAS_WIDTH + 80) - 40, 30, 36, p)
        self._draw_cloud(surface, (200 + cloud_shift * 0.5) % (CANVAS_WIDTH + 80) - 40, 50, 48, p)
        self._draw_cloud(surface, (330 + cloud_shift * 1.1) % (CANVAS_WIDTH + 80) - 40, 22, 28, p)

        # Distant Mountains
        self._draw_mountains(surface, p["mountains"])

        # Midground Rolling Hills & Pines
        self._draw_hills(surface, p["hills"], p["grass_dark"])

        # Village Scene
        self._draw_village(surface, frame_data, p, time_sec)

        # Ground & Cobblestones
        self._draw_ground(surface, p)

        # Scene Props (Barrels, Crane Rope, Balloon)
        self._draw_props(surface, frame_data, p)

        # The Pink Monster Character (Toy)
        self._draw_monster(surface, frame_data, p, time_sec)

        # Glowing "PIXELTOWN" 3D Title
        self._draw_title_banner(surface, frame_data, p, time_sec)

        # Celebratory Effects (Sparkles, Dust, Fireworks)
        self._draw_effects(surface, frame_data, p, time_sec)

    def _draw_pixel_circle(self, surf, cx, cy, r, color):
        r_sq = r * r
        for y in range(-r, r + 1, 2):
            for x in range(-r, r + 1, 2):
                if x * x + y * y <= r_sq:
                    surf.set_at((int(cx + x), int(cy + y)), color[:3])

    def _draw_cloud(self, surf, x, y, width, p):
        ix, iy = int(x), int(y)
        pygame.draw.rect(surf, p["cloud_shadow"], (ix, iy + 6, width, 8))
        pygame.draw.rect(surf, p["cloud"], (ix + 4, iy + 2, width - 8, 10))
        pygame.draw.rect(surf, p["cloud"], (ix + 8, iy - 4, int(width * 0.4), 12))
        pygame.draw.rect(surf, p["cloud"], (ix + int(width * 0.35), iy - 8, int(width * 0.45), 16))

    def _draw_mountains(self, surf, color):
        peaks = [(-20, 120, 45, 100), (70, 115, 55, 120), (180, 118, 50, 110), (280, 112, 60, 130)]
        for px, py, ph, pw in peaks:
            pts = [(px, py + ph), (px + pw // 2, py), (px + pw, py + ph)]
            pygame.draw.polygon(surf, color, pts)
            snow_pts = [
                (px + int(pw * 0.35), py + int(ph * 0.35)),
                (px + pw // 2, py),
                (px + int(pw * 0.65), py + int(ph * 0.35)),
            ]
            pygame.draw.polygon(surf, (255, 255, 255), snow_pts)

    def _draw_hills(self, surf, hill_col, tree_col):
        pygame.draw.rect(surf, hill_col, (0, 150, CANVAS_WIDTH, 40))
        for tx in [15, 45, 60, 110, 130, 270, 290, 350, 375]:
            pygame.draw.rect(surf, (120, 53, 15), (tx + 2, 142, 2, 8))
            pygame.draw.polygon(surf, tree_col, [(tx - 3, 144), (tx + 3, 134), (tx + 9, 144)])

    def _draw_ground(self, surf, p):
        pygame.draw.rect(surf, p["grass"], (0, 185, CANVAS_WIDTH, 115))
        pts = [(0, 240), (160, 220), (240, 220), (400, 250), (400, 300), (0, 300)]
        pygame.draw.polygon(surf, p["stone_light"], pts)
        for py in range(225, 295, 12):
            shift = 8 if (py % 24 == 0) else 0
            for px in range(20 + shift, CANVAS_WIDTH - 20, 16):
                pygame.draw.rect(surf, p["stone_dark"], (px, py, 14, 8))
                pygame.draw.rect(surf, p["stone_light"], (px + 1, py + 1, 12, 6))

    def _draw_village(self, surf, frame, p, time_sec):
        self._draw_windmill(surf, 35, 120, p, time_sec)
        self._draw_house(surf, 80, 135, 75, 70, p["roof_tile"], frame["roof"], frame["scaffold"], p, is_complete=frame["progress"] >= 40)
        self._draw_house(surf, 245, 120, 85, 85, p["brick_red"], frame["progress"] >= 30, frame["scaffold"], p, is_tower=True, is_complete=frame["progress"] >= 65)
        self._draw_crane(surf, 200, 70, frame["crane_angle"], p)

    def _draw_windmill(self, surf, x, y, p, time_sec):
        pygame.draw.rect(surf, p["stone_light"], (x + 6, y + 20, 24, 45))
        pygame.draw.rect(surf, p["roof_tile"], (x + 2, y + 8, 32, 14))
        cx, cy = x + 18, y + 18
        angle = time_sec * 2.5
        for i in range(4):
            cur_a = angle + i * (math.pi / 2)
            dx = math.cos(cur_a) * 26
            dy = math.sin(cur_a) * 26
            pygame.draw.line(surf, p["wood_light"], (cx, cy), (int(cx + dx), int(cy + dy)), 3)
            sx = cx + dx * 0.5
            sy = cy + dy * 0.5
            pygame.draw.rect(surf, (255, 255, 255), (int(sx), int(sy), 8, 8))
        pygame.draw.rect(surf, p["wood_dark"], (cx - 3, cy - 3, 6, 6))

    def _draw_house(self, surf, x, y, w, h, roof_col, has_roof, scaffold_lvl, p, is_tower=False, is_complete=False):
        pygame.draw.rect(surf, p["stone_dark"], (x, y + h - 14, w, 14))
        pygame.draw.rect(surf, p["wood_dark"], (x + 4, y + (15 if is_tower else 25), w - 8, h - (29 if is_tower else 39)))
        pygame.draw.rect(surf, p["wood_light"], (x + 6, y + (17 if is_tower else 27), w - 12, h - (33 if is_tower else 43)))
        pygame.draw.rect(surf, (30, 41, 59), (x + 12, y + h - 22, 12, 14))
        win_col = (254, 240, 138) if is_complete else (56, 189, 248)
        pygame.draw.rect(surf, win_col, (x + w - 24, y + h - 32, 12, 12))
        if has_roof:
            roof_pts = [(x - 4, y + (18 if is_tower else 26)), (x + w // 2, y), (x + w + 4, y + (18 if is_tower else 26))]
            pygame.draw.polygon(surf, roof_col, roof_pts)
            pygame.draw.rect(surf, p["brick_red"], (x + w - 16, y - 6, 8, 14))
        else:
            pygame.draw.line(surf, p["wood_dark"], (x + 2, y + 28), (x + w // 2, y + 6), 3)
            pygame.draw.line(surf, p["wood_dark"], (x + w // 2, y + 6), (x + w - 2, y + 28), 3)

    def _draw_crane(self, surf, x, y, angle_deg, p):
        pygame.draw.rect(surf, (245, 158, 11), (x - 4, y + 10, 8, 80))
        boom_pts = [(x - 50, y + 10), (x + 60, y + 10)]
        pygame.draw.line(surf, (217, 119, 6), boom_pts[0], boom_pts[1], 4)
        rad = math.radians(angle_deg)
        hook_x = x + 30 + math.sin(rad) * 20
        hook_y = y + 55 + math.cos(rad) * 10
        pygame.draw.line(surf, (71, 85, 105), (x + 30, y + 10), (int(hook_x), int(hook_y)), 2)
        pygame.draw.rect(surf, (245, 158, 11), (int(hook_x - 3), int(hook_y), 6, 6))

    def _draw_props(self, surf, frame, p):
        m = frame
        if frame["id"] in [9, 10]:
            bx = 160 + m["m_x"]
            by = 245 + m["m_y"]
            pygame.draw.rect(surf, (180, 83, 9), (bx - 14, by - 16, 28, 22))
            pygame.draw.rect(surf, (245, 158, 11), (bx - 12, by - 14, 24, 18))
            pygame.draw.rect(surf, (71, 85, 105), (bx - 14, by - 12, 28, 3))
            pygame.draw.rect(surf, (71, 85, 105), (bx - 14, by - 3, 28, 3))
        if frame.get("m_rot") == -15:
            pygame.draw.line(surf, (217, 119, 6), (200, 70), (200 + m["m_x"], 205 + m["m_y"]), 3)
        if m["item"] == "balloon":
            bx = 200 + m["m_x"] + 24
            by = 200 + m["m_y"] - 50
            pygame.draw.line(surf, (203, 213, 225), (bx, by + 18), (200 + m["m_x"] + 14, 200 + m["m_y"] - 10), 2)
            self._draw_pixel_circle(surf, bx, by, 16, (236, 72, 153))
            pygame.draw.rect(surf, (255, 255, 255), (bx - 6, by - 8, 4, 4))

    def _draw_monster(self, surf, frame, p, time_sec):
        m = frame
        cx = 200 + m["m_x"]
        cy = 210 + m["m_y"]
        idle_squish = math.sin(time_sec * 4) * 1.5
        bw = int(55 * m["m_scale_x"])
        bh = int((50 + idle_squish) * m["m_scale_y"])

        # Paws / Feet
        pygame.draw.rect(surf, (15, 23, 42), (cx - 38, cy + 44, 26, 18))
        pygame.draw.rect(surf, p["monster_shade"], (cx - 36, cy + 46, 22, 14))
        pygame.draw.rect(surf, p["monster_body"], (cx - 34, cy + 46, 18, 10))
        pygame.draw.rect(surf, (15, 23, 42), (cx + 12, cy + 44, 26, 18))
        pygame.draw.rect(surf, p["monster_shade"], (cx + 14, cy + 46, 22, 14))
        pygame.draw.rect(surf, p["monster_body"], (cx + 16, cy + 46, 18, 10))

        # Main Fuzzy Body
        pygame.draw.rect(surf, (15, 23, 42), (cx - bw - 3, cy - bh - 10, bw * 2 + 6, bh * 2 + 14))
        pygame.draw.rect(surf, p["monster_shade"], (cx - bw, cy - bh - 8, bw * 2, bh * 2 + 10))
        pygame.draw.rect(surf, p["monster_body"], (cx - bw + 4, cy - bh - 4, bw * 2 - 8, bh * 2 + 4))

        # Belly Highlights
        pygame.draw.rect(surf, p["monster_highlight"], (cx - 32, cy + 10, 64, 30))
        pygame.draw.rect(surf, p["monster_highlight"], (cx - 24, cy, 48, 14))

        # Horns
        horn_l = [(cx - 46, cy - 42), (cx - 34, cy - 72), (cx - 20, cy - 50)]
        pygame.draw.polygon(surf, (15, 23, 42), horn_l)
        pygame.draw.polygon(surf, p["monster_shade"], [(cx - 43, cy - 44), (cx - 34, cy - 68), (cx - 23, cy - 50)])
        horn_r = [(cx + 20, cy - 50), (cx + 34, cy - 72), (cx + 46, cy - 42)]
        pygame.draw.polygon(surf, (15, 23, 42), horn_r)
        pygame.draw.polygon(surf, p["monster_shade"], [(cx + 23, cy - 50), (cx + 34, cy - 68), (cx + 43, cy - 44)])

        # Eyes
        eye_y = cy - 22
        for ex in [cx - 18, cx + 18]:
            self._draw_pixel_circle(surf, ex, eye_y, 16, (15, 23, 42))
            self._draw_pixel_circle(surf, ex, eye_y, 14, p["monster_eye_white"])
            if m["eyes"] == "blink":
                pygame.draw.arc(surf, (15, 23, 42), (ex - 10, eye_y - 8, 20, 16), 0, math.pi, 3)
            else:
                self._draw_pixel_circle(surf, ex, eye_y, 8, p["monster_iris"])
                self._draw_pixel_circle(surf, ex, eye_y, 4, (15, 23, 42))
                pygame.draw.rect(surf, (255, 255, 255), (ex - 4, eye_y - 4, 4, 4))
                pygame.draw.rect(surf, (255, 255, 255), (ex + 1, eye_y + 1, 2, 2))

        # Mouth with Teeth
        mouth_y = cy + 4
        mw = 36
        pygame.draw.rect(surf, (15, 23, 42), (cx - mw - 2, mouth_y - 4, mw * 2 + 4, 24))
        pygame.draw.rect(surf, p["monster_mouth_dark"], (cx - mw, mouth_y - 2, mw * 2, 20))
        for tx in [-26, -18, -10, -2, 6, 14, 22]:
            pygame.draw.rect(surf, (255, 255, 255), (cx + tx, mouth_y - 3, 6, 6))
        for tx in [-22, -14, -6, 2, 10, 18]:
            pygame.draw.rect(surf, (255, 255, 255), (cx + tx, mouth_y + 9, 6, 6))

        # Arms
        if m["arm_r"] == "wave":
            pygame.draw.rect(surf, (15, 23, 42), (cx + 44, cy + 2, 24, 28))
            pygame.draw.rect(surf, p["monster_body"], (cx + 48, cy + 6, 16, 20))
            for fx, fy in [(62, -4), (68, 6), (68, 16), (62, 24)]:
                pygame.draw.rect(surf, p["monster_body"], (cx + fx, cy + fy, 8, 8))
        elif m["arm_r"] == "holding-hammer" or m["item"] == "hammer":
            pygame.draw.rect(surf, (15, 23, 42), (cx + 44, cy, 20, 20))
            pygame.draw.rect(surf, p["monster_body"], (cx + 46, cy + 2, 16, 16))
            pygame.draw.rect(surf, (180, 83, 9), (cx + 58, cy - 18, 6, 32))
            pygame.draw.rect(surf, (245, 158, 11), (cx + 48, cy - 28, 26, 14))
        else:
            pygame.draw.rect(surf, (15, 23, 42), (cx + 42, cy + 8, 16, 30))
            pygame.draw.rect(surf, p["monster_body"], (cx + 46, cy + 12, 8, 22))
        if m["arm_l"] == "spread":
            pygame.draw.rect(surf, (15, 23, 42), (cx - 68, cy + 5, 24, 16))
            pygame.draw.rect(surf, p["monster_body"], (cx - 66, cy + 7, 20, 12))
        else:
            pygame.draw.rect(surf, (15, 23, 42), (cx - 56, cy + 5, 16, 28))
            pygame.draw.rect(surf, p["monster_body"], (cx - 52, cy + 9, 8, 20))

    def _draw_title_banner(self, surf, frame, p, time_sec):
        title_x = 200
        title_y = 36
        text = "PIXELTOWN"
        for d in range(4, 0, -1):
            rendered_shadow = self.font_title.render(text, False, p["title_border"])
            surf.blit(rendered_shadow, (title_x - rendered_shadow.get_width() // 2 + d, title_y - rendered_shadow.get_height() // 2 + d))
        rendered_sec = self.font_title.render(text, False, p["title_secondary"])
        surf.blit(rendered_sec, (title_x - rendered_sec.get_width() // 2 + 1, title_y - rendered_sec.get_height() // 2 + 1))
        rendered_main = self.font_title.render(text, False, p["title_primary"])
        surf.blit(rendered_main, (title_x - rendered_main.get_width() // 2, title_y - rendered_main.get_height() // 2))
        if int(time_sec * 2.5) % 2 == 0:
            sub = self.font_subtitle.render("PRESS START TO PLAY", False, (255, 255, 255))
            surf.blit(sub, (title_x - sub.get_width() // 2, title_y + 22))

    def _draw_effects(self, surf, frame, p, time_sec):
        if frame["progress"] >= 35:
            for i, (sx, sy) in enumerate([(180, 110), (220, 90), (140, 140), (260, 100)]):
                pulse = 1 + math.sin(time_sec * 8 + i) * 0.4
                if pulse > 0.8:
                    pygame.draw.rect(surf, p["accent_gold"], (sx - 1, sy - 1, 3, 3))
                    pygame.draw.rect(surf, (255, 255, 255), (sx, sy, 1, 1))
        if frame["id"] == 20:
            for fx, fy, f_col in [(100, 50, (244, 63, 94)), (300, 45, (56, 189, 248)), (200, 30, (250, 204, 21))]:
                for spk in range(8):
                    ang = spk * (math.pi / 4)
                    rad = 12 + math.sin(time_sec * 6) * 6
                    px = fx + math.cos(ang) * rad
                    py = fy + math.sin(ang) * rad
                    pygame.draw.rect(surf, f_col, (int(px), int(py), 3, 3))


# SINGLETON STATE — initialized once, persists across menu_scene calls
_ts_renderer = None
_ts_canvas = None
_ts_crt_overlay = None
_ts_frame_idx = 0
_ts_last_tick = 0
_ts_start_time = 0


def render_title_background(screen, screen_w, screen_h):
    """Render one frame of the animated title screen onto the given surface.
    Called every tick from menu_scene in game.py.
    """
    global _ts_renderer, _ts_canvas, _ts_crt_overlay
    global _ts_frame_idx, _ts_last_tick, _ts_start_time

    # Lazy-init on first call
    if _ts_renderer is None:
        _ts_renderer = PixeltownRenderer()
        _ts_canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        _ts_crt_overlay = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.SRCALPHA)
        for y in range(0, CANVAS_HEIGHT, 2):
            pygame.draw.line(_ts_crt_overlay, (0, 0, 0, 45), (0, y), (CANVAS_WIDTH, y))
        _ts_start_time = time.time()
        _ts_last_tick = _ts_start_time

    now = time.time()
    time_sec = now - _ts_start_time

    # Advance frame at 6 FPS
    if now - _ts_last_tick >= 1.0 / 6:
        _ts_last_tick = now
        _ts_frame_idx = (_ts_frame_idx + 1) % len(PHOTOGRAM_FRAMES)

    # Render to internal canvas
    cur_frame = PHOTOGRAM_FRAMES[_ts_frame_idx]
    _ts_renderer.render_frame(_ts_canvas, cur_frame, PALETTE, time_sec)
    _ts_canvas.blit(_ts_crt_overlay, (0, 0))

    # Scale to screen size
    scaled = pygame.transform.scale(_ts_canvas, (screen_w, screen_h))
    screen.blit(scaled, (0, 0))
