"""Rendering for the intro, exercise, and win screens."""

import pygame
import random
import math

import game_engine as engine
from game_engine import (
    get_exercise,
    get_level,
    is_last_exercise_of_level,
    is_last_level_of_preset,
    is_last_preset,
    sorted_ids,
)
from missions import game_data
from settings import (
    CYAN,
    COMPROMISED_BUTTON_RECT,
    DIM,
    GREEN,
    H,
    HINT_AFTER,
    MENU_BUTTON_RECT,
    RED,
    SCALE,
    WHITE,
    W,
    YELLOW,
    VICTORY_BUTTON_RECT,
)
from ui_components import (
    draw_background,
    draw_header,
    draw_panel,
    draw_button,
    draw_padlock,
    draw_shield,
    draw_text,
    draw_text_center,
    wrap_text,
)

# ======================================================================
# SCREENS
# ======================================================================
def draw_menu(surf):
    draw_panel(surf, pygame.Rect(15, 35, 420, 194), "GLOBAL NETWORK // SECURE ACCESS")
    draw_text_center(surf, "CYBER DEFENSE", 67, CYAN, "l")
    draw_text_center(surf, "MAINFRAME OPERATIONS CENTER", 96, CYAN, "s")
    lock_y = 112 + round(math.sin(pygame.time.get_ticks() / 360) * 2)
    draw_padlock(surf, 209, lock_y)
    story = (
        "AGENT CIPHER // You are the last line of defense. "
        "A rogue AI is breaching the global network. "
        "Patch the mainframe before it takes control."
    )
    for i, line in enumerate(wrap_text(story, "s", 370)):
        draw_text_center(surf, line, 163 + i * 14, WHITE, "s")

    draw_button(
        surf,
        pygame.Rect(MENU_BUTTON_RECT),
        "ACCESS MISSION 1: THE DATA BREACH",
        CYAN,
        engine.menu_button_hover,
    )


def draw_intro(surf):
    total_levels = len(sorted_ids(game_data[engine.current_preset]))
    total_ex = len(sorted_ids(get_level()))
    draw_header(surf, f"PRESET {engine.current_preset}  LEVEL {engine.current_level}/{total_levels}", CYAN)

    panel = pygame.Rect(32, 40, 386, 270)
    draw_panel(surf, panel, "MISSION BRIEFING // AUTHORIZED AGENT ONLY")
    pulse = round(math.sin(pygame.time.get_ticks() / 250) * 2)
    draw_shield(surf, 207 - pulse, 72 - pulse)
    draw_text_center(surf, "CONCEPT UNLOCKED", 133, GREEN, "s")
    draw_text_center(surf, get_level()["title"], 157, CYAN, "l")
    draw_text_center(surf, f"{total_ex} missions // LEVEL {engine.current_level}", 190, WHITE, "s")

    if (pygame.time.get_ticks() // 500) % 2 == 0:
        draw_text_center(surf, "> PRESS ENTER TO INITIALIZE <", 265, CYAN, "s")


def draw_lesson_overlay(surf):
    shade = pygame.Surface((W, H), pygame.SRCALPHA)
    shade.fill((0, 3, 12, 210))
    surf.blit(shade, (0, 0))

    panel = pygame.Rect(24, 61, W - 48, 228)
    draw_panel(surf, panel, "MISSION LESSON // F1 TO CLOSE", CYAN, (3, 13, 28))
    for index, line in enumerate(wrap_text(get_exercise()["lesson"], "s", W - 84)[:10]):
        draw_text(surf, line, 39, 91 + index * 15, WHITE, "s")
    draw_text(surf, "F1 // CLOSE BRIEFING", 39, 267, CYAN, "s")


def draw_comms_box(surf):
    dialogue = engine.active_dialogue
    speaker = dialogue["speaker"] if dialogue else "COMMS"
    accent = dialogue["color"] if dialogue else CYAN
    panel = pygame.Rect(214, 77, 204, 58)
    pygame.draw.rect(surf, (2, 12, 26), panel)
    pygame.draw.rect(surf, accent, panel, 1)
    pygame.draw.line(surf, accent, (panel.left + 5, panel.top + 13),
                     (panel.right - 5, panel.top + 13), 1)

    portrait = pygame.Rect(220, 94, 27, 34)
    pygame.draw.rect(surf, (4, 23, 39), portrait)
    pygame.draw.rect(surf, accent, portrait, 1)
    pygame.draw.rect(surf, accent, pygame.Rect(226, 99, 15, 16))
    pygame.draw.rect(surf, (8, 15, 28), pygame.Rect(229, 103, 3, 3))
    pygame.draw.rect(surf, (8, 15, 28), pygame.Rect(236, 103, 3, 3))
    pygame.draw.rect(surf, WHITE, pygame.Rect(231, 110, 7, 2))
    pygame.draw.rect(surf, accent, pygame.Rect(224, 116, 19, 9))
    if speaker == "ROGUE_AI":
        pygame.draw.line(surf, RED, (222, 101), (245, 101), 1)
        pygame.draw.line(surf, RED, (222, 113), (245, 113), 1)

    label = speaker if dialogue else "COMMS"
    draw_text(surf, label, 253, 80, accent, "s")
    if dialogue:
        visible_text = dialogue["text"][:dialogue["visible"]]
    else:
        visible_text = "SECURE CHANNEL IDLE"
    for index, line in enumerate(wrap_text(visible_text, "s", 157)[:2]):
        draw_text(surf, line, 253, 96 + index * 13, WHITE, "s")


def draw_apply(surf):
    ex = get_exercise()
    mode = ex["mode"]
    debug = mode == "DEBUG"

    pygame.draw.rect(surf, (2, 8, 19), pygame.Rect(0, 0, W, 20))
    pygame.draw.line(surf, (18, 68, 96), (0, 19), (W, 19), 1)
    progress = engine.progress_display
    progress_rect = pygame.Rect(8, 12, 204, 6)
    takeover_rect = pygame.Rect(224, 12, 218, 6)
    draw_text(surf, f"PROGRESS {round(progress)}%", 8, 2, CYAN, "s")
    draw_text(surf, f"ROGUE AI TAKEOVER {engine.takeover_percent}%", 224, 2, RED, "s")
    pygame.draw.rect(surf, (7, 27, 42), progress_rect)
    pygame.draw.rect(
        surf,
        CYAN,
        pygame.Rect(progress_rect.x, progress_rect.y, round(progress_rect.width * progress / 100), progress_rect.height),
    )
    pygame.draw.rect(surf, CYAN, progress_rect, 1)
    pygame.draw.rect(surf, (54, 13, 26), takeover_rect)
    pygame.draw.rect(
        surf,
        RED,
        pygame.Rect(
            takeover_rect.x,
            takeover_rect.y,
            round(takeover_rect.width * engine.takeover_percent / 100),
            takeover_rect.height,
        ),
    )
    pygame.draw.rect(surf, RED, takeover_rect, 1)

    ticket_id = engine.current_preset * 1000 + engine.current_level * 10 + engine.current_exercise
    priority = ex["priority"]
    ticket_prefix = f"TICKET #{ticket_id} [{priority}] "
    ticket_font = engine.fonts["s"]
    ticket_text = ex["ticket"]
    available_width = W - 24 - ticket_font.size(ticket_prefix)[0]
    while ticket_text and ticket_font.size(ticket_text + "...")[0] > available_width:
        ticket_text = ticket_text[:-1]
    if ticket_text != ex["ticket"]:
        ticket_text = ticket_text.rstrip(" ,.!") + "..."
    priority_colors = {
        "LOW": GREEN,
        "MED": CYAN,
        "HIGH": YELLOW,
        "CRITICAL": RED,
    }
    pygame.draw.rect(surf, (4, 15, 29), pygame.Rect(8, 24, W - 16, 20))
    draw_text(surf, ticket_prefix, 12, 29, priority_colors[priority], "s")
    draw_text(surf, ticket_text, 12 + ticket_font.size(ticket_prefix)[0], 29, WHITE, "s")

    terminal_panel = pygame.Rect(12, 50, W - 24, 290)
    draw_panel(surf, terminal_panel, "", CYAN, (3, 11, 24))
    title_bar = pygame.Rect(13, 51, W - 26, 21)
    pygame.draw.rect(surf, (5, 23, 41), title_bar)
    pygame.draw.line(surf, (24, 93, 128), (title_bar.left, title_bar.bottom), (title_bar.right, title_bar.bottom), 1)
    draw_text(surf, "SECURE_CONSOLE v1.0", 22, 56, CYAN, "s")
    status_text = f"XP {engine.xp} // STREAK x{engine.streak}"
    status_x = title_bar.right - 8 - ticket_font.size(status_text)[0]
    draw_text(surf, status_text, status_x, 56, DIM, "s")

    draw_text(surf, "mainframe.py // CONTEXT", 30, 78, CYAN, "s")
    if mode == "SPEED":
        time_left = max(0, engine.speed_timer_frames) / 60
        context_lines = [
            "041  RESPONSE WINDOW // 20 SEC",
            "042  TYPE THE ANSWER BELOW",
            f"043  TIME REMAINING // {time_left:04.1f}s",
        ]
    elif mode == "BOSS":
        context_lines = [
            "041  BOSS FIREWALL // MULTI-CONCEPT PATCH",
            "042      # arrange each defense step",
            "043  " + ex["ticket"],
        ]
    else:
        context_lines = [
            "041  def patch():",
            "042      # policy",
            f"043  {ex['broken_code'] if debug else '# enter patch here'}",
        ]
    context_font = engine.fonts["m"]
    for index, line in enumerate(context_lines):
        original_line = line
        while line and context_font.size(line + "...")[0] > 170:
            line = line[:-1]
        if line != original_line:
            line = line.rstrip() + "..."
        draw_text(surf, line, 30, 93 + index * 13, RED if debug and index == 2 else DIM, "m")
    draw_comms_box(surf)

    log_panel = pygame.Rect(22, 137, W - 44, 132)
    pygame.draw.rect(surf, (1, 7, 17), log_panel)
    pygame.draw.rect(surf, (19, 76, 105), log_panel, 1)
    if mode == "SPEED":
        draw_text(surf, "RAPID QUESTION //", 30, 147, CYAN, "s")
        for index, line in enumerate(wrap_text(ex["question"], "s", W - 64)[:3]):
            draw_text(surf, line, 30, 164 + index * 16, WHITE, "s")
        time_left = max(0, engine.speed_timer_frames) / 60
        timer_bar = pygame.Rect(30, 224, W - 60, 8)
        pygame.draw.rect(surf, (46, 13, 24), timer_bar)
        pygame.draw.rect(
            surf,
            RED if time_left <= 5 else CYAN,
            pygame.Rect(timer_bar.x, timer_bar.y, round(timer_bar.width * time_left / 20), timer_bar.height),
        )
        pygame.draw.rect(surf, (19, 76, 105), timer_bar, 1)
    elif mode == "CHOOSE":
        for index, option in enumerate(ex["options"]):
            marker = ">" if index == engine.choice_index else " "
            color = CYAN if index == engine.choice_index else WHITE
            draw_text(surf, f"{marker} {index + 1}. {option}", 30, 148 + index * 27, color, "s")
    elif mode in ("ORDER", "BOSS"):
        for index, line in enumerate(engine.order_items):
            marker = ">" if index == engine.order_cursor else " "
            color = YELLOW if index == engine.order_cursor else WHITE
            draw_text(surf, f"{marker} {index + 1}. {line}", 30, 148 + index * 27, color, "s")
    else:
        for index, line in enumerate(engine.console_log[-8:]):
            visible_text = line["text"][:line["visible"]]
            draw_text(surf, visible_text, 30, 143 + index * 14, line["color"], "s")

    if engine.attempts >= HINT_AFTER:
        hint = "HINT // " + ex["hint"]
        while hint and ticket_font.size(hint + "...")[0] > W - 64:
            hint = hint[:-1]
        if hint != "HINT // " + ex["hint"]:
            hint = hint.rstrip(" ,.!") + "..."
        draw_text(surf, hint, 30, 271, YELLOW, "s")

    if mode == "CHOOSE":
        input_label = "UP/DOWN: SELECT  //  ENTER: CONFIRM"
    elif mode in ("ORDER", "BOSS"):
        input_label = "UP/DOWN: SELECT  //  LEFT/RIGHT: MOVE"
    elif mode == "SPEED":
        input_label = f"RAPID RESPONSE // {max(0, engine.speed_timer_frames) / 60:04.1f}s"
    else:
        input_label = "INPUT // PYTHON PATCH"
    draw_text(surf, input_label, 30, 282, DIM, "s")
    console = pygame.Rect(22, 296, W - 44, 30)
    pygame.draw.rect(surf, (1, 7, 17), console)
    pygame.draw.rect(surf, (22, 91, 124), console, 1)
    if mode in ("WRITE", "DEBUG", "SPEED"):
        prompt = ">>> "
        before_cursor = prompt + engine.typed[:engine.cursor_pos]
        after_cursor = engine.typed[engine.cursor_pos:]
        input_font = engine.fonts["m"]
        input_x, input_y = 31, 303
        before_image = input_font.render(before_cursor, False, GREEN)
        surf.blit(before_image, (input_x, input_y))
        cursor_x = input_x + before_image.get_width()
        cursor_y = input_y + 1
        cursor_visible = (pygame.time.get_ticks() // 500) % 2 == 0
        cursor_gap = 8 if cursor_visible else 0
        if cursor_visible:
            pygame.draw.rect(surf, GREEN, pygame.Rect(cursor_x, cursor_y, 7, 13))
        after_image = input_font.render(after_cursor, False, GREEN)
        surf.blit(after_image, (cursor_x + cursor_gap, input_y))
    else:
        draw_text(surf, "ENTER: SUBMIT", 31, 303, GREEN, "m")

    draw_text(
        surf,
        "ENTER // F1 // CTRL+C/V // CTRL+/- VOL // CTRL+M/R",
        30,
        330,
        DIM,
        "s",
    )
    if engine.lesson_open:
        draw_lesson_overlay(surf)
    if engine.flash > 0 and engine.flash_color == GREEN and not engine.reduce_effects:
        pygame.draw.rect(surf, GREEN, terminal_panel, 2)


def draw_win(surf):
    ex = get_exercise()
    level_done = is_last_exercise_of_level()
    preset_done = level_done and is_last_level_of_preset()

    draw_header(surf, f"LEVEL {engine.current_level} // EXERCISE CLEARED", GREEN)
    draw_panel(surf, pygame.Rect(32, 40, 386, 270), "MISSION DEBRIEF // PATCH VERIFIED")
    if level_done and engine.unlock_animation_timer > 0:
        draw_unlock_lock(surf)
    else:
        draw_shield(surf, 207, 57)

    if preset_done:
        draw_text_center(surf, f"PRESET {engine.current_preset} SECURED!", 115, GREEN, "l")
        draw_text_center(surf, "You patched every bug in this preset!", 143, WHITE, "s")
    elif level_done:
        draw_text_center(surf, "LEVEL CLEARED!", 115, GREEN, "l")
        draw_text_center(surf, f"Completed: {get_level()['title']}", 143, WHITE, "s")
    else:
        draw_text_center(surf, "EXERCISE CLEARED!", 115, GREEN, "l")
        draw_text_center(surf, f"{get_level()['title']}  -  {engine.current_exercise}/{len(sorted_ids(get_level()))}",
                         143, WHITE, "s")

    box = pygame.Rect(52, 181, 346, 50)
    draw_panel(surf, box, "PATCH ACCEPTED // YOUR CODE", GREEN, (5, 20, 20))
    if ex["mode"] in ("ORDER", "BOSS"):
        draw_text(surf, "SECURITY ORDER VERIFIED", 65, 209, GREEN, "s")
    else:
        draw_text(surf, ex["expected"], 65, 209, GREEN, "s")

    if (pygame.time.get_ticks() // 500) % 2 == 0:
        if preset_done:
            label = "> PRESS ENTER TO CONTINUE <" if not is_last_preset() else "> PRESS ENTER TO PLAY AGAIN <"
        elif level_done:
            label = "> PRESS ENTER FOR NEXT LEVEL <"
        else:
            label = "> PRESS ENTER FOR NEXT EXERCISE <"
        draw_text_center(surf, label, 267, CYAN, "s")


def draw_unlock_lock(surf, x=199, y=57):
    elapsed = 120 - engine.unlock_animation_timer
    lock_y = y + round(math.sin(elapsed / 8) * 2)
    opened = engine.unlock_animation_timer < 90
    body = pygame.Rect(x, lock_y + 18, 42, 32)
    pygame.draw.rect(surf, (5, 35, 63), body)
    pygame.draw.rect(surf, GREEN, body, 2)
    if opened:
        shackle = [(x + 8, lock_y + 19), (x + 8, lock_y + 7), (x + 12, lock_y + 3),
                   (x + 30, lock_y + 3), (x + 34, lock_y + 8), (x + 34, lock_y + 13)]
    else:
        shackle = [(x + 8, lock_y + 19), (x + 8, lock_y + 8), (x + 12, lock_y + 4),
                   (x + 30, lock_y + 4), (x + 34, lock_y + 8), (x + 34, lock_y + 19)]
    pygame.draw.lines(surf, GREEN, False, shackle, 3)
    pygame.draw.circle(surf, GREEN, (x + 21, lock_y + 30), 3)


def draw_boss_intro(surf):
    draw_panel(surf, pygame.Rect(28, 48, 394, 254), "ROGUE AI // BOSS FIREWALL", RED, (24, 5, 16))
    draw_text_center(surf, "BOSS PROTOCOL", 89, RED, "l")
    draw_text_center(surf, get_level()["title"].upper(), 126, YELLOW, "s")
    draw_text_center(surf, "Combine every concept from this level.", 157, WHITE, "s")
    draw_text_center(surf, "Rebuild the security chain under pressure.", 177, CYAN, "s")
    if engine.active_dialogue:
        message = engine.active_dialogue["text"][:engine.active_dialogue["visible"]]
        for index, line in enumerate(wrap_text(message, "s", 350)[:2]):
            draw_text_center(surf, line, 217 + index * 14, RED, "s")
    if (pygame.time.get_ticks() // 350) % 2 == 0:
        draw_text_center(surf, "> PRESS ENTER TO ENGAGE <", 272, YELLOW, "s")


def draw_victory(surf):
    title_font = pygame.font.SysFont(
        "couriernew,courier,dejavusansmono,consolas,monospace",
        34,
        bold=True,
    )
    draw_panel(surf, pygame.Rect(24, 42, 402, 264), "GLOBAL NETWORK // ALL THREATS NEUTRALIZED")
    if engine.unlock_animation_timer > 0:
        draw_unlock_lock(surf, 383, 56)
    title = title_font.render("SYSTEM SECURED", False, GREEN)
    surf.blit(title, ((W - title.get_width()) // 2, 95))
    draw_text_center(surf, "Mainframe saved. Rogue AI neutralized.", 150, WHITE, "s")

    draw_button(
        surf,
        pygame.Rect(VICTORY_BUTTON_RECT),
        "RETURN TO MAIN MENU",
        GREEN,
    )


def draw_compromised(surf):
    draw_panel(surf, pygame.Rect(24, 42, 402, 264), "ROGUE AI // CONTROL LOST", RED, (24, 5, 16))
    title_font = pygame.font.SysFont(
        "couriernew,courier,dejavusansmono,consolas,monospace",
        29,
        bold=True,
    )
    title = title_font.render("SYSTEM COMPROMISED", False, RED)
    surf.blit(title, ((W - title.get_width()) // 2, 102))
    draw_text_center(surf, "Rogue AI takeover reached 100%.", 151, WHITE, "s")
    draw_text_center(surf, f"Rebooting restarts LEVEL {engine.current_level}.", 171, CYAN, "s")
    draw_button(
        surf,
        pygame.Rect(COMPROMISED_BUTTON_RECT),
        "REBOOT CURRENT LEVEL",
        RED,
    )
    draw_text_center(surf, "PRESS ENTER TO REDEPLOY", 307, DIM, "s")


def draw_progress_notifications(surf):
    if engine.milestone_banner_timer > 0 and engine.milestone_banner:
        width = 218
        banner_y = {
            "APPLY": 137,
            "WIN": 158,
            "GAMEOVER_WIN": 200,
        }[engine.state]
        banner = pygame.Rect((W - width) // 2, banner_y, width, 19)
        pygame.draw.rect(surf, (4, 22, 36), banner)
        pygame.draw.rect(surf, CYAN, banner, 1)
        draw_text_center(surf, engine.milestone_banner, banner.y + 4, CYAN, "s")
    if engine.combo_popup_timer > 0:
        combo_y = 222 if engine.state == "GAMEOVER_WIN" else 244
        draw_text_center(surf, engine.combo_popup_text, combo_y, YELLOW, "m")


def draw_frame(canvas):
    draw_background(canvas)
    if engine.state == "MENU":
        draw_menu(canvas)
    elif engine.state == "INTRO":
        draw_intro(canvas)
    elif engine.state == "BOSS_INTRO":
        draw_boss_intro(canvas)
    elif engine.state == "APPLY":
        draw_apply(canvas)
    elif engine.state == "WIN":
        draw_win(canvas)
    elif engine.state == "GAMEOVER_WIN":
        draw_victory(canvas)
    elif engine.state == "GAMEOVER_LOSS":
        draw_compromised(canvas)

    if engine.state in ("APPLY", "WIN", "GAMEOVER_WIN"):
        draw_progress_notifications(canvas)

    for p in engine.particles:
        pygame.draw.rect(canvas, p["color"], pygame.Rect(int(p["x"]), int(p["y"]), 3, 3))

    for floating_text in engine.floating_texts:
        image = engine.fonts["m"].render(
            floating_text["text"],
            False,
            GREEN,
        )
        image.set_alpha(round(255 * floating_text["timer"] / 60))
        canvas.blit(
            image,
            ((W - image.get_width()) // 2, floating_text["y"]),
        )
        floating_text["y"] -= 2
        floating_text["timer"] -= 1
    engine.floating_texts = [
        floating_text for floating_text in engine.floating_texts
        if floating_text["timer"] > 0
    ]

    if engine.glitch_timer > 0:
        for line in engine.glitch_lines:
            pygame.draw.rect(
                canvas,
                RED,
                pygame.Rect(0, line["y"], W, line["thickness"]),
            )
        engine.glitch_timer -= 1

    if engine.flash > 0 and not engine.reduce_effects:
        pygame.draw.rect(canvas, engine.flash_color, pygame.Rect(0, 0, W, H), 3)

    if engine.transition_timer > 0:
        fade = pygame.Surface((W, H), pygame.SRCALPHA)
        alpha = round(255 * engine.transition_timer / 30)
        fade.fill((0, 0, 0, alpha))
        canvas.blit(fade, (0, 0))
        engine.transition_timer -= 1


def present(screen, canvas):
    s = 0 if engine.reduce_effects else int(engine.shake)
    ox = random.randint(-s, s) if s > 0 else 0
    oy = random.randint(-s, s) if s > 0 else 0
    scaled = pygame.transform.scale(canvas, (W * SCALE, H * SCALE))   # retro pixel scaling
    screen.fill((0, 0, 0))
    screen.blit(scaled, (ox * SCALE, oy * SCALE))
    pygame.display.flip()
