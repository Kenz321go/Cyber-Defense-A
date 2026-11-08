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
    draw_mission_header,
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
    for center_x, shortcut in (
        (25 + 400 // 6, "F1: MISSION"),
        (225, "F2: LIBRARY"),
        (25 + 400 * 5 // 6, "F3: SETTINGS"),
    ):
        image = engine.fonts["s"].render(shortcut, False, DIM)
        surf.blit(image, (center_x - image.get_width() // 2, 311))
    if engine.save_error:
        draw_text_center(surf, "SAVE ERROR // CHECK DISK ACCESS", 334, RED, "s")
    if engine.settings_open:
        draw_settings_overlay(surf)


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
    cursor_x = 84 + engine.fonts["m"].size(
        engine.concept_typed[:engine.concept_cursor_pos]
    )[0]
    pygame.draw.line(surf, CYAN, (cursor_x, 197), (cursor_x, 214), 1)
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

        def draw_card_text(text, y, color, size="s"):
            image = engine.fonts[size].render(text, False, color)
            surf.blit(image, (card.centerx - image.get_width() // 2, y))

        title_lines = wrap_text(level["title"], "s", 80)[:3]
        for line_index, line in enumerate(title_lines):
            draw_card_text(line, 103 + line_index * 13, WHITE if is_unlocked else DIM)

        dot_centers = [card.left + offset for offset in (10, 28, 46, 64, 86)]
        pygame.draw.line(surf, (25, 55, 75), (dot_centers[0], 167), (dot_centers[-1], 167), 1)
        exercise_ids = sorted_ids(level)
        next_exercise = (
            exercise_ids[-1]
            if engine.master_replay
            else next(
                (
                    exercise_id for exercise_id in exercise_ids
                    if (level_id, exercise_id) not in engine.completed_exercises
                ),
                exercise_ids[0],
            )
        )
        for exercise_index, exercise_id in enumerate(exercise_ids):
            done = level_done or (level_id, exercise_id) in engine.completed_exercises
            current = is_selected and exercise_id == next_exercise
            hovered = engine.hovered_button == f"task_{level_id}_{exercise_id}"
            color = (
                YELLOW if current and engine.master_replay
                else GREEN if done
                else YELLOW if current or hovered
                else CYAN if is_unlocked
                else DIM
            )
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
        draw_card_text("4 TASKS + BOSS", 230, DIM, "xs")

    draw_button(
        surf,
        pygame.Rect(ROADMAP_BUTTON_RECT),
        (
            f"START MASTER BOSS {engine.roadmap_selection}"
            if engine.master_replay
            else f"START LEVEL {engine.roadmap_selection}"
        ),
        CYAN,
        engine.hovered_button == "roadmap",
    )
    roadmap_help = engine.roadmap_notice or (
        "ARROWS: LEVEL // CLICK OR 1-5: TASK // 5 = BOSS"
        if not engine.master_replay
        else "MASTER // ARROWS/CLICK: SELECT LEVEL // ENTER: BOSS"
    )
    help_color = YELLOW if engine.roadmap_notice else DIM
    draw_text_center(surf, roadmap_help, 278, help_color, "s")
    if engine.save_error:
        draw_text(surf, "SAVE ERROR", 12, 335, RED, "s")


def draw_level_complete(surf):
    completion_title = (
        f"MASTER BOSS {engine.current_level} // CLEARED"
        if engine.master_replay
        else f"LEVEL {engine.current_level} // COMPLETE"
    )
    draw_header(surf, completion_title, GREEN)
    draw_panel(
        surf,
        pygame.Rect(28, 43, 394, 248),
        "MASTER CHALLENGE CLEARED" if engine.master_replay else "SECURITY LAYER RESTORED",
        GREEN,
    )
    draw_shield(surf, 207, 63)
    draw_text_center(surf, "LEVEL COMPLETE!", 125, GREEN, "l")
    draw_text_center(surf, f"SCORE {engine.score}  //  XP {engine.xp}", 159, WHITE, "m")
    level_ids = sorted_ids(game_data[engine.current_preset])
    if engine.master_replay:
        unlock_text = "MASTER CLEARED // SELECT ANY LEVEL"
    elif engine.current_level < level_ids[-1]:
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


def mission_progress_percent():
    total = sum(
        len(sorted_ids(game_data[engine.current_preset][level_id]))
        for level_id in sorted_ids(game_data[engine.current_preset])
    )
    completed = sum(
        (level_id, exercise_id) in engine.completed_exercises
        for level_id in sorted_ids(game_data[engine.current_preset])
        for exercise_id in sorted_ids(game_data[engine.current_preset][level_id])
    )
    return round(completed * 100 / total) if total else 0


def draw_apply(surf):
    exercise = get_exercise()
    mode = exercise["mode"]
    if mode == "BOSS":
        draw_boss_apply(surf, exercise)
        return

    panel = pygame.Rect(12, 66, W - 24, 258)
    draw_mission_header(
        surf,
        exercise,
        mission_progress_percent(),
        engine.rogue_ai_takeover,
    )
    draw_panel(surf, panel, f"MISSION // {mode}", CYAN, (3, 11, 24))
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

    content_y = 91
    for line in wrap_text(exercise["objective"], "s", W - 48):
        draw_text(surf, line, 24, content_y, WHITE, "s")
        content_y += 13
    content_y += 8

    if mode == "CHOOSE":
        for index, option in enumerate(exercise["options"]):
            marker = ">" if index == engine.choice_index else " "
            color = CYAN if index == engine.choice_index else WHITE
            draw_text(
                surf,
                f"{marker} {index + 1}. {option}",
                30,
                content_y + index * 23,
                color,
                "s",
            )
    elif mode == "ORDER":
        for index, line in enumerate(engine.order_items):
            marker = ">" if index == engine.order_cursor else " "
            color = CYAN if index == engine.order_cursor else WHITE
            draw_text(
                surf,
                f"{marker} {index + 1}. {line}",
                30,
                content_y + index * 19,
                color,
                "s",
            )
    elif mode == "DEBUG":
        draw_text(surf, "CURRENT LINE //", 24, content_y, YELLOW, "s")
        draw_text(surf, exercise["broken_code"], 30, content_y + 17, RED, "s")
    elif mode == "SPEED":
        question_y = content_y
        question_lines = wrap_text(exercise["question"], "s", W - 48)
        for index, line in enumerate(question_lines):
            draw_text(surf, line, 24, question_y + index * 13, WHITE, "s")
        timer_y = question_y + 46
        if exercise.get("broken_code"):
            code_y = question_y + len(question_lines) * 13 + 5
            draw_text(surf, "CODE //", 24, code_y, YELLOW, "s")
            code_panel = pygame.Rect(24, code_y + 15, W - 48, 22)
            pygame.draw.rect(surf, (1, 7, 17), code_panel)
            pygame.draw.rect(surf, (19, 76, 105), code_panel, 1)
            draw_text(surf, exercise["broken_code"], 30, code_y + 19, RED, "s")
            timer_y = code_panel.bottom + 5
        time_left = max(0, engine.speed_timer_frames) / 60
        timer_bar = pygame.Rect(24, timer_y, W - 48, 8)
        pygame.draw.rect(surf, (46, 13, 24), timer_bar)
        pygame.draw.rect(
            surf,
            RED if time_left <= 5 else CYAN,
            pygame.Rect(
                timer_bar.x,
                timer_bar.y,
                round(timer_bar.width * time_left / 40),
                timer_bar.height,
            ),
        )
        pygame.draw.rect(surf, (19, 76, 105), timer_bar, 1)

    status_y = 264
    if engine.feedback_timer > 0 or engine.hint_message_persistent:
        status_lines = wrap_text(engine.msg, "s", W - 48)[:2]
        start_y = status_y - (len(status_lines) - 1) * 12
        for index, line in enumerate(status_lines):
            draw_text(surf, line, 24, start_y + index * 12, engine.msg_color, "s")
    elif engine.attempts >= HINT_AFTER:
        hint = "HINT // " + exercise["hint"]
        for index, line in enumerate(wrap_text(hint, "s", W - 48)[:2]):
            draw_text(surf, line, 24, status_y + index * 12, YELLOW, "s")

    if engine.solution_revealed:
        solution_y = max(content_y + 8, 210)
        for line in engine.console_log[-6:]:
            visible_text = line["text"][:line["visible"]]
            if visible_text and solution_y < 258:
                draw_text(surf, visible_text, 24, solution_y, line["color"], "s")
                solution_y += 12

    if mode in ("WRITE", "DEBUG", "SPEED"):
        input_panel = pygame.Rect(22, 284, W - 44, 32)
        pygame.draw.rect(surf, (1, 7, 17), input_panel)
        pygame.draw.rect(surf, (22, 91, 124), input_panel, 1)
        before_cursor = ">>> " + engine.typed[:engine.cursor_pos]
        after_cursor = engine.typed[engine.cursor_pos:]
        input_font = engine.fonts["m"]
        input_x, input_y = 31, 293
        before_image = input_font.render(before_cursor, False, GREEN)
        surf.blit(before_image, (input_x, input_y))
        cursor_x = input_x + before_image.get_width()
        cursor_visible = (pygame.time.get_ticks() // 500) % 2 == 0
        if cursor_visible:
            pygame.draw.rect(surf, GREEN, pygame.Rect(cursor_x, input_y + 1, 7, 13))
        after_image = input_font.render(after_cursor, False, GREEN)
        surf.blit(after_image, (cursor_x + (8 if cursor_visible else 0), input_y))

    pygame.draw.rect(surf, (2, 8, 19), pygame.Rect(0, 326, W, 24))
    controls = {
        "CHOOSE": "UP/DOWN: SELECT // ENTER: CONFIRM",
        "ORDER": "UP/DOWN: SELECT // LEFT/RIGHT: MOVE // ENTER: CONFIRM",
        "WRITE": "TYPE ANSWER // ENTER: CONFIRM // F1: LESSON",
        "DEBUG": "TYPE ANSWER // ENTER: CONFIRM // F1: LESSON",
        "SPEED": "TYPE ANSWER // ENTER: CONFIRM // F1: LESSON",
    }[mode]
    draw_text_center(surf, controls, 331, WHITE, "s")
    if engine.lesson_open:
        draw_lesson_overlay(surf)
    if engine.settings_open:
        draw_settings_overlay(surf)
    if engine.flash > 0 and engine.flash_color == GREEN and not engine.reduce_effects:
        pygame.draw.rect(surf, GREEN, panel, 2)


def wrap_code_line(text, size, max_width):
    lines = []
    line = ""
    for character in text:
        candidate = line + character
        if line and engine.fonts[size].size(candidate)[0] > max_width:
            lines.append(line)
            line = character
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines or [""]


def draw_boss_apply(surf, exercise):
    exercise_count = len(exercise["correct_script"])
    draw_mission_header(
        surf,
        exercise,
        mission_progress_percent(),
        engine.rogue_ai_takeover,
    )
    lesson_panel = pygame.Rect(8, 66, W - 16, 65)
    draw_panel(
        surf,
        lesson_panel,
        f"MISSION // {exercise['mode']}",
        CYAN,
        (4, 10, 23),
    )
    for index, line in enumerate(wrap_text(exercise["objective"], "s", W - 40)[:3]):
        draw_text(surf, line, 17, 87 + index * 12, WHITE, "s")

    evidence_panel = pygame.Rect(8, 137, 156, 181)
    draw_panel(surf, evidence_panel, "", YELLOW, (3, 11, 24))
    evidence_lines = (
        exercise["correct_script"]
        if engine.solution_revealed
        else exercise["scrambled_blocks"]
    )
    evidence_color = GREEN if engine.solution_revealed else WHITE
    evidence_font = "xxs" if engine.solution_revealed else "s"
    evidence_line_height = 12 if engine.solution_revealed else 14
    evidence_title = "EVIDENCE // SOLUTION" if engine.solution_revealed else "EVIDENCE // SCRAMBLED"
    draw_text(surf, evidence_title, 15, 141, YELLOW, "xs")
    line_y = 158
    code_x = 34
    code_width = evidence_panel.right - 8 - code_x
    for line_index, code_line in enumerate(evidence_lines):
        wrapped_lines = wrap_code_line(code_line, evidence_font, code_width)
        draw_text(surf, f"{line_index + 1}.", 14, line_y, YELLOW, "s")
        for wrapped_index, wrapped_line in enumerate(wrapped_lines):
            draw_text(
                surf,
                wrapped_line,
                code_x,
                line_y + wrapped_index * evidence_line_height,
                evidence_color,
                evidence_font,
            )
        line_y += max(1, len(wrapped_lines)) * evidence_line_height + 2

    terminal_panel = pygame.Rect(170, 137, 272, 181)
    draw_panel(surf, terminal_panel, "mainframe.py // LIVE SCRIPT", CYAN, (1, 7, 17))
    for index, line in enumerate(engine.boss_typed_lines):
        draw_text(surf, line, 181, 161 + index * 22, GREEN, "s")

    input_panel = pygame.Rect(178, 266, 256, 29)
    pygame.draw.rect(surf, (3, 16, 27), input_panel)
    pygame.draw.rect(surf, CYAN, input_panel, 1)
    draw_text(surf, ">>>", 185, 274, CYAN, "s")
    input_x, input_y = 210, 274
    draw_text(surf, engine.boss_player_input, input_x, input_y, WHITE, "s")
    if (pygame.time.get_ticks() // 500) % 2 == 0:
        cursor_prefix = engine.boss_player_input[:engine.cursor_pos]
        cursor_x = input_x + engine.fonts["s"].size(cursor_prefix)[0]
        pygame.draw.rect(surf, CYAN, pygame.Rect(cursor_x, input_y + 1, 6, 11))

    if engine.feedback_timer > 0 or engine.hint_message_persistent:
        status_lines = wrap_text(engine.msg, "s", W - 48)[:2]
        start_y = 313 - (len(status_lines) - 1) * 12
        for index, line in enumerate(status_lines):
            draw_text(surf, line, 24, start_y + index * 12, engine.msg_color, "s")
    elif engine.boss_line_index < exercise_count:
        draw_text(surf, "TYPE THIS LINE, THEN PRESS ENTER", 181, 301, DIM, "s")

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
    draw_text_center(
        surf,
        "LEFT/RIGHT: CURSOR // BACKSPACE: DELETE // ENTER: SEND",
        329,
        WHITE,
        "s",
    )
    if engine.lesson_open:
        draw_lesson_overlay(surf)
    if engine.settings_open:
        draw_settings_overlay(surf)
    if engine.flash > 0 and engine.flash_color == GREEN and not engine.reduce_effects:
        pygame.draw.rect(surf, GREEN, terminal_panel, 2)


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
    title = (
        "MASTER MODE // ALL BOSSES DEFEATED"
        if engine.master_replay
        else "GLOBAL NETWORK // CAMPAIGN COMPLETE"
    )
    draw_panel(surf, pygame.Rect(24, 42, 402, 264), title)
    if engine.unlock_animation_timer > 0:
        draw_unlock_lock(surf, 383, 56)
    celebration = "MASTER COMPLETE" if engine.master_replay else "SYSTEM SECURED"
    title_image = title_font.render(celebration, False, GREEN)
    surf.blit(title_image, ((W - title_image.get_width()) // 2, 95))
    message = (
        "Level 4 boss defeated! All Master challenges cleared."
        if engine.master_replay
        else "Level 4 boss defeated! All four levels are secured."
    )
    draw_text_center(surf, message, 150, WHITE, "s")
    draw_text_center(surf, f"FINAL SCORE {engine.score}  //  XP {engine.xp}", 179, CYAN, "s")

    draw_button(
        surf,
        pygame.Rect(VICTORY_BUTTON_RECT),
        "RETURN TO MASTER SELECT" if engine.master_replay else "RETURN TO HOME SCREEN",
        GREEN,
    )


def draw_compromised(surf):
    draw_panel(surf, pygame.Rect(24, 42, 402, 264), "MISSION FAILED", RED, (24, 5, 16))
    for index, line in enumerate(
        wrap_text(
            "Takeover reached 100%. Mission lost. Retry this level or return to the roadmap.",
            "s",
            350,
        )[:2]
    ):
        draw_text_center(surf, line, 123 + index * 14, WHITE, "s")
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

    if engine.state in ("WIN", "LEVEL_COMPLETE", "GAMEOVER_WIN"):
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
