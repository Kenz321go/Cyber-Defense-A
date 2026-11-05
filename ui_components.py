"""Shared drawing primitives and text helpers."""

import math
import pygame

import game_engine as engine
from game_engine import is_last_exercise_of_level, sorted_ids
from missions import game_data
from settings import BG, CYAN, DIM, GREEN, H, PANEL, W, WHITE

# ======================================================================
# DRAWING HELPERS
# ======================================================================
def init_fonts():
    """Monospace fonts so typed code lines up nicely."""
    names = "couriernew,courier,dejavusansmono,consolas,monospace"
    engine.fonts["s"] = pygame.font.SysFont(names, 11, bold=True)
    engine.fonts["m"] = pygame.font.SysFont(names, 13, bold=True)
    engine.fonts["l"] = pygame.font.SysFont(names, 20, bold=True)


def draw_text(surf, text, x, y, color, size="m"):
    surf.blit(engine.fonts[size].render(text, False, color), (x, y))


def draw_glow_text(surf, text, x, y, color, size="m"):
    image = engine.fonts[size].render(text, False, color)
    glow = (0, 100, 100)
    glow_image = engine.fonts[size].render(text, False, glow)
    for offset_x, offset_y in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        surf.blit(
            glow_image,
            (x + offset_x, y + offset_y),
            special_flags=pygame.BLEND_RGB_ADD,
        )
    surf.blit(image, (x, y))


def draw_text_center(surf, text, y, color, size="m"):
    img = engine.fonts[size].render(text, False, color)
    surf.blit(img, ((W - img.get_width()) // 2, y))


def wrap_text(text, size, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, line = [], ""
    for word in text.split():
        trial = word if line == "" else line + " " + word
        if engine.fonts[size].size(trial)[0] <= max_w:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_background(surf):
    surf.fill(BG)
    grid_color = (10, 23, 42)
    map_fill = (5, 17, 34)
    map_line = (10, 37, 63)
    for x in range(0, W, 30):
        pygame.draw.line(surf, grid_color, (x, 0), (x, H))
    for y in range(0, H, 30):
        pygame.draw.line(surf, grid_color, (0, y), (W, y))

    continents = (
        [(29, 66), (41, 47), (64, 42), (79, 51), (75, 66), (87, 77),
         (76, 91), (71, 108), (57, 118), (48, 101), (37, 91)],
        [(75, 122), (91, 128), (101, 151), (97, 171), (105, 187),
         (96, 207), (88, 194), (84, 170), (77, 151)],
        [(157, 62), (177, 52), (194, 59), (207, 53), (225, 63),
         (239, 58), (254, 71), (276, 69), (294, 80), (317, 75),
         (339, 86), (365, 83), (385, 97), (377, 111), (354, 109),
         (345, 122), (326, 115), (311, 128), (296, 120), (283, 135),
         (264, 128), (248, 140), (229, 129), (214, 137), (198, 120),
         (182, 123), (169, 105), (154, 98), (149, 80)],
        [(194, 137), (210, 142), (220, 159), (215, 179), (205, 195),
         (198, 180), (190, 160)],
        [(331, 146), (349, 139), (363, 149), (376, 146), (391, 161),
         (385, 179), (368, 183), (359, 198), (342, 192), (335, 176)],
        [(378, 205), (388, 201), (394, 214), (385, 221)],
    )
    for points in continents:
        pygame.draw.polygon(surf, map_fill, points)
        pygame.draw.polygon(surf, map_line, points, 1)

    ticks = pygame.time.get_ticks()
    sweep_y = (ticks // 70) % H
    pygame.draw.line(surf, (8, 30, 50), (0, sweep_y), (W, sweep_y))

    nodes = ((55, 74), (89, 151), (181, 91), (222, 104), (293, 101), (358, 162))
    for index, (x, y) in enumerate(nodes):
        target_x, target_y = nodes[(index + 2) % len(nodes)]
        pygame.draw.line(surf, (8, 37, 61), (x, y), (target_x, target_y), 1)
        pulse = (math.sin(ticks / 450 + index) + 1) / 2
        node_color = (0, 60 + round(pulse * 45), 95 + round(pulse * 70))
        pygame.draw.circle(surf, node_color, (x, y), 2)
        pygame.draw.circle(surf, (3, 12, 28), (x, y), 1)

    # Sparse drifting pixels add motion without distracting from mission text.
    for index in range(18):
        x = (index * 67 + 19) % W
        y = (ticks // 55 + index * 31) % H
        shade = 75 + round((math.sin(ticks / 500 + index) + 1) * 35)
        pygame.draw.rect(surf, (0, shade, min(150, shade + 35)), (x, y, 1, 1))


def draw_panel(surf, rect, title, accent=CYAN, fill=PANEL):
    panel_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(panel_surface, (*fill, 232), panel_surface.get_rect())
    surf.blit(panel_surface, rect.topleft)
    cut = 8
    corners = [
        (rect.left + cut, rect.top),
        (rect.right - cut, rect.top),
        (rect.right, rect.top + cut),
        (rect.right, rect.bottom - cut),
        (rect.right - cut, rect.bottom),
        (rect.left + cut, rect.bottom),
        (rect.left, rect.bottom - cut),
        (rect.left, rect.top + cut),
    ]
    pygame.draw.lines(surf, (20, 92, 130), True, corners, 1)
    pygame.draw.lines(surf, accent, False, corners[:2], 2)
    pygame.draw.line(surf, accent, corners[2], corners[3], 2)
    pygame.draw.line(
        surf,
        (18, 68, 96),
        (rect.left + 12, rect.top + 17),
        (rect.right - 12, rect.top + 17),
        1,
    )
    if title:
        draw_text(surf, title, rect.left + 12, rect.top + 4, accent, "s")


def draw_button(surf, rect, label, accent, hovered=False):
    pygame.draw.rect(surf, (4, 17, 32), rect)
    pygame.draw.rect(surf, (18, 76, 110), rect, 1)
    pygame.draw.line(surf, accent, (rect.left + 8, rect.top), (rect.right - 8, rect.top), 2)
    if hovered:
        pygame.draw.rect(surf, CYAN, rect.inflate(8, 8), 2)
        pygame.draw.line(
            surf,
            CYAN,
            (rect.left + 8, rect.bottom - 3),
            (rect.right - 8, rect.bottom - 3),
            2,
        )
    image = engine.fonts["s"].render(label, False, accent)
    surf.blit(image, (rect.centerx - image.get_width() // 2, rect.centery - image.get_height() // 2))


def draw_shield(surf, x, y):
    pts = [(x, y), (x + 36, y), (x + 36, y + 22), (x + 18, y + 44), (x, y + 22)]
    pygame.draw.polygon(surf, (10, 70, 20), pts)
    pygame.draw.polygon(surf, GREEN, pts, 3)
    pygame.draw.line(surf, GREEN, (x + 9, y + 20), (x + 16, y + 28), 3)
    pygame.draw.line(surf, GREEN, (x + 16, y + 28), (x + 28, y + 11), 3)


def draw_padlock(surf, x, y):
    lock_color = (35, 185, 235)
    halo = (8, 57, 91)
    pygame.draw.ellipse(surf, halo, pygame.Rect(x - 9, y + 29, 50, 12), 1)
    pygame.draw.lines(
        surf,
        halo,
        False,
        [(x + 5, y + 17), (x + 5, y + 7), (x + 8, y + 3),
         (x + 24, y + 3), (x + 27, y + 7), (x + 27, y + 17)],
        5,
    )
    pygame.draw.lines(
        surf,
        lock_color,
        False,
        [(x + 7, y + 17), (x + 7, y + 8), (x + 10, y + 5),
         (x + 22, y + 5), (x + 25, y + 8), (x + 25, y + 17)],
        2,
    )
    body = pygame.Rect(x, y + 14, 32, 23)
    pygame.draw.rect(surf, (5, 35, 63), body)
    pygame.draw.rect(surf, lock_color, body, 2)
    pygame.draw.circle(surf, lock_color, (x + 16, y + 22), 3)
    pygame.draw.rect(surf, lock_color, pygame.Rect(x + 14, y + 23, 4, 7))


def draw_segmented_bar(surf, rect, percent, segments=20, color=CYAN):
    pygame.draw.rect(surf, (3, 12, 27), rect)
    pygame.draw.rect(surf, (17, 73, 105), rect, 1)
    gap = 2
    inner_width = max(0, rect.width - 4)
    segment_area = max(0, inner_width - gap * (segments - 1))
    filled = round(max(0, min(100, percent)) * segments / 100)
    for index in range(segments):
        segment_left = rect.x + 2 + round(index * segment_area / segments) + index * gap
        segment_right = rect.x + 2 + round((index + 1) * segment_area / segments) + index * gap
        segment = pygame.Rect(
            segment_left,
            rect.y + 2,
            max(1, segment_right - segment_left),
            max(1, rect.height - 4),
        )
        pygame.draw.rect(surf, color if index < filled else (6, 23, 39), segment)


def draw_header(surf, label, color):
    pygame.draw.rect(surf, (3, 11, 25), pygame.Rect(0, 0, W, 25))
    pygame.draw.line(surf, color, (0, 24), (W, 24), 1)
    draw_text(surf, "SECURE ACCESS SYSTEM", 10, 3, CYAN, "s")
    draw_text(surf, label, 10, 13, color, "s")

    # Progress bar: one segment per level in the current preset
    total = len(sorted_ids(game_data[engine.current_preset]))
    done = engine.current_level - 1
    if engine.state == "WIN" and is_last_exercise_of_level():
        done += 1
    draw_text(surf, "LEVEL", W - total * 13 - 38, 6, DIM, "s")
    for i in range(total):
        seg = pygame.Rect(W - total * 13 + i * 13, 6, 9, 8)
        if i < done:
            pygame.draw.rect(surf, GREEN, seg)
        else:
            pygame.draw.rect(surf, DIM, seg, 1)


def draw_code_box(surf, rect, title, lines, color, fill):
    pygame.draw.rect(surf, fill, rect)
    pygame.draw.rect(surf, color, rect, 2)
    draw_text(surf, title, rect.x + 8, rect.y + 4, color, "s")
    for i, line in enumerate(lines):
        draw_text(surf, line, rect.x + 10, rect.y + 20 + i * 14, WHITE)
