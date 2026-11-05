"""Game state, progression rules, and input handling."""

import ast
import pygame
import random
import sys

from dialogue import choose_line
from missions import game_data
from settings import (
    CYAN,
    COMPROMISED_BUTTON_RECT,
    GREEN,
    H,
    MAX_INPUT,
    MENU_BUTTON_RECT,
    PINK,
    RED,
    SCALE,
    VICTORY_BUTTON_RECT,
    W,
    WHITE,
    YELLOW,
)

# ======================================================================
# ENGINE STATE (module-level globals, no classes)
# ======================================================================
current_preset = 1      # key into game_data
current_level = 1       # key into game_data[current_preset]
current_exercise = 1    # key into game_data[current_preset][current_level]
attempts = 0            # wrong answers on the current exercise

state = "MENU"          # MENU -> INTRO -> APPLY -> WIN -> GAMEOVER_WIN
typed = ""              # what the player has typed
cursor_pos = 0          # cursor index inside `typed`
msg = ""                # feedback message
msg_color = WHITE

shake = 0.0             # screen-shake intensity
flash = 0               # frames of border flash left
flash_color = RED
particles = []          # win confetti
floating_texts = []
transition_timer = 0
glitch_timer = 0
glitch_lines = []
menu_button_hover = False
lesson_open = False
seen_concepts = set()
console_log = []
console_queue = []
answer_pending = False
pending_state = None
pending_state_timer = 0
dialogue_queue = []
active_dialogue = None
takeover_percent = 0
completed_exercises = set()
milestones_seen = set()
milestone_banner = ""
milestone_banner_timer = 0
milestone_queue = []
streak = 0
xp = 0
combo_popup_timer = 0
combo_popup_text = ""

fonts = {}              # filled in by init_fonts()
type_sound = None       # optional typing click
sound_manager = None
reduce_effects = False
choice_index = 0
order_items = []
order_cursor = 0
speed_timer_frames = 0
progress_display = 0.0
unlock_animation_timer = 0


# ======================================================================
# DATA HELPERS
# ======================================================================
def sorted_ids(d):
    """Integer keys of a dict, in order (skips text keys like "title")."""
    return sorted(k for k in d if isinstance(k, int))


def get_level():
    return game_data[current_preset][current_level]


def get_exercise():
    return get_level()[current_exercise]


def normalize(code):
    """Forgiving compare: trim, collapse spaces, treat " and ' the same."""
    return " ".join(code.replace('"', "'").split())


def insert_text(text):
    """Insert printable single-line text at the active input cursor."""
    global typed, cursor_pos
    text = text.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    text = "".join(character for character in text if character.isprintable())
    available = MAX_INPUT - len(typed)
    if available <= 0 or not text:
        return
    text = text[:available]
    typed = typed[:cursor_pos] + text + typed[cursor_pos:]
    cursor_pos += len(text)


def is_last_exercise_of_level():
    return current_exercise == sorted_ids(get_level())[-1]


def is_last_level_of_preset():
    return current_level == sorted_ids(game_data[current_preset])[-1]


def is_last_preset():
    return current_preset == sorted_ids(game_data)[-1]


def set_state(new_state):
    global state, transition_timer
    if state != new_state:
        state = new_state
        transition_timer = 30


# ======================================================================
# GAME LOGIC
# ======================================================================
def start_apply():
    global typed, cursor_pos, msg, attempts, lesson_open, console_log, console_queue
    global answer_pending, pending_state, pending_state_timer
    global choice_index, order_items, order_cursor, speed_timer_frames
    set_state("APPLY")
    typed = ""
    cursor_pos = 0
    msg = ""
    attempts = 0
    concept = (current_preset, current_level)
    lesson_open = concept not in seen_concepts
    seen_concepts.add(concept)
    console_log = [
        {
            "text": "> awaiting patch input",
            "color": CYAN,
            "visible": len("> awaiting patch input"),
            "ticks": 0,
        }
    ]
    console_queue = []
    answer_pending = False
    pending_state = None
    pending_state_timer = 0
    choice_index = 0
    order_cursor = 0
    mode = get_exercise()["mode"]
    if mode == "ORDER":
        order_items = random.sample(get_exercise()["order_lines"], len(get_exercise()["order_lines"]))
    elif mode == "BOSS":
        order_items = random.sample(get_exercise()["boss_order"], len(get_exercise()["boss_order"]))
    else:
        order_items = []
    speed_timer_frames = 20 * 60 if mode == "SPEED" else 0
    trigger_dialogue("mission_start")


def reset_campaign_progress():
    global completed_exercises, milestones_seen, milestone_banner, milestone_banner_timer
    global milestone_queue
    completed_exercises = set()
    milestones_seen = set()
    milestone_banner = ""
    milestone_banner_timer = 0
    milestone_queue = []


def reset_current_level_progress():
    global completed_exercises, milestone_banner, milestone_banner_timer, milestone_queue
    completed_exercises.difference_update(
        (current_level, exercise_id) for exercise_id in sorted_ids(get_level())
    )
    milestone_banner = ""
    milestone_banner_timer = 0
    milestone_queue = []


def restart_current_level():
    global current_exercise, takeover_percent, streak, combo_popup_timer
    global combo_popup_text, dialogue_queue, active_dialogue, particles, floating_texts
    global answer_pending
    current_exercise = sorted_ids(get_level())[0]
    takeover_percent = 0
    streak = 0
    combo_popup_timer = 0
    combo_popup_text = ""
    reset_current_level_progress()
    dialogue_queue = []
    active_dialogue = None
    particles = []
    floating_texts = []
    answer_pending = False
    start_apply()


def trigger_dialogue(event):
    global active_dialogue
    speaker, text = choose_line(event)
    color = CYAN if speaker == "HANDLER" else RED
    dialogue_queue.append({
        "speaker": speaker,
        "text": text,
        "color": color,
    })
    if active_dialogue is None:
        active_dialogue = dialogue_queue.pop(0)
        active_dialogue.update({"visible": 0, "ticks": 0, "hold": 40})


def append_console_line(text, color, animated=False):
    line = {
        "text": text,
        "color": color,
        "visible": 0 if animated else len(text),
        "ticks": 0,
    }
    console_log.append(line)
    if animated:
        console_queue.append(line)
    if len(console_log) > 40:
        del console_log[:-40]


def submit_answer(timed_out=False):
    global attempts, shake, flash, flash_color, msg, msg_color, glitch_timer, glitch_lines
    global answer_pending, pending_state, pending_state_timer
    global milestones_seen, milestone_banner, milestone_banner_timer, milestone_queue
    global streak, xp, combo_popup_timer, combo_popup_text, takeover_percent
    global speed_timer_frames, shake, reduce_effects, unlock_animation_timer
    mode = get_exercise()["mode"]
    if sound_manager:
        sound_manager.play("submit")
    if mode == "CHOOSE":
        answer_correct = choice_index == get_exercise()["answer_index"]
    elif mode == "ORDER":
        answer_correct = order_items == get_exercise()["expected_order"]
    elif mode == "BOSS":
        answer_correct = order_items == get_exercise()["boss_order"]
    else:
        answer_correct = not timed_out and normalize(typed) == normalize(get_exercise()["expected"])
    speed_timer_frames = 0
    append_console_line(">>> " + typed, GREEN)
    if mode in ("CHOOSE", "ORDER", "BOSS"):
        submitted = order_items if mode in ("ORDER", "BOSS") else get_exercise()["options"][choice_index]
        append_console_line(f">>> {submitted}", GREEN)
    if answer_correct:
        takeover_percent = max(0, takeover_percent - 15)
        completed_exercises.add((current_level, current_exercise))
        streak += 1
        reward = 100 + max(0, streak - 1) * 25
        xp += reward
        if streak >= 3:
            combo_popup_text = f"COMBO x{streak}"
            combo_popup_timer = 90
            if sound_manager:
                sound_manager.play("combo")
        total_exercises = sum(
            len(sorted_ids(game_data[current_preset][level_id]))
            for level_id in sorted_ids(game_data[current_preset])
        )
        progress_percent = round(len(completed_exercises) * 100 / total_exercises)
        for milestone in (25, 50, 75, 100):
            if progress_percent >= milestone and milestone not in milestones_seen:
                milestones_seen.add(milestone)
                milestone_queue.append(f"PROGRESS MILESTONE // {milestone}%")
        if milestone_banner_timer <= 0 and milestone_queue:
            milestone_banner = milestone_queue.pop(0)
            milestone_banner_timer = 150
        trigger_dialogue("correct")
        if is_last_exercise_of_level():
            trigger_dialogue("level_complete")
            if is_last_level_of_preset() and is_last_preset():
                trigger_dialogue("final_mission")
        for line in get_exercise()["output"]:
            append_console_line(line, GREEN, animated=True)
        pending_state = (
            "GAMEOVER_WIN"
            if is_last_exercise_of_level() and is_last_level_of_preset()
            else "WIN"
        )
        answer_pending = True
        pending_state_timer = 30
        flash, flash_color = 12, GREEN
        if not reduce_effects:
            spawn_confetti()
        if sound_manager:
            sound_manager.play("success")
            if is_last_exercise_of_level():
                sound_manager.play("level_complete")
        if is_last_exercise_of_level():
            unlock_animation_timer = 120
        floating_texts.append({
            "text": f"+{reward} XP",
            "x": W // 2,
            "y": H // 2,
            "timer": 60,
        })
    else:
        takeover_percent = min(100, takeover_percent + 10)
        streak = 0
        if timed_out:
            error_text = "TIMEOUT: response window expired"
        elif mode == "CHOOSE":
            error_text = "ChoiceError: incorrect option selected"
        elif mode in ("ORDER", "BOSS"):
            error_text = "OrderError: security steps are out of sequence"
        else:
            try:
                ast.parse(typed)
            except SyntaxError as error:
                error_text = f"SyntaxError: {error.msg}"
            else:
                error_text = "PatchError: command does not match expected patch"
        append_console_line(error_text, RED, animated=True)
        if sound_manager:
            sound_manager.play("error")
        attempts += 1
        if attempts == 1:
            trigger_dialogue("first_wrong")
        elif attempts == 3:
            trigger_dialogue("third_wrong")
        shake = 0.0 if reduce_effects else 3.0
        flash, flash_color = 10, RED
        msg = "ACCESS DENIED - check your syntax!"
        msg_color = RED
        glitch_lines = [
            {"y": random.randint(0, H - 1), "thickness": random.randint(1, 3)}
            for _ in range(3)
        ]
        glitch_timer = 0 if reduce_effects else 5
        if sound_manager:
            sound_manager.update_alarm(takeover_percent)
        if takeover_percent >= 100:
            answer_pending = False
            set_state("GAMEOVER_LOSS")


def advance():
    """Move to the next exercise, level, or preset (all driven by game_data)."""
    global current_preset, current_level, current_exercise, particles
    global active_dialogue, dialogue_queue

    particles = []
    if not is_last_exercise_of_level():
        current_exercise += 1
        if get_exercise()["mode"] == "BOSS":
            active_dialogue = None
            dialogue_queue = []
            set_state("BOSS_INTRO")
            trigger_dialogue("boss_intro")
            if sound_manager:
                sound_manager.play("boss_intro")
        else:
            start_apply()
        return

    # Level finished
    current_exercise = 1
    previous_preset = current_preset
    if not is_last_level_of_preset():
        current_level += 1
    else:
        # Preset finished -> next preset if it exists, else loop to the first
        current_level = 1
        if is_last_preset():
            current_preset = sorted_ids(game_data)[0]
        else:
            current_preset += 1
    if current_preset != previous_preset:
        reset_campaign_progress()
    set_state("INTRO")


def spawn_confetti():
    colors = [CYAN, PINK, GREEN, YELLOW]
    for _ in range(50):
        particles.append({
            "x": random.randint(0, W),
            "y": random.randint(-60, 0),
            "vy": random.uniform(1.0, 3.0),
            "color": random.choice(colors),
        })


def update_effects():
    global shake, flash, particles, answer_pending, pending_state, pending_state_timer
    global active_dialogue
    global milestone_banner, milestone_banner_timer, milestone_queue, combo_popup_timer
    global progress_display, unlock_animation_timer, speed_timer_frames
    shake = shake * 0.85 if shake > 0.4 else 0.0
    if flash > 0:
        flash -= 1
    for p in particles:
        p["y"] += p["vy"]
    particles = [p for p in particles if p["y"] < H]
    target_progress = len(completed_exercises) * 100 / sum(
        len(sorted_ids(game_data[current_preset][level_id]))
        for level_id in sorted_ids(game_data[current_preset])
    )
    progress_display += (target_progress - progress_display) * 0.12
    if abs(target_progress - progress_display) < 0.1:
        progress_display = target_progress
    if state in ("WIN", "GAMEOVER_WIN") and unlock_animation_timer > 0:
        unlock_animation_timer -= 1
    if sound_manager:
        sound_manager.update_alarm(takeover_percent)
    if state == "APPLY" and get_exercise()["mode"] == "SPEED" and speed_timer_frames > 0:
        speed_timer_frames -= 1
        if speed_timer_frames == 0:
            submit_answer(timed_out=True)
    if console_queue:
        line = console_queue[0]
        line["ticks"] += 1
        if line["ticks"] >= 2:
            line["ticks"] = 0
            line["visible"] += 1
            if line["visible"] >= len(line["text"]):
                console_queue.pop(0)
    if active_dialogue is not None:
        if active_dialogue["visible"] < len(active_dialogue["text"]):
            active_dialogue["ticks"] += 1
            if active_dialogue["ticks"] >= 2:
                active_dialogue["ticks"] = 0
                active_dialogue["visible"] += 1
        else:
            active_dialogue["hold"] -= 1
            if active_dialogue["hold"] <= 0:
                active_dialogue = dialogue_queue.pop(0) if dialogue_queue else None
                if active_dialogue is not None:
                    active_dialogue.update({"visible": 0, "ticks": 0, "hold": 40})
    if not answer_pending:
        if milestone_banner_timer > 0:
            milestone_banner_timer -= 1
        if combo_popup_timer > 0:
            combo_popup_timer -= 1
        if milestone_banner_timer <= 0 and milestone_queue:
            milestone_banner = milestone_queue.pop(0)
            milestone_banner_timer = 150
    if answer_pending and not console_queue and active_dialogue is None:
        if pending_state_timer > 0:
            pending_state_timer -= 1
        else:
            set_state(pending_state)
            if pending_state == "WIN" and is_last_exercise_of_level():
                unlock_animation_timer = 120
            answer_pending = False
            pending_state = None


def handle_key(event):
    global typed, cursor_pos, lesson_open, choice_index, order_cursor, order_items, reduce_effects
    global shake, flash, glitch_timer
    modifiers = getattr(event, "mod", 0)
    control_pressed = bool(modifiers & pygame.KMOD_CTRL)
    if event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()

    if event.key == pygame.K_m and (state != "APPLY" or control_pressed):
        if sound_manager:
            sound_manager.toggle_mute()
        return
    if event.key == pygame.K_r and (state != "APPLY" or control_pressed):
        reduce_effects = not reduce_effects
        if reduce_effects:
            shake = 0.0
            flash = 0
            glitch_timer = 0
        return
    if event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS) and (
        state != "APPLY" or control_pressed
    ):
        if sound_manager:
            sound_manager.adjust_volume(0.1)
        return
    if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS) and (
        state != "APPLY" or control_pressed
    ):
        if sound_manager:
            sound_manager.adjust_volume(-0.1)
        return
    if state == "BOSS_INTRO" and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        start_apply()
        return

    if state == "APPLY" and event.key == pygame.K_F1:
        lesson_open = not lesson_open
        return
    if state == "APPLY" and answer_pending:
        return
    if state == "APPLY" and lesson_open:
        return

    is_enter = event.key in (pygame.K_RETURN, pygame.K_KP_ENTER)

    if state == "INTRO":
        if is_enter:
            start_apply()

    elif state == "APPLY":
        mode = get_exercise()["mode"]
        if mode in ("WRITE", "DEBUG", "SPEED") and control_pressed:
            if event.key == pygame.K_v:
                try:
                    clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                except pygame.error as error:
                    append_console_line(f"> clipboard paste failed: {error}", RED)
                    return
                if clipboard_text:
                    if isinstance(clipboard_text, bytes):
                        clipboard_text = clipboard_text.decode("utf-8", errors="replace")
                    insert_text(clipboard_text.split("\0", 1)[0])
                    if sound_manager:
                        sound_manager.play("key")
                else:
                    append_console_line("> clipboard is empty or unavailable", RED)
                return
            if event.key == pygame.K_c:
                try:
                    pygame.scrap.put(pygame.SCRAP_TEXT, typed.encode("utf-8"))
                except pygame.error as error:
                    append_console_line(f"> clipboard copy failed: {error}", RED)
                return
        if mode == "CHOOSE" and event.key in (pygame.K_UP, pygame.K_DOWN):
            choice_index = (choice_index + (1 if event.key == pygame.K_DOWN else -1)) % len(get_exercise()["options"])
            if sound_manager:
                sound_manager.play("key")
        elif mode in ("ORDER", "BOSS") and event.key in (pygame.K_UP, pygame.K_DOWN):
            order_cursor = (order_cursor + (1 if event.key == pygame.K_DOWN else -1)) % len(order_items)
            if sound_manager:
                sound_manager.play("key")
        elif mode in ("ORDER", "BOSS") and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            offset = -1 if event.key == pygame.K_LEFT else 1
            swap_index = order_cursor + offset
            if 0 <= swap_index < len(order_items):
                order_items[order_cursor], order_items[swap_index] = order_items[swap_index], order_items[order_cursor]
                order_cursor = swap_index
                if sound_manager:
                    sound_manager.play("key")
        elif is_enter:
            submit_answer()
        elif event.key == pygame.K_BACKSPACE:
            if cursor_pos > 0:
                typed = typed[:cursor_pos - 1] + typed[cursor_pos:]
                cursor_pos -= 1
                if sound_manager:
                    sound_manager.play("key")
                elif type_sound:
                    type_sound.play()
        elif event.key == pygame.K_LEFT:
            cursor_pos = max(0, cursor_pos - 1)
            if sound_manager:
                sound_manager.play("key")
        elif event.key == pygame.K_RIGHT:
            cursor_pos = min(len(typed), cursor_pos + 1)
            if sound_manager:
                sound_manager.play("key")
        elif event.unicode != "" and event.unicode.isprintable():
            insert_text(event.unicode)
            if sound_manager:
                sound_manager.play("key")
            elif type_sound:
                type_sound.play()

    elif state == "WIN":
        if is_enter:
            advance()
    elif state == "GAMEOVER_LOSS":
        if is_enter:
            restart_current_level()


def handle_event(event):
    global current_preset, current_level, current_exercise, menu_button_hover
    global takeover_percent, streak, xp
    if event.type == pygame.MOUSEMOTION:
        button = pygame.Rect(MENU_BUTTON_RECT)
        position = (event.pos[0] // SCALE, event.pos[1] // SCALE)
        hovering = state == "MENU" and button.collidepoint(position)
        if hovering and not menu_button_hover and type_sound:
            if sound_manager:
                sound_manager.play("menu_hover")
            else:
                channel = type_sound.play()
                if channel:
                    channel.set_volume(0.15)
        menu_button_hover = hovering
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        position = (event.pos[0] // SCALE, event.pos[1] // SCALE)
        if state == "MENU" and pygame.Rect(MENU_BUTTON_RECT).collidepoint(position):
            if sound_manager:
                sound_manager.play("menu_click")
            set_state("INTRO")
        elif state == "GAMEOVER_WIN" and pygame.Rect(VICTORY_BUTTON_RECT).collidepoint(position):
            current_preset = 1
            current_level = 1
            current_exercise = 1
            takeover_percent = 0
            streak = 0
            xp = 0
            reset_campaign_progress()
            set_state("MENU")
            menu_button_hover = False
        elif state == "GAMEOVER_LOSS" and pygame.Rect(COMPROMISED_BUTTON_RECT).collidepoint(position):
            restart_current_level()
    elif event.type == pygame.KEYDOWN:
        handle_key(event)
