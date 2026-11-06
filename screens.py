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
from missions import concept_library
from settings import (
    CYAN,
    BOSS_HELPER_BUTTON_RECT,
    BOSS_LIBRARY_BUTTON_RECT,
    CONCEPT_BACK_BUTTON_RECT,
    CONCEPT_LIST_RECT,
    CONCEPT_TRY_BUTTON_RECT,
    DIM,
    GREEN,
    H,
    HELPER_BUTTON_RECT,
    HINT_AFTER,
    LIBRARY_BUTTON_RECT,
    LEVEL_COMPLETE_BUTTON_RECT,
    LOSS_RETRY_BUTTON_RECT,
    LOSS_ROADMAP_BUTTON_RECT,
    MISSION_BUTTON_RECT,
    MISSION_LIBRARY_BUTTON_RECT,
    MISSION_SETTINGS_BUTTON_RECT,
    MASTER_BUTTON_RECT,
    MENU_BUTTON_RECT,
    RED,
    RESUME_BUTTON_RECT,
    ROADMAP_BUTTON_RECT,
    TRAINING_BUTTON_RECT,
    WHITE,
    W,
    YELLOW,
    VICTORY_BUTTON_RECT,
    get_viewport,
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
def draw_story(surf):
    draw_panel(surf, pygame.Rect(28, 54, 394, 242), "GLOBAL NETWORK // DISTRESS SIGNAL", CYAN)
    draw_text_center(surf, "CYBER DEFENSE", 91, CYAN, "l")
    draw_text_center(surf, engine.STORY_LINES[engine.story_index], 157, WHITE, "m")
    draw_text_center(surf, "A NEW AGENT. ONE LAST CHANCE.", 204, GREEN, "s")
    draw_text_center(surf, "PRESS ANY KEY TO SKIP", 273, DIM, "s")


def draw_mode_select(surf):
    actions = engine.mode_select_actions()
    engine.mode_selection %= len(actions)
    draw_header(surf, "CHOOSE YOUR TRAINING", CYAN)
    draw_panel(surf, pygame.Rect(25, 42, 400, 288), "SELECT A MODE")
    training_card = pygame.Rect(35, 75, 182, 146)
    mission_card = pygame.Rect(233, 75, 182, 146)
    draw_panel(surf, training_card, "PRACTICE", GREEN, (4, 17, 30))
    draw_panel(surf, mission_card, "CHALLENGE", CYAN, (4, 17, 30))
    draw_button(
        surf,
        pygame.Rect(TRAINING_BUTTON_RECT),
        "TRAINING",
        GREEN,
        engine.hovered_button == "training" or engine.mode_selection == actions.index("training"),
    )
    draw_button(
        surf,
        pygame.Rect(MISSION_BUTTON_RECT),
        "PLAY MISSION",
        CYAN,
        engine.hovered_button == "mission" or engine.mode_selection == actions.index("mission"),
    )
    for center_x, line, y, color in (
        (126, "Learn at your own pace.", 163, WHITE),
        (126, "No timer. No fail.", 181, DIM),
        (324, "Timed challenges.", 163, WHITE),
        (324, "You can fail and resume.", 181, DIM),
    ):
        image = engine.fonts["s"].render(line, False, color)
        surf.blit(image, (center_x - image.get_width() // 2, y))
    if engine.has_saved_game():
        draw_button(
            surf,
            pygame.Rect(RESUME_BUTTON_RECT),
            "RESUME SAVED GAME",
            YELLOW,
            engine.hovered_button == "resume" or engine.mode_selection == actions.index("resume"),
        )
    master_unlocked = engine.all_levels_completed()
    draw_button(
        surf,
        pygame.Rect(MASTER_BUTTON_RECT),
        "MASTER MODE" if master_unlocked else "MASTER LOCKED",
        YELLOW if master_unlocked else DIM,
        engine.hovered_button == "master"
        or (master_unlocked and engine.mode_selection == actions.index("master")),
    )
    draw_button(
        surf,
        pygame.Rect(LIBRARY_BUTTON_RECT),
        "CONCEPT LIBRARY",
        YELLOW,
        engine.hovered_button == "library" or engine.mode_selection == actions.index("library"),
    )
    controls = "ARROWS SELECT // ENTER OPEN"
    if engine.has_saved_game():
        shortcuts = "1 TRAINING  2 MISSION  3 RESUME  4 LIBRARY  M MASTER"
    else:
        shortcuts = "1 TRAINING  2 MISSION  4 LIBRARY  M MASTER"
    draw_text_center(surf, controls, 307, DIM, "s")
    draw_text_center(surf, shortcuts, 322, DIM, "s")
    if engine.save_error:
        draw_text_center(surf, "SAVE ERROR // CHECK DISK ACCESS", 334, RED, "s")


def draw_concept_library(surf):
    concept_names = tuple(concept_library)
    draw_header(surf, "CONCEPT LIBRARY", CYAN)
    draw_panel(surf, pygame.Rect(9, 52, 136, 230), "TOPICS", CYAN)
    for index, name in enumerate(concept_names):
        row = pygame.Rect(
            CONCEPT_LIST_RECT[0],
            CONCEPT_LIST_RECT[1] + index * 27,
            CONCEPT_LIST_RECT[2],
            CONCEPT_LIST_RECT[3],
        )
        selected = index == engine.selected_concept
        color = CYAN if selected else DIM
        pygame.draw.rect(surf, (5, 23, 41) if selected else (4, 14, 30), row)
        pygame.draw.rect(surf, color, row, 1)
        draw_text(surf, name, row.x + 5, row.y + 6, color, "s")

    name = concept_names[engine.selected_concept]
    concept = concept_library[name]
    panel = pygame.Rect(151, 52, 288, 230)
    draw_panel(surf, panel, name.upper(), CYAN)
    for index, line in enumerate(wrap_text(concept["explanation"], "s", 254)[:3]):
        draw_text(surf, line, 164, 78 + index * 14, WHITE, "s")

    example_panel = pygame.Rect(162, 126, 266, 55)
    draw_panel(surf, example_panel, "EXAMPLE", GREEN, (3, 18, 27))
    for index, code_line in enumerate(concept["example"].splitlines()[:2]):
        draw_text(surf, code_line, 173, 148 + index * 13, GREEN, "s")

    draw_text(surf, "TRY THIS:", 164, 191, YELLOW, "s")
    for index, line in enumerate(wrap_text(concept["task"], "s", 254)[:3]):
        draw_text(surf, line, 164, 207 + index * 13, WHITE, "s")

    draw_button(
        surf,
        pygame.Rect(CONCEPT_BACK_BUTTON_RECT),
        "BACK",
        DIM,
        engine.hovered_button == "concept_back",
    )
    draw_button(
        surf,
        pygame.Rect(CONCEPT_TRY_BUTTON_RECT),
        "TRY IT",
        GREEN,
        engine.hovered_button == "concept_try",
    )
    draw_text_center(surf, "UP/DOWN SELECT // ENTER TRY", 332, DIM, "s")


def draw_concept_practice(surf):
    name = tuple(concept_library)[engine.selected_concept]
    concept = concept_library[name]
    draw_header(surf, "CONCEPT PRACTICE", CYAN)
    draw_panel(surf, pygame.Rect(25, 44, 400, 240), name.upper(), CYAN)
    draw_text_center(surf, "TRY IT YOURSELF", 78, YELLOW, "s")
    for index, line in enumerate(wrap_text(concept["task"], "s", 340)[:3]):
        draw_text_center(surf, line, 106 + index * 15, WHITE, "s")
    draw_text(surf, "EXAMPLE // " + concept["example"].replace("\n", " "), 49, 158, GREEN, "s")
    draw_text(surf, ">>>", 49, 197, CYAN, "m")
    input_box = pygame.Rect(77, 191, 320, 27)
    pygame.draw.rect(surf, (1, 7, 17), input_box)
    pygame.draw.rect(surf, CYAN, input_box, 1)
    draw_text(surf, engine.concept_typed, 84, 198, WHITE, "m")
    if engine.concept_feedback:
        color = GREEN if engine.concept_feedback.startswith("Correct!") else YELLOW
        for index, line in enumerate(wrap_text(engine.concept_feedback, "s", 340)[:2]):
            draw_text_center(surf, line, 235 + index * 14, color, "s")
    else:
        draw_text_center(surf, "TYPE YOUR ANSWER // PRESS ENTER TO CHECK", 238, DIM, "s")
    draw_button(
        surf,
        pygame.Rect(CONCEPT_BACK_BUTTON_RECT),
        "BACK TO LIBRARY",
        DIM,
        engine.hovered_button == "concept_back",
    )
    draw_button(
        surf,
        pygame.Rect(CONCEPT_TRY_BUTTON_RECT),
        "CHECK ANSWER",
        GREEN,
        engine.hovered_button == "concept_try",
    )


def draw_roadmap(surf):
    level_ids = sorted_ids(game_data[engine.current_preset])
    selected_level = game_data[engine.current_preset][engine.roadmap_selection]
    current_title = selected_level["title"]
    draw_header(surf, "CAMPAIGN ROADMAP", CYAN)
    draw_text_center(
        surf,
        f"LEVEL {engine.roadmap_selection}: {current_title.upper()}",
        34,
        YELLOW,
        "s",
    )
    draw_panel(surf, pygame.Rect(10, 55, 430, 222), "4 TASKS + 1 BOSS")
    for level_index, level_id in enumerate(level_ids):
        level = game_data[engine.current_preset][level_id]
        card = pygame.Rect(14 + level_index * 106, 75, 100, 185)
        level_done = level_id in engine.completed_levels
        is_unlocked = engine.is_level_unlocked(level_id)
        is_selected = level_id == engine.roadmap_selection
        is_played = level_id in engine.played_levels
        accent = (
            GREEN if level_done else
            YELLOW if is_selected else
            CYAN if is_unlocked else DIM
        )
        draw_panel(surf, card, f"LEVEL {level_id}", accent, (4, 14, 30))
        if is_selected:
            pygame.draw.rect(surf, accent, card.inflate(4, 4), 1)

        def draw_card_text(text, y, color):
            image = engine.fonts["s"].render(text, False, color)
            surf.blit(image, (card.centerx - image.get_width() // 2, y))

        title_lines = wrap_text(level["title"], "s", 80)[:3]
        for line_index, line in enumerate(title_lines):
            draw_card_text(line, 103 + line_index * 13, WHITE if is_unlocked else DIM)

        dot_centers = [card.left + offset for offset in (10, 28, 46, 64, 86)]
        pygame.draw.line(surf, (25, 55, 75), (dot_centers[0], 167), (dot_centers[-1], 167), 1)
        exercise_ids = sorted_ids(level)
        next_exercise = next(
            (
                exercise_id for exercise_id in exercise_ids
                if (level_id, exercise_id) not in engine.completed_exercises
            ),
            exercise_ids[0],
        )
        for exercise_index, exercise_id in enumerate(exercise_ids):
            done = level_done or (level_id, exercise_id) in engine.completed_exercises
            current = is_selected and exercise_id == next_exercise
            hovered = engine.hovered_button == f"task_{level_id}_{exercise_id}"
            color = GREEN if done else (YELLOW if current or hovered else CYAN if is_unlocked else DIM)
            radius = 5 if exercise_index == 4 else 3
            pygame.draw.circle(surf, color, (dot_centers[exercise_index], 167), radius)
            label = "B" if exercise_index == 4 else str(exercise_index + 1)
            label_image = engine.fonts["s"].render(label, False, color)
            surf.blit(label_image, (dot_centers[exercise_index] - label_image.get_width() // 2, 178))

        status = (
            "DONE" if level_done else
            "PLAYED" if is_played else
            "READY" if is_unlocked else "LOCKED"
        )
        status_color = GREEN if level_done else YELLOW if is_played or is_selected else CYAN if is_unlocked else DIM
        draw_card_text(status, 209, status_color)
        draw_card_text("4 TASKS + BOSS", 230, DIM)

    draw_button(
        surf,
        pygame.Rect(ROADMAP_BUTTON_RECT),
        (
            f"START MASTER LEVEL {engine.roadmap_selection}"
            if engine.master_replay
            else f"START LEVEL {engine.roadmap_selection}"
        ),
        CYAN,
        engine.hovered_button == "roadmap",
    )
    roadmap_help = engine.roadmap_notice or (
        "ARROWS: LEVEL // CLICK OR 1-5: TASK // 5 = BOSS"
        if not engine.master_replay
        else "MASTER // ARROWS: LEVEL // CLICK OR 1-5: TASK"
    )
    help_color = YELLOW if engine.roadmap_notice else DIM
    draw_text_center(surf, roadmap_help, 278, help_color, "s")
    if engine.save_error:
        draw_text(surf, "SAVE ERROR", 12, 335, RED, "s")


def draw_level_complete(surf):
    draw_header(surf, f"LEVEL {engine.current_level} // COMPLETE", GREEN)
    draw_panel(surf, pygame.Rect(28, 43, 394, 248), "SECURITY LAYER RESTORED", GREEN)
    draw_shield(surf, 207, 63)
    draw_text_center(surf, "LEVEL COMPLETE!", 125, GREEN, "l")
    draw_text_center(surf, f"SCORE {engine.score}  //  XP {engine.xp}", 159, WHITE, "m")
    level_ids = sorted_ids(game_data[engine.current_preset])
    if engine.current_level < level_ids[-1]:
        next_level = engine.current_level + 1
        next_title = game_data[engine.current_preset][next_level]["title"]
        unlock_text = f"UNLOCKED: LEVEL {next_level} // {next_title.upper()}"
    else:
        unlock_text = "ALL FOUR LEVELS COMPLETE"
    for index, line in enumerate(wrap_text(unlock_text, "s", 340)[:2]):
        draw_text_center(surf, line, 209 + index * 14, CYAN, "s")
    draw_button(
        surf,
        pygame.Rect(LEVEL_COMPLETE_BUTTON_RECT),
        "CONTINUE TO ROADMAP",
        GREEN,
        engine.hovered_button == "level_complete",
    )


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
    exercise = get_exercise()
    concept, has_mission, mission = exercise["lesson"].partition("MISSION:")
    if not has_mission:
        concept = exercise["lesson"]
        mission = exercise.get("order_goal", exercise["ticket"])
    mission = mission.split(" BOSS CHALLENGE:", 1)[0].strip()

    draw_text(surf, "CONCEPT", 40, 91, YELLOW, "s")
    for index, line in enumerate(wrap_text(concept.strip(), "s", W - 84)[:3]):
        draw_text(surf, line, 40, 108 + index * 14, WHITE, "s")
    draw_text(surf, "YOUR MISSION", 40, 158, YELLOW, "s")
    for index, line in enumerate(wrap_text(mission, "s", W - 84)[:5]):
        draw_text(surf, line, 40, 175 + index * 14, WHITE, "s")
    draw_text(surf, "F1 // CLOSE", 40, 267, CYAN, "s")


def draw_comms_box(surf):
    dialogue = engine.active_dialogue
    speaker = dialogue["speaker"] if dialogue else "HANDLER"
    accent = dialogue["color"] if dialogue else CYAN
    panel = pygame.Rect(208, 91, 230, 44)
    pygame.draw.rect(surf, (2, 12, 26), panel)
    pygame.draw.rect(surf, accent, panel, 1)
    draw_text(surf, speaker, 214, 93, accent, "s")
    visible_text = (
        dialogue["text"][:dialogue["visible"]]
        if dialogue else engine.last_comms_message
    )
    for index, line in enumerate(wrap_text(visible_text, "s", 218)[:2]):
        draw_text(surf, line, 214, 106 + index * 12, WHITE, "s")
    draw_button(
        surf,
        pygame.Rect(HELPER_BUTTON_RECT),
        "HINT",
        YELLOW,
        engine.hovered_button == "helper",
    )
    draw_button(
        surf,
        pygame.Rect(MISSION_LIBRARY_BUTTON_RECT),
        "LIBRARY",
        CYAN,
        engine.hovered_button == "mission_library",
    )


def draw_apply(surf):
    ex = get_exercise()
    mode = ex["mode"]
    if mode == "BOSS":
        draw_boss_apply(surf, ex)
        return
    debug = mode == "DEBUG"
    exercise_ids = sorted_ids(get_level())
    task_number = exercise_ids.index(engine.current_exercise) + 1
    level_total = len(exercise_ids)
    level_done = sum(
        (engine.current_level, exercise_id) in engine.completed_exercises
        for exercise_id in exercise_ids
    )
    level_progress = level_done * 100 / level_total
    progress_width = 198
    takeover_width = 194

    pygame.draw.rect(surf, (2, 8, 19), pygame.Rect(0, 0, W, 44))
    pygame.draw.line(surf, (18, 68, 96), (0, 43), (W, 43), 1)
    draw_text(surf, f"LEVEL {engine.current_level} · TASK {task_number}/{level_total}", 8, 2, CYAN, "s")
    draw_text(surf, f"LEVEL PROGRESS {round(level_progress)}%", 151, 2, GREEN, "s")
    if engine.play_mode == "TRAINING":
        draw_text(surf, "TRAINING", 306, 2, GREEN, "s")
    else:
        draw_text(surf, f"TAKEOVER {engine.takeover_percent}%", 286, 2, RED, "s")

    progress_rect = pygame.Rect(8, 17, progress_width, 6)
    pygame.draw.rect(surf, (7, 27, 42), progress_rect)
    pygame.draw.rect(
        surf,
        GREEN,
        pygame.Rect(progress_rect.x, progress_rect.y, round(progress_rect.width * level_progress / 100), progress_rect.height),
    )
    pygame.draw.rect(surf, GREEN, progress_rect, 1)
    if engine.play_mode == "MISSION":
        takeover_rect = pygame.Rect(220, 17, takeover_width, 6)
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

    draw_settings_icon(surf)
    if engine.takeover_tooltip_timer > 0:
        tooltip = pygame.Rect(218, 24, 220, 27)
        pygame.draw.rect(surf, (9, 25, 42), tooltip)
        pygame.draw.rect(surf, YELLOW, tooltip, 1)
        for index, line in enumerate(wrap_text("Wrong answers raise it. At 100% you fail.", "s", 208)):
            draw_text(surf, line, 224, 26 + index * 11, YELLOW, "s")

    ticket_panel = pygame.Rect(8, 52, W - 16, 14)
    pygame.draw.rect(surf, (4, 15, 29), ticket_panel)
    pygame.draw.rect(surf, (18, 68, 96), ticket_panel, 1)
    draw_text_center(surf, ex["ticket"], 53, WHITE, "s")

    terminal_panel = pygame.Rect(12, 67, W - 24, 273)
    draw_panel(surf, terminal_panel, "", CYAN, (3, 11, 24))
    title_bar = pygame.Rect(13, 68, W - 26, 21)
    pygame.draw.rect(surf, (5, 23, 41), title_bar)
    pygame.draw.line(surf, (24, 93, 128), (title_bar.left, title_bar.bottom), (title_bar.right, title_bar.bottom), 1)
    draw_text(surf, "SECURE_CONSOLE // PATCH", 22, 73, CYAN, "s")
    status_text = f"XP {engine.xp} // STREAK x{engine.streak}"
    status_x = title_bar.right - 8 - engine.fonts["s"].size(status_text)[0]
    draw_text(surf, status_text, status_x, 73, DIM, "s")

    context_panel = pygame.Rect(18, 92, 184, 42)
    draw_panel(surf, context_panel, "mainframe.py // CODE", CYAN, (2, 9, 20))
    if debug:
        context_lines = [ex["broken_code"]]
    else:
        context_lines = {
            1: ["security = 10", "codename = 'cipher'"],
            2: ["attempts = 0", "if attempts > 3:"],
            3: ["ports = [80, 443]", "ports.append(8080)"],
            4: ["def secure_system():", "    return True"],
        }[engine.current_level]
    for index, line in enumerate(context_lines[:2]):
        draw_text(surf, line, 24, 110 + index * 12, RED if debug else GREEN, "s")
    draw_comms_box(surf)

    log_panel = pygame.Rect(22, 138, W - 44, 127)
    pygame.draw.rect(surf, (1, 7, 17), log_panel)
    pygame.draw.rect(surf, (19, 76, 105), log_panel, 1)
    if mode == "ORDER":
        goal = ex["order_goal"]
        draw_text(surf, goal, 29, 143, YELLOW, "s")
        for index, line in enumerate(engine.order_items):
            marker = ">" if index == engine.order_cursor else " "
            color = YELLOW if index == engine.order_cursor else WHITE
            draw_text(surf, f"{marker} {index + 1}. {line}", 30, 161 + index * 19, color, "s")
    elif mode == "SPEED":
        for index, line in enumerate(wrap_text(ex["question"], "s", W - 64)[:3]):
            draw_text(surf, line, 30, 148 + index * 15, WHITE, "s")
        time_left = max(0, engine.speed_timer_frames) / 60
        timer_bar = pygame.Rect(30, 218, W - 60, 8)
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
            draw_text(surf, f"{marker} {index + 1}. {option}", 30, 148 + index * 26, color, "s")
    else:
        for index, line in enumerate(engine.console_log[-7:]):
            visible_text = line["text"][:line["visible"]]
            draw_text(surf, visible_text, 30, 143 + index * 15, line["color"], "s")

    if engine.attempts >= HINT_AFTER and engine.feedback_timer <= 0:
        hint = "HINT // " + ex["hint"]
        for index, line in enumerate(wrap_text(hint, "s", W - 64)[:2]):
            draw_text(surf, line, 30, 268 + index * 12, YELLOW, "s")
    if engine.feedback_timer > 0:
        draw_text(surf, engine.msg, 30, 276, engine.msg_color, "s")

    console = pygame.Rect(22, 293, W - 44, 31)
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
        draw_text(surf, "SELECTION READY", 31, 302, GREEN, "s")

    controls = {
        "WRITE": "[Enter] Submit   [F1] Lesson   [Hint]",
        "DEBUG": "[Enter] Submit   [F1] Lesson   [Hint]",
        "SPEED": "[Enter] Submit   [F1] Lesson   [Hint]",
        "CHOOSE": "[Up/Down] Select   [Enter] Submit   [F1] Lesson",
        "ORDER": "[Up/Down] Pick line   [Left/Right] Move   [Enter] Submit",
    }[mode]
    draw_text(surf, controls, 12, 328, WHITE, "s")
    if engine.lesson_open:
        draw_lesson_overlay(surf)
    if engine.settings_open:
        draw_settings_overlay(surf)
    if engine.flash > 0 and engine.flash_color == GREEN and not engine.reduce_effects:
        pygame.draw.rect(surf, GREEN, terminal_panel, 2)


def draw_boss_apply(surf, exercise):
    exercise_count = len(exercise["correct_script"])
    line_number = min(engine.boss_line_index + 1, exercise_count)
    pygame.draw.rect(surf, (18, 3, 12), pygame.Rect(0, 0, W, 27))
    pygame.draw.line(surf, RED, (0, 26), (W, 26), 1)
    draw_text(surf, f"BOSS FIGHT // LEVEL {engine.current_level}", 8, 4, RED, "m")
    right_status = (
        f"LINE {line_number}/{exercise_count}"
        if engine.play_mode == "TRAINING"
        else f"TAKEOVER {engine.takeover_percent}%"
    )
    status_x = 405 - engine.fonts["s"].size(right_status)[0]
    draw_text(surf, right_status, status_x, 7, YELLOW, "s")

    lesson_panel = pygame.Rect(8, 30, W - 16, 72)
    draw_panel(surf, lesson_panel, "MISSION // OBJECTIVE", RED, (4, 10, 23))
    for index, line in enumerate(wrap_text(exercise["lesson"], "s", W - 40)[:4]):
        draw_text(surf, line, 17, 51 + index * 12, WHITE, "s")

    evidence_panel = pygame.Rect(8, 108, 156, 210)
    draw_panel(surf, evidence_panel, "", YELLOW, (3, 11, 24))
    draw_text(surf, "EVIDENCE // SCRAMBLED", 15, 112, YELLOW, "s")
    if engine.solution_revealed:
        draw_text(surf, "SOLUTION", 15, 128, GREEN, "s")
        y = 145
        for line in exercise["correct_script"]:
            for wrapped_line in wrap_text(line, "s", 122):
                draw_text(surf, wrapped_line, 15, y, GREEN, "s")
                y += 12
    else:
        y = 130
        for block_index, block in enumerate(exercise["scrambled_blocks"], 1):
            lines = wrap_text(block, "s", 122)
            draw_text(surf, f"{block_index}.", 15, y, YELLOW, "s")
            for line_index, line in enumerate(lines):
                draw_text(surf, line, 34, y + line_index * 12, WHITE, "s")
            y += max(16, len(lines) * 12 + 4)

    terminal_panel = pygame.Rect(170, 108, 272, 210)
    draw_panel(surf, terminal_panel, "mainframe.py // LIVE SCRIPT", CYAN, (1, 7, 17))
    for index, line in enumerate(engine.boss_typed_lines):
        draw_text(surf, line, 181, 132 + index * 22, GREEN, "s")

    input_panel = pygame.Rect(178, 266, 256, 29)
    pygame.draw.rect(surf, (3, 16, 27), input_panel)
    pygame.draw.rect(surf, CYAN, input_panel, 1)
    draw_text(surf, ">>>", 185, 274, CYAN, "s")
    input_x, input_y = 210, 274
    draw_text(surf, engine.boss_player_input, input_x, input_y, WHITE, "s")
    if (pygame.time.get_ticks() // 500) % 2 == 0:
        cursor_x = input_x + engine.fonts["s"].size(engine.boss_player_input)[0]
        pygame.draw.rect(surf, CYAN, pygame.Rect(cursor_x, input_y + 1, 6, 11))

    if engine.feedback_timer > 0:
        draw_text(surf, engine.msg, 181, 301, engine.msg_color, "s")
    elif engine.boss_line_index < exercise_count:
        draw_text(surf, "TYPE THIS LINE, THEN PRESS ENTER", 181, 301, DIM, "s")

    draw_settings_icon(surf)
    draw_button(
        surf,
        pygame.Rect(BOSS_HELPER_BUTTON_RECT),
        "HINT",
        YELLOW,
        engine.hovered_button == "boss_helper",
    )
    draw_button(
        surf,
        pygame.Rect(BOSS_LIBRARY_BUTTON_RECT),
        "LIBRARY",
        CYAN,
        engine.hovered_button == "boss_library",
    )
    draw_text(surf, "[Type line]  [Enter] Submit  [F1] Lesson", 158, 329, WHITE, "s")
    if engine.lesson_open:
        draw_lesson_overlay(surf)
    if engine.settings_open:
        draw_settings_overlay(surf)
    if engine.flash > 0 and engine.flash_color == GREEN and not engine.reduce_effects:
        pygame.draw.rect(surf, GREEN, terminal_panel, 2)


def draw_settings_icon(surf):
    rect = pygame.Rect(MISSION_SETTINGS_BUTTON_RECT)
    pygame.draw.rect(surf, (5, 23, 41), rect)
    pygame.draw.rect(surf, CYAN if engine.settings_open else DIM, rect, 1)
    center = rect.center
    pygame.draw.circle(surf, CYAN if engine.settings_open else WHITE, center, 5, 1)
    pygame.draw.circle(surf, CYAN if engine.settings_open else WHITE, center, 1)
    for angle in range(0, 360, 90):
        direction = pygame.Vector2(1, 0).rotate(angle)
        start = (round(center[0] + direction.x * 6), round(center[1] + direction.y * 6))
        end = (round(center[0] + direction.x * 8), round(center[1] + direction.y * 8))
        pygame.draw.line(surf, CYAN if engine.settings_open else WHITE, start, end, 1)


def draw_settings_overlay(surf):
    shade = pygame.Surface((W, H), pygame.SRCALPHA)
    shade.fill((0, 3, 12, 205))
    surf.blit(shade, (0, 0))
    panel = pygame.Rect(86, 108, 278, 132)
    draw_panel(surf, panel, "SETTINGS // F3 OR ESC TO CLOSE", CYAN)
    draw_text(surf, "M // MUTE AUDIO", 108, 145, WHITE, "s")
    draw_text(surf, f"R // REDUCED EFFECTS: {'ON' if engine.reduce_effects else 'OFF'}", 108, 165, WHITE, "s")
    volume = round(engine.sound_manager.volume * 100) if engine.sound_manager else 0
    draw_text(surf, f"+ / - // VOLUME {volume}%", 108, 185, WHITE, "s")
    draw_text(surf, "Press M, R, +, or - here", 108, 214, YELLOW, "s")


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
    if ex["mode"] == "ORDER":
        draw_text(surf, "SECURITY ORDER VERIFIED", 65, 209, GREEN, "s")
    elif ex["mode"] == "BOSS":
        draw_text(surf, "FILL-IN PATCH VERIFIED", 65, 209, GREEN, "s")
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
    draw_panel(surf, pygame.Rect(24, 42, 402, 264), "MISSION FAILED", RED, (24, 5, 16))
    draw_text_center(surf, "Rogue AI takeover reached 100%.", 128, WHITE, "s")
    draw_button(
        surf,
        pygame.Rect(LOSS_RETRY_BUTTON_RECT),
        "RETRY THIS LEVEL",
        RED,
        engine.hovered_button == "loss_retry",
    )
    draw_button(
        surf,
        pygame.Rect(LOSS_ROADMAP_BUTTON_RECT),
        "BACK TO ROADMAP",
        CYAN,
        engine.hovered_button == "loss_roadmap",
    )
    draw_text_center(surf, "1 RETRY  //  2 ROADMAP", 307, DIM, "s")


def draw_progress_notifications(surf):
    if engine.milestone_banner_timer > 0 and engine.milestone_banner:
        width = 218
        banner_y = {
            "APPLY": 137,
            "WIN": 158,
            "LEVEL_COMPLETE": 158,
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
    if engine.state == "STORY":
        draw_story(canvas)
    elif engine.state == "MODE_SELECT":
        draw_mode_select(canvas)
    elif engine.state == "CONCEPT_LIBRARY":
        draw_concept_library(canvas)
    elif engine.state == "CONCEPT_TRY":
        draw_concept_practice(canvas)
    elif engine.state == "ROADMAP":
        draw_roadmap(canvas)
    elif engine.state == "LEVEL_COMPLETE":
        draw_level_complete(canvas)
    elif engine.state == "MENU":
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

    if engine.state in ("APPLY", "WIN", "LEVEL_COMPLETE", "GAMEOVER_WIN"):
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
    shake = 0 if engine.reduce_effects else int(engine.shake)
    offset_x = random.randint(-shake, shake) if shake > 0 else 0
    offset_y = random.randint(-shake, shake) if shake > 0 else 0
    left, top, width, height = get_viewport(screen.get_size())
    scaled = pygame.transform.scale(canvas, (width, height))
    screen.fill((0, 0, 0))
    scale = min(screen.get_width() / W, screen.get_height() / H)
    screen.blit(
        scaled,
        (round(left + offset_x * scale), round(top + offset_y * scale)),
    )
    pygame.display.flip()
