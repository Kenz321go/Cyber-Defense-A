"""Game state, progression rules, and input handling."""

import ast
import json
import pygame
import random
from pathlib import Path
from textwrap import wrap

from dialogue import choose_line, helper_line, task_feedback, task_tip
from missions import concept_library, game_data
from settings import (
    CYAN,
    BOSS_HELPER_BUTTON_RECT,
    BOSS_LIBRARY_BUTTON_RECT,
    CONCEPT_BACK_BUTTON_RECT,
    CONCEPT_LIST_RECT,
    CONCEPT_TRY_BUTTON_RECT,
    FPS,
    GREEN,
    H,
    LOSS_RETRY_BUTTON_RECT,
    LOSS_ROADMAP_BUTTON_RECT,
    HELPER_BUTTON_RECT,
    LIBRARY_BUTTON_RECT,
    LEVEL_COMPLETE_BUTTON_RECT,
    MAX_INPUT,
    MISSION_BUTTON_RECT,
    MISSION_LIBRARY_BUTTON_RECT,
    MISSION_SETTINGS_BUTTON_RECT,
    MENU_BUTTON_RECT,
    MASTER_BUTTON_RECT,
    PINK,
    RED,
    RESUME_BUTTON_RECT,
    ROADMAP_BUTTON_RECT,
    SCALE,
    screen_to_canvas,
    TRAINING_BUTTON_RECT,
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

state = "STORY"
typed = ""              # what the player has typed
cursor_pos = 0          # cursor index inside `typed`
msg = ""                # feedback message
msg_color = WHITE
feedback_timer = 0

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
last_comms_message = ""
takeover_tooltip_seen = False
takeover_tooltip_timer = 0
settings_open = False
takeover_percent = 0
completed_exercises = set()
played_levels = set()
campaign_progress_loaded = False
roadmap_selection = 1
roadmap_notice = ""
milestones_seen = set()
milestone_banner = ""
milestone_banner_timer = 0
milestone_queue = []
streak = 0
xp = 0
combo_popup_timer = 0
combo_popup_text = ""
library_return_state = "MODE_SELECT"
selected_concept = 0
concept_typed = ""
concept_feedback = ""
helper_stage = 0
solution_revealed = False
play_mode = "MISSION"
score = 0
completed_levels = set()
story_index = 0
story_timer = 2 * FPS
mode_selection = 0
master_replay = False
hovered_button = ""
save_error = ""
SAVE_PATH = Path(__file__).with_name("savegame.json")
STORY_LINES = (
    "AGENT CIPHER // LAST DEFENDER.",
    "A ROGUE AI IS TAKING THE NETWORK.",
    "LEARN PYTHON. PATCH EACH SECURITY LAYER.",
    "RESTORE FOUR SYSTEMS TO STOP THE BREACH.",
)

fonts = {}              # filled in by init_fonts()
type_sound = None       # optional typing click
sound_manager = None
reduce_effects = False
choice_index = 0
order_items = []
order_cursor = 0
boss_line_index = 0
boss_player_input = ""
boss_typed_lines = []
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
    global boss_line_index, boss_player_input, boss_typed_lines
    global helper_stage, solution_revealed, takeover_tooltip_seen, takeover_tooltip_timer
    global settings_open, feedback_timer
    set_state("APPLY")
    typed = ""
    cursor_pos = 0
    msg = ""
    attempts = 0
    feedback_timer = 0
    concept = (current_preset, current_level)
    lesson_open = concept not in seen_concepts
    helper_stage = 0
    solution_revealed = False
    settings_open = False
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
    boss_line_index = 0
    boss_player_input = ""
    boss_typed_lines = []
    mode = get_exercise()["mode"]
    if mode == "ORDER":
        order_items = random.sample(get_exercise()["order_lines"], len(get_exercise()["order_lines"]))
    else:
        order_items = []
    speed_timer_frames = 20 * FPS if mode == "SPEED" and play_mode == "MISSION" else 0
    tip = get_exercise().get("order_goal", get_exercise()["hint"]) if mode == "ORDER" else get_exercise()["hint"]
    speaker, text = task_tip(tip)
    set_comms_message(speaker, text)
    if play_mode == "MISSION" and not takeover_tooltip_seen:
        takeover_tooltip_seen = True
        takeover_tooltip_timer = 8 * FPS
    save_game()


def begin_game(mode):
    global current_preset, current_level, current_exercise, play_mode, mode_selection, master_replay
    global takeover_percent, streak, score, xp
    global roadmap_selection
    load_campaign_progress()
    current_preset = sorted_ids(game_data)[0]
    current_level = campaign_frontier()
    current_exercise = sorted_ids(get_level())[0]
    roadmap_selection = current_level
    play_mode = mode
    master_replay = False
    takeover_percent = 0
    streak = 0
    score = 0
    xp = 0
    mode_selection = 0
    set_state("ROADMAP")


def load_campaign_progress():
    """Restore shared curriculum progress when starting Training or Mission."""
    global current_preset, completed_exercises, completed_levels, played_levels, save_error
    global campaign_progress_loaded
    if not has_saved_game():
        reset_campaign_progress()
        save_error = ""
        campaign_progress_loaded = True
        return
    try:
        data = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("version") != 1:
            raise ValueError("unsupported save format")
        preset = data.get("preset")
        if type(preset) is not int or preset not in game_data:
            raise ValueError("save progress is invalid")
        saved_exercises = data.get("completed_exercises", [])
        saved_levels = data.get("completed_levels", [])
        saved_played = data.get("played_levels", [])
        if not all(isinstance(items, list) for items in (saved_exercises, saved_levels, saved_played)):
            raise ValueError("save progress is invalid")
        exercises = set()
        for item in saved_exercises:
            if (
                not isinstance(item, list)
                or len(item) != 2
                or type(item[0]) is not int
                or type(item[1]) is not int
                or item[0] not in game_data[preset]
                or item[1] not in game_data[preset][item[0]]
            ):
                raise ValueError("save progress is invalid")
            exercises.add(tuple(item))
        levels = set()
        for level_id in saved_levels:
            if type(level_id) is not int or level_id not in game_data[preset]:
                raise ValueError("save progress is invalid")
            levels.add(level_id)
        played = set()
        for level_id in saved_played:
            if type(level_id) is not int or level_id not in game_data[preset]:
                raise ValueError("save progress is invalid")
            played.add(level_id)
        saved_level = data.get("level")
        if type(saved_level) is int and saved_level in game_data[preset]:
            played.add(saved_level)
        current_preset = preset
        completed_exercises = exercises
        completed_levels = levels
        played_levels = played | levels
    except (OSError, ValueError, TypeError) as error:
        reset_campaign_progress()
        save_error = f"SAVE ERROR // {error}"
        campaign_progress_loaded = True
        return
    save_error = ""
    campaign_progress_loaded = True


def campaign_frontier():
    level_ids = sorted_ids(game_data[current_preset])
    return next(
        (level_id for level_id in level_ids if level_id not in completed_levels),
        level_ids[-1],
    )


def all_levels_completed():
    if not campaign_progress_loaded:
        load_campaign_progress()
    level_ids = sorted_ids(game_data[current_preset])
    return bool(level_ids) and set(level_ids).issubset(completed_levels)


def mode_select_actions():
    actions = ["training", "mission"]
    if has_saved_game():
        actions.append("resume")
    actions.append("library")
    if all_levels_completed():
        actions.append("master")
    return actions


def start_master_mode():
    global play_mode, roadmap_selection, master_replay
    load_campaign_progress()
    if not all_levels_completed():
        return
    play_mode = "MISSION"
    master_replay = True
    if roadmap_selection not in completed_levels:
        roadmap_selection = min(completed_levels)
    set_state("ROADMAP")


def start_master_level():
    global play_mode
    if not all_levels_completed() or roadmap_selection not in completed_levels:
        return
    play_mode = "MISSION"
    start_selected_level()


def is_level_unlocked(level_id):
    level_ids = sorted_ids(game_data[current_preset])
    if level_id not in level_ids:
        return False
    level_index = level_ids.index(level_id)
    return (
        level_index == 0
        or level_id in played_levels
        or level_id in completed_levels
        or level_ids[level_index - 1] in completed_levels
    )


def unlocked_levels():
    return [level_id for level_id in sorted_ids(game_data[current_preset]) if is_level_unlocked(level_id)]


def open_concept_library(return_state=None):
    global library_return_state, selected_concept
    library_return_state = state if return_state is None else return_state
    selected_concept = min(selected_concept, len(concept_library) - 1)
    set_state("CONCEPT_LIBRARY")


def close_concept_library():
    set_state(library_return_state)


def start_concept_practice():
    global concept_typed, concept_feedback
    concept_typed = ""
    concept_feedback = ""
    set_state("CONCEPT_TRY")


def submit_concept_practice():
    global concept_feedback
    concept = concept_library[tuple(concept_library)[selected_concept]]
    if normalize(concept_typed) == normalize(concept["answer"]):
        concept_feedback = "Correct! " + concept["why"]
    else:
        concept_feedback = "Not quite. Check the example and try again."


def show_agent_hint():
    global helper_stage, active_dialogue, dialogue_queue, solution_revealed
    if helper_stage >= 3:
        return
    exercise = get_exercise()
    if helper_stage < 2:
        speaker, text = helper_line(current_level, current_exercise, helper_stage + 1)
        helper_stage += 1
        set_comms_message(speaker, text)
        return

    if exercise["mode"] == "BOSS":
        answer_lines = exercise["correct_script"]
        solution_revealed = True
    else:
        answer_lines = exercise.get("expected_order", [exercise["expected"]])
    append_console_line("AGENT ANSWER //", CYAN)
    for line in answer_lines:
        for answer_line in wrap(line, width=58):
            append_console_line(answer_line, GREEN)
    explanation = exercise["lesson"].strip()
    for explanation_line in wrap("WHY // " + explanation, width=58):
        append_console_line(explanation_line, CYAN)
    set_comms_message(
        "HANDLER",
        "Full script is shown in Evidence." if exercise["mode"] == "BOSS"
        else "Answer and why are in the console.",
    )
    helper_stage = 3


def has_saved_game():
    return SAVE_PATH.is_file()


def save_game(resume_state="APPLY", level=None, exercise=None):
    global save_error
    task_index = current_exercise if exercise is None else exercise
    data = {
        "version": 1,
        "preset": current_preset,
        "level": current_level if level is None else level,
        "task_index": task_index,
        "exercise": task_index,
        "mode": play_mode,
        "score": score,
        "xp": xp,
        "completed_exercises": sorted([list(item) for item in completed_exercises]),
        "completed_levels": sorted(completed_levels),
        "played_levels": sorted(played_levels),
        "resume_state": resume_state,
    }
    try:
        SAVE_PATH.write_text(json.dumps(data), encoding="utf-8")
    except OSError as error:
        save_error = f"SAVE ERROR // {error}"
        if state == "APPLY" and console_log:
            append_console_line("SAVE ERROR // PROGRESS NOT SAVED", RED)
        return
    save_error = ""


def resume_saved_game():
    global current_preset, current_level, current_exercise, play_mode
    global score, xp, completed_exercises, completed_levels, played_levels, roadmap_selection, save_error
    global campaign_progress_loaded
    try:
        data = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("version") != 1:
            raise ValueError("unsupported save format")
        preset = data["preset"]
        level = data["level"]
        exercise = data.get("task_index", data.get("exercise"))
        mode = data["mode"]
        if (
            type(preset) is not int
            or type(level) is not int
            or type(exercise) is not int
            or preset not in game_data
            or level not in game_data[preset]
            or exercise not in game_data[preset][level]
            or mode not in ("TRAINING", "MISSION")
        ):
            raise ValueError("save progress is invalid")
        saved_exercises = data["completed_exercises"]
        saved_levels = data["completed_levels"]
        saved_played = data.get("played_levels", [])
        if not isinstance(saved_exercises, list) or not isinstance(saved_levels, list) or not isinstance(saved_played, list):
            raise ValueError("save progress is invalid")
        exercises = set()
        for item in saved_exercises:
            if (
                not isinstance(item, list)
                or len(item) != 2
                or type(item[0]) is not int
                or type(item[1]) is not int
                or item[0] not in game_data[preset]
                or item[1] not in game_data[preset][item[0]]
            ):
                raise ValueError("save progress is invalid")
            exercises.add(tuple(item))
        if any(type(level_id) is not int or level_id not in game_data[preset] for level_id in saved_levels):
            raise ValueError("save progress is invalid")
        if any(type(level_id) is not int or level_id not in game_data[preset] for level_id in saved_played):
            raise ValueError("save progress is invalid")
        saved_score = data["score"]
        saved_xp = data["xp"]
        if type(saved_score) is not int or saved_score < 0 or type(saved_xp) is not int or saved_xp < 0:
            raise ValueError("save score is invalid")
        resume_state = data.get("resume_state", "APPLY")
        if resume_state not in ("APPLY", "ROADMAP"):
            raise ValueError("save progress is invalid")
        current_preset = preset
        current_level = level
        current_exercise = exercise
        play_mode = mode
        score = saved_score
        xp = saved_xp
        completed_exercises = exercises
        completed_levels = set(saved_levels)
        played_levels = set(saved_played) | completed_levels | {level}
        roadmap_selection = level
        campaign_progress_loaded = True
    except (OSError, ValueError, TypeError, KeyError) as error:
        save_error = f"SAVE ERROR // {error}"
        return
    save_error = ""
    if resume_state == "ROADMAP":
        set_state("ROADMAP")
    else:
        start_apply()


def start_selected_level():
    global current_level, current_exercise, roadmap_selection, master_replay, roadmap_notice
    if not is_level_unlocked(roadmap_selection):
        roadmap_notice = "Complete the previous level first."
        return
    current_level = roadmap_selection
    current_exercise = next(
        (
            exercise_id for exercise_id in sorted_ids(get_level())
            if (current_level, exercise_id) not in completed_exercises
        ),
        sorted_ids(get_level())[0],
    )
    played_levels.add(current_level)
    roadmap_notice = ""
    start_apply()
    master_replay = False


def start_selected_exercise(exercise_id):
    global current_level, current_exercise, roadmap_selection, master_replay, roadmap_notice
    if not is_level_unlocked(roadmap_selection):
        roadmap_notice = "Complete the previous level first."
        return False
    exercise_ids = sorted_ids(game_data[current_preset][roadmap_selection])
    if exercise_id not in exercise_ids:
        return False
    exercise_index = exercise_ids.index(exercise_id)
    if any(
        (roadmap_selection, previous_id) not in completed_exercises
        for previous_id in exercise_ids[:exercise_index]
    ):
        roadmap_notice = "Complete previous task first."
        return False
    current_level = roadmap_selection
    current_exercise = exercise_id
    played_levels.add(current_level)
    roadmap_notice = ""
    master_replay = False
    start_apply()
    return True


def continue_to_roadmap():
    global current_level, current_exercise, roadmap_selection
    current_level = campaign_frontier()
    roadmap_selection = current_level
    current_exercise = sorted_ids(get_level())[0]
    save_game("ROADMAP")
    set_state("ROADMAP")


def reset_campaign_progress():
    global completed_exercises, completed_levels, played_levels, roadmap_selection
    global roadmap_notice
    global campaign_progress_loaded
    global milestones_seen, milestone_banner, milestone_banner_timer
    global milestone_queue
    completed_exercises = set()
    completed_levels = set()
    played_levels = set()
    roadmap_selection = sorted_ids(game_data[current_preset])[0]
    roadmap_notice = ""
    campaign_progress_loaded = True
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


def return_to_roadmap():
    global current_exercise, takeover_percent, answer_pending, active_dialogue, dialogue_queue
    current_exercise = next(
        (
            exercise_id for exercise_id in sorted_ids(get_level())
            if (current_level, exercise_id) not in completed_exercises
        ),
        sorted_ids(get_level())[0],
    )
    takeover_percent = 0
    answer_pending = False
    active_dialogue = None
    dialogue_queue = []
    if sound_manager:
        sound_manager.update_alarm(0)
    save_game("ROADMAP")
    set_state("ROADMAP")


def set_comms_message(speaker, text, hold=FPS * 10):
    global active_dialogue, dialogue_queue, last_comms_message
    last_comms_message = text
    dialogue_queue = []
    active_dialogue = {
        "speaker": speaker,
        "text": text,
        "color": CYAN if speaker == "HANDLER" else RED,
        "visible": 0,
        "ticks": 0,
        "hold": hold,
    }


def reveal_mission_solution():
    global solution_revealed
    if solution_revealed:
        return
    exercise = get_exercise()
    console_log.clear()
    console_queue.clear()
    if exercise["mode"] == "CHOOSE":
        answer_lines = [exercise["expected"]]
    elif exercise["mode"] == "ORDER":
        answer_lines = exercise["expected_order"]
    elif exercise["mode"] == "BOSS":
        answer_lines = exercise["correct_script"]
    else:
        answer_lines = [exercise["expected"]]

    explanation = exercise["lesson"].split(". ", 1)[0].strip().rstrip(".")
    append_console_line("ANSWER //", YELLOW, animated=True)
    for answer in answer_lines:
        for line in wrap(answer, width=52):
            append_console_line(line, GREEN, animated=True)
    for line in wrap("WHY // " + explanation, width=52):
        append_console_line(line, CYAN, animated=True)
    solution_revealed = True


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


def append_console_line(text, color, animated=False, delay=2):
    line = {
        "text": text,
        "color": color,
        "visible": 0 if animated else len(text),
        "ticks": 0,
        "delay": delay,
    }
    console_log.append(line)
    if animated:
        console_queue.append(line)
    if len(console_log) > 40:
        del console_log[:-40]


def submit_boss_line():
    global boss_line_index, boss_player_input, boss_typed_lines, attempts, takeover_percent
    global streak, shake, flash, flash_color, msg, msg_color, feedback_timer
    global glitch_lines, glitch_timer, solution_revealed
    exercise = get_exercise()
    expected = exercise["correct_script"][boss_line_index]
    correct = boss_player_input.strip() == expected.strip()
    if sound_manager and not (correct and boss_line_index == len(exercise["correct_script"]) - 1):
        sound_manager.play("submit")
    if correct:
        boss_typed_lines.append(expected)
        boss_line_index += 1
        boss_player_input = ""
        flash, flash_color = 8, GREEN
        msg = f"LINE {boss_line_index}/{len(exercise['correct_script'])} // ACCEPTED"
        msg_color = GREEN
        feedback_timer = FPS // 2
        set_comms_message("HANDLER", "Line accepted. Keep going.", hold=FPS // 2)
        if sound_manager and boss_line_index < len(exercise["correct_script"]):
            sound_manager.play("success")
        if boss_line_index == len(exercise["correct_script"]):
            submit_answer()
        return

    if play_mode == "MISSION":
        takeover_percent = min(100, takeover_percent + 10)
    streak = 0
    attempts += 1
    error_text = f"SyntaxError: expected line {boss_line_index + 1}"
    if not solution_revealed:
        append_console_line(error_text, RED, animated=True)
    if sound_manager:
        sound_manager.play("error")
    speaker, feedback = task_feedback(False, attempts)
    set_comms_message(speaker, feedback)
    if play_mode == "MISSION" and attempts == 2:
        reveal_mission_solution()
    shake = 0.0 if reduce_effects else 3.0
    msg = error_text
    msg_color = RED
    feedback_timer = FPS
    flash, flash_color = 10, msg_color
    glitch_lines = [] if reduce_effects else [
        {"y": random.randint(0, H - 1), "thickness": random.randint(1, 3)}
        for _ in range(3)
    ]
    glitch_timer = 0 if reduce_effects else 5
    boss_player_input = ""
    if sound_manager and play_mode == "MISSION":
        sound_manager.update_alarm(takeover_percent)
    if play_mode == "MISSION" and takeover_percent >= 100:
        set_state("GAMEOVER_LOSS")


def submit_answer(timed_out=False):
    global attempts, shake, flash, flash_color, msg, msg_color, glitch_timer, glitch_lines
    global answer_pending, pending_state, pending_state_timer
    global milestones_seen, milestone_banner, milestone_banner_timer, milestone_queue
    global streak, score, xp, completed_levels, combo_popup_timer, combo_popup_text, takeover_percent
    global speed_timer_frames, shake, reduce_effects, unlock_animation_timer, solution_revealed
    global feedback_timer
    mode = get_exercise()["mode"]
    if mode == "BOSS" and boss_line_index < len(get_exercise()["correct_script"]):
        submit_boss_line()
        return
    if sound_manager:
        sound_manager.play("submit")
    if mode == "CHOOSE":
        answer_correct = choice_index == get_exercise()["answer_index"]
    elif mode == "ORDER":
        answer_correct = order_items == get_exercise()["expected_order"]
    elif mode == "BOSS":
        answer_correct = boss_line_index == len(get_exercise()["correct_script"])
    else:
        answer_correct = not timed_out and normalize(typed) == normalize(get_exercise()["expected"])
    speed_timer_frames = 0
    if not solution_revealed and mode != "BOSS":
        append_console_line(">>> " + typed, GREEN)
    if mode in ("CHOOSE", "ORDER") and not solution_revealed:
        submitted = order_items if mode == "ORDER" else get_exercise()["options"][choice_index]
        append_console_line(f">>> {submitted}", GREEN)
    if answer_correct:
        takeover_percent = max(0, takeover_percent - 15)
        completed_exercises.add((current_level, current_exercise))
        streak += 1
        reward = 100 + max(0, streak - 1) * 25
        score += reward
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
        speaker, feedback = task_feedback(True)
        set_comms_message(speaker, feedback, hold=FPS // 2)
        if is_last_exercise_of_level():
            if is_last_level_of_preset() and is_last_preset():
                set_comms_message(
                    "HANDLER",
                    "Mainframe secure. Great work, agent.",
                    hold=FPS // 2,
                )
        for line in get_exercise()["output"]:
            append_console_line(line, GREEN, animated=True, delay=1)
        pending_state = "LEVEL_COMPLETE" if is_last_exercise_of_level() else "WIN"
        if is_last_exercise_of_level():
            completed_levels.add(current_level)
            next_level = min(current_level + 1, sorted_ids(game_data[current_preset])[-1])
            save_game("ROADMAP", next_level, sorted_ids(game_data[current_preset][next_level])[0])
        else:
            exercise_ids = sorted_ids(get_level())
            next_exercise = exercise_ids[exercise_ids.index(current_exercise) + 1]
            save_game("APPLY", current_level, next_exercise)
        answer_pending = True
        pending_state_timer = 30
        msg = f"CORRECT // {get_exercise()['why']}"
        msg_color = GREEN
        feedback_timer = FPS
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
        if play_mode == "MISSION":
            takeover_percent = min(100, takeover_percent + 10)
        streak = 0
        if play_mode == "TRAINING":
            error_text = "Try again. Check the example or press HINT."
        elif timed_out:
            error_text = "TIMEOUT: response window expired"
        elif mode == "CHOOSE":
            error_text = "ChoiceError: incorrect option selected"
        elif mode == "ORDER":
            error_text = "OrderError: security steps are out of sequence"
        else:
            try:
                ast.parse(typed)
            except SyntaxError as error:
                error_text = f"SyntaxError: {error.msg}"
            else:
                error_text = "PatchError: command does not match expected patch"
        if not solution_revealed:
            append_console_line(error_text, CYAN if play_mode == "TRAINING" else RED, animated=True)
        if sound_manager:
            sound_manager.play("error")
        attempts += 1
        speaker, feedback = task_feedback(False, attempts)
        set_comms_message(speaker, feedback)
        if play_mode == "MISSION" and attempts == 2:
            reveal_mission_solution()
        shake = 0.0 if reduce_effects or play_mode == "TRAINING" else 3.0
        msg = f"WRONG // {get_exercise()['why']}"
        msg_color = CYAN if play_mode == "TRAINING" else RED
        feedback_timer = FPS
        flash, flash_color = 10, msg_color
        glitch_lines = [] if play_mode == "TRAINING" else [
            {"y": random.randint(0, H - 1), "thickness": random.randint(1, 3)}
            for _ in range(3)
        ]
        glitch_timer = 0 if reduce_effects or play_mode == "TRAINING" else 5
        if sound_manager and play_mode == "MISSION":
            sound_manager.update_alarm(takeover_percent)
        if play_mode == "MISSION" and takeover_percent >= 100:
            answer_pending = False
            set_state("GAMEOVER_LOSS")


def advance():
    """Move to the next exercise in the current level."""
    global current_exercise, particles
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
    global story_index, story_timer, takeover_tooltip_timer, feedback_timer
    shake = shake * 0.85 if shake > 0.4 else 0.0
    if flash > 0:
        flash -= 1
    if feedback_timer > 0:
        feedback_timer -= 1
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
    if state in ("WIN", "LEVEL_COMPLETE", "GAMEOVER_WIN") and unlock_animation_timer > 0:
        unlock_animation_timer -= 1
    if state == "STORY":
        story_timer -= 1
        if story_timer <= 0:
            story_index += 1
            if story_index >= len(STORY_LINES):
                set_state("MODE_SELECT")
            else:
                story_timer = 2 * FPS
    if takeover_tooltip_timer > 0:
        takeover_tooltip_timer -= 1
    if sound_manager:
        sound_manager.update_alarm(takeover_percent)
    if state == "APPLY" and get_exercise()["mode"] == "SPEED" and speed_timer_frames > 0:
        speed_timer_frames -= 1
        if speed_timer_frames == 0:
            submit_answer(timed_out=True)
    if console_queue:
        line = console_queue[0]
        line["ticks"] += 1
        if line["ticks"] >= line.get("delay", 2):
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


def handle_escape():
    global settings_open, lesson_open
    if settings_open:
        settings_open = False
    elif state == "APPLY" and lesson_open:
        lesson_open = False
    elif state == "CONCEPT_LIBRARY":
        close_concept_library()
    elif state == "CONCEPT_TRY":
        set_state("CONCEPT_LIBRARY")
    elif state == "LEVEL_COMPLETE":
        continue_to_roadmap()
    elif state in ("APPLY", "GAMEOVER_LOSS"):
        return_to_roadmap()
    elif state in ("INTRO", "BOSS_INTRO", "WIN"):
        set_state("ROADMAP")
    elif state == "GAMEOVER_WIN":
        set_state("MODE_SELECT")
    elif state == "MODE_SELECT":
        set_state("MENU")
    elif state == "MENU":
        set_state("MODE_SELECT")
    elif state in ("STORY", "ROADMAP"):
        set_state("MODE_SELECT")


def handle_key(event):
    global typed, cursor_pos, lesson_open, choice_index, order_cursor, order_items, reduce_effects
    global shake, flash, glitch_timer, mode_selection, selected_concept, concept_typed, concept_feedback
    global settings_open, roadmap_selection, boss_player_input, roadmap_notice
    modifiers = getattr(event, "mod", 0)
    control_pressed = bool(modifiers & pygame.KMOD_CTRL)
    if event.key == pygame.K_ESCAPE:
        handle_escape()
        return

    if state == "APPLY" and event.key == pygame.K_F3:
        settings_open = not settings_open
        return
    if state == "STORY":
        set_state("MODE_SELECT")
        return

    if event.key == pygame.K_m and state not in ("MODE_SELECT", "ROADMAP") and (
        state != "APPLY" or control_pressed or settings_open
    ):
        if sound_manager:
            sound_manager.toggle_mute()
        return
    if event.key == pygame.K_r and (state != "APPLY" or control_pressed or settings_open):
        reduce_effects = not reduce_effects
        if reduce_effects:
            shake = 0.0
            flash = 0
            glitch_timer = 0
        return
    if event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS) and (
        state != "APPLY" or control_pressed or settings_open
    ):
        if sound_manager:
            sound_manager.adjust_volume(0.1)
        return
    if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS) and (
        state != "APPLY" or control_pressed or settings_open
    ):
        if sound_manager:
            sound_manager.adjust_volume(-0.1)
        return
    if settings_open:
        return
    if state == "BOSS_INTRO" and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        start_apply()
        return

    if state == "APPLY" and event.key == pygame.K_F2:
        open_concept_library()
        return
    if state == "APPLY" and event.key == pygame.K_F1:
        lesson_open = not lesson_open
        return
    if state == "APPLY" and answer_pending:
        return
    if state == "APPLY" and lesson_open:
        return

    is_enter = event.key in (pygame.K_RETURN, pygame.K_KP_ENTER)

    if state == "MODE_SELECT":
        if event.key in (pygame.K_4, pygame.K_KP4):
            open_concept_library()
        elif event.key in (pygame.K_1, pygame.K_KP1):
            begin_game("TRAINING")
        elif event.key in (pygame.K_2, pygame.K_KP2):
            begin_game("MISSION")
        elif event.key in (pygame.K_3, pygame.K_KP3) and has_saved_game():
            resume_saved_game()
        elif event.key == pygame.K_m and all_levels_completed():
            start_master_mode()
        elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            actions = mode_select_actions()
            direction = 1 if event.key in (pygame.K_DOWN, pygame.K_RIGHT) else -1
            mode_selection = (mode_selection + direction) % len(actions)
        elif is_enter:
            action = mode_select_actions()[mode_selection]
            if action == "training":
                begin_game("TRAINING")
            elif action == "mission":
                begin_game("MISSION")
            elif action == "resume":
                resume_saved_game()
            elif action == "library":
                open_concept_library()
            elif action == "master":
                start_master_mode()
        return

    if state == "CONCEPT_LIBRARY":
        if event.key in (pygame.K_UP, pygame.K_DOWN):
            selected_concept = (
                selected_concept + (1 if event.key == pygame.K_DOWN else -1)
            ) % len(concept_library)
        elif is_enter or event.key == pygame.K_t:
            start_concept_practice()
        elif event.key in (pygame.K_BACKSPACE, pygame.K_b):
            close_concept_library()
        return

    if state == "CONCEPT_TRY":
        if is_enter:
            submit_concept_practice()
        elif event.key == pygame.K_BACKSPACE:
            concept_typed = concept_typed[:-1]
            concept_feedback = ""
        elif event.unicode and event.unicode.isprintable() and len(concept_typed) < MAX_INPUT:
            concept_typed += event.unicode
            concept_feedback = ""
        return

    if state == "ROADMAP":
        available = unlocked_levels()
        if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            selection_index = available.index(roadmap_selection) if roadmap_selection in available else 0
            roadmap_selection = available[
                (selection_index + (1 if event.key == pygame.K_RIGHT else -1)) % len(available)
            ]
            roadmap_notice = ""
        elif event.key in (
            pygame.K_1, pygame.K_KP1,
            pygame.K_2, pygame.K_KP2,
            pygame.K_3, pygame.K_KP3,
            pygame.K_4, pygame.K_KP4,
            pygame.K_5, pygame.K_KP5,
        ):
            exercise_by_key = {
                pygame.K_1: 1, pygame.K_KP1: 1,
                pygame.K_2: 2, pygame.K_KP2: 2,
                pygame.K_3: 3, pygame.K_KP3: 3,
                pygame.K_4: 4, pygame.K_KP4: 4,
                pygame.K_5: 5, pygame.K_KP5: 5,
            }
            exercise_id = exercise_by_key[event.key]
            start_selected_exercise(exercise_id)
        elif event.key == pygame.K_m and all_levels_completed():
            start_master_level()
        elif is_enter:
            if master_replay:
                start_master_level()
            else:
                start_selected_level()
        return

    if state == "LEVEL_COMPLETE":
        if is_enter:
            continue_to_roadmap()
        return

    if state == "INTRO":
        if is_enter:
            start_apply()

    elif state == "APPLY":
        mode = get_exercise()["mode"]
        if mode in ("WRITE", "DEBUG", "SPEED", "BOSS") and control_pressed:
            if event.key == pygame.K_v:
                try:
                    clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                except pygame.error as error:
                    append_console_line(f"> clipboard paste failed: {error}", RED)
                    return
                if clipboard_text:
                    if isinstance(clipboard_text, bytes):
                        clipboard_text = clipboard_text.decode("utf-8", errors="replace")
                    clipboard_text = clipboard_text.split("\0", 1)[0]
                    if mode == "BOSS":
                        line = clipboard_text.splitlines()[0] if clipboard_text.splitlines() else clipboard_text
                        boss_player_input = line[:MAX_INPUT]
                    else:
                        insert_text(clipboard_text)
                    if sound_manager:
                        sound_manager.play("key")
                else:
                    append_console_line("> clipboard is empty or unavailable", RED)
                return
            if event.key == pygame.K_c:
                try:
                    copied_text = boss_player_input if mode == "BOSS" else typed
                    pygame.scrap.put(pygame.SCRAP_TEXT, copied_text.encode("utf-8"))
                except pygame.error as error:
                    append_console_line(f"> clipboard copy failed: {error}", RED)
                return
        if mode == "BOSS":
            if is_enter:
                submit_boss_line()
            elif event.key == pygame.K_BACKSPACE:
                boss_player_input = boss_player_input[:-1]
                if sound_manager:
                    sound_manager.play("key")
            elif event.unicode and event.unicode.isprintable() and len(boss_player_input) < MAX_INPUT:
                boss_player_input += event.unicode
                if sound_manager:
                    sound_manager.play("key")
                elif type_sound:
                    type_sound.play()
            return
        if mode == "CHOOSE" and event.key in (pygame.K_UP, pygame.K_DOWN):
            choice_index = (choice_index + (1 if event.key == pygame.K_DOWN else -1)) % len(get_exercise()["options"])
            if sound_manager:
                sound_manager.play("key")
        elif mode == "ORDER" and event.key in (pygame.K_UP, pygame.K_DOWN):
            order_cursor = (order_cursor + (1 if event.key == pygame.K_DOWN else -1)) % len(order_items)
            if sound_manager:
                sound_manager.play("key")
        elif mode == "ORDER" and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
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
        if event.key in (pygame.K_1, pygame.K_KP1):
            restart_current_level()
        elif event.key in (pygame.K_2, pygame.K_KP2):
            return_to_roadmap()


def handle_event(event):
    global current_preset, current_level, current_exercise, menu_button_hover
    global takeover_percent, streak, xp
    global hovered_button, selected_concept, settings_open, roadmap_selection, roadmap_notice
    if event.type == pygame.MOUSEMOTION:
        display = pygame.display.get_surface()
        window_size = display.get_size() if display else (W * SCALE, H * SCALE)
        position = screen_to_canvas(event.pos, window_size)
        button_rects = {
            "training": TRAINING_BUTTON_RECT,
            "mission": MISSION_BUTTON_RECT,
            "resume": RESUME_BUTTON_RECT,
            "master": MASTER_BUTTON_RECT,
            "library": LIBRARY_BUTTON_RECT,
            "roadmap": ROADMAP_BUTTON_RECT,
            "level_complete": LEVEL_COMPLETE_BUTTON_RECT,
            "helper": HELPER_BUTTON_RECT,
            "mission_library": MISSION_LIBRARY_BUTTON_RECT,
            "boss_helper": BOSS_HELPER_BUTTON_RECT,
            "boss_library": BOSS_LIBRARY_BUTTON_RECT,
            "concept_try": CONCEPT_TRY_BUTTON_RECT,
            "concept_back": CONCEPT_BACK_BUTTON_RECT,
            "loss_retry": LOSS_RETRY_BUTTON_RECT,
            "loss_roadmap": LOSS_ROADMAP_BUTTON_RECT,
            "settings": MISSION_SETTINGS_BUTTON_RECT,
        }
        concept_row = pygame.Rect(CONCEPT_LIST_RECT)
        concept_row_index = next(
            (
                index for index in range(len(concept_library))
                if pygame.Rect(
                    concept_row.x,
                    concept_row.y + index * 27,
                    concept_row.width,
                    concept_row.height,
                ).collidepoint(position)
            ),
            -1,
        )
        hovered_button = next(
            (
                name for name, rect in button_rects.items()
                if pygame.Rect(rect).collidepoint(position)
                and (
                    (state == "MODE_SELECT" and name in ("training", "mission", "resume", "library") and (name != "resume" or has_saved_game()))
                    or (state == "MODE_SELECT" and name == "master")
                    or (state == "ROADMAP" and name == "roadmap")
                    or (state == "LEVEL_COMPLETE" and name == "level_complete")
                    or (state == "APPLY" and name in ("helper", "mission_library"))
                    or (
                        state == "APPLY"
                        and get_exercise()["mode"] == "BOSS"
                        and name in ("boss_helper", "boss_library")
                    )
                    or (state == "CONCEPT_LIBRARY" and name in ("concept_try", "concept_back"))
                    or (state == "GAMEOVER_LOSS" and name in ("loss_retry", "loss_roadmap"))
                    or (state == "APPLY" and name == "settings")
                )
            ),
            "",
        )
        if state == "CONCEPT_LIBRARY" and concept_row_index in range(len(concept_library)):
            hovered_button = f"concept_{concept_row_index}"
        if state == "ROADMAP":
            level_ids = sorted_ids(game_data[current_preset])
            hovered_task = next(
                (
                    (level_id, exercise_id)
                    for index, level_id in enumerate(level_ids)
                    for task_index, exercise_id in enumerate(
                        sorted_ids(game_data[current_preset][level_id])
                    )
                    if pygame.Rect(
                        14 + index * 106 + (10, 28, 46, 64, 86)[task_index] - 8,
                        157,
                        16,
                        37,
                    ).collidepoint(position)
                ),
                None,
            )
            if hovered_task is not None:
                hovered_button = f"task_{hovered_task[0]}_{hovered_task[1]}"
            hovered_level = next(
                (
                    level_id for index, level_id in enumerate(level_ids)
                    if pygame.Rect(14 + index * 106, 75, 100, 185).collidepoint(position)
                    and is_level_unlocked(level_id)
                ),
                None,
            )
            if hovered_task is None and hovered_level is not None:
                hovered_button = f"level_{hovered_level}"
        hovering = state == "MENU" and pygame.Rect(MENU_BUTTON_RECT).collidepoint(position)
        if hovering and not menu_button_hover and type_sound:
            if sound_manager:
                sound_manager.play("menu_hover")
            else:
                channel = type_sound.play()
                if channel:
                    channel.set_volume(0.15)
        menu_button_hover = hovering
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        display = pygame.display.get_surface()
        window_size = display.get_size() if display else (W * SCALE, H * SCALE)
        position = screen_to_canvas(event.pos, window_size)
        if state == "APPLY" and settings_open:
            settings_open = False
        elif state == "APPLY" and pygame.Rect(MISSION_SETTINGS_BUTTON_RECT).collidepoint(position):
            settings_open = True
        elif state == "MODE_SELECT" and pygame.Rect(LIBRARY_BUTTON_RECT).collidepoint(position):
            open_concept_library()
        elif state == "MODE_SELECT" and pygame.Rect(TRAINING_BUTTON_RECT).collidepoint(position):
            begin_game("TRAINING")
        elif state == "MODE_SELECT" and pygame.Rect(MISSION_BUTTON_RECT).collidepoint(position):
            begin_game("MISSION")
        elif state == "MODE_SELECT" and has_saved_game() and pygame.Rect(RESUME_BUTTON_RECT).collidepoint(position):
            resume_saved_game()
        elif state == "MODE_SELECT" and pygame.Rect(MASTER_BUTTON_RECT).collidepoint(position):
            start_master_mode()
        elif state == "ROADMAP":
            level_ids = sorted_ids(game_data[current_preset])
            task_clicked = False
            for index, level_id in enumerate(level_ids):
                card_left = 14 + index * 106
                exercise_ids = sorted_ids(game_data[current_preset][level_id])
                centers = [card_left + offset for offset in (10, 28, 46, 64, 86)]
                for task_index, exercise_id in enumerate(exercise_ids):
                    target = pygame.Rect(centers[task_index] - 8, 157, 16, 37)
                    if target.collidepoint(position):
                        roadmap_selection = level_id
                        start_selected_exercise(exercise_id)
                        task_clicked = True
                        break
                if task_clicked:
                    break
            if task_clicked:
                pass
            elif pygame.Rect(ROADMAP_BUTTON_RECT).collidepoint(position):
                start_selected_level()
            else:
                for index, level_id in enumerate(level_ids):
                    card = pygame.Rect(14 + index * 106, 75, 100, 185)
                    if card.collidepoint(position) and is_level_unlocked(level_id):
                        roadmap_selection = level_id
                        roadmap_notice = ""
                        break
        elif state == "LEVEL_COMPLETE" and pygame.Rect(LEVEL_COMPLETE_BUTTON_RECT).collidepoint(position):
            continue_to_roadmap()
        elif (
            state == "APPLY"
            and get_exercise()["mode"] == "BOSS"
            and pygame.Rect(BOSS_HELPER_BUTTON_RECT).collidepoint(position)
        ):
            show_agent_hint()
        elif (
            state == "APPLY"
            and get_exercise()["mode"] == "BOSS"
            and pygame.Rect(BOSS_LIBRARY_BUTTON_RECT).collidepoint(position)
        ):
            open_concept_library()
        elif state == "APPLY" and pygame.Rect(HELPER_BUTTON_RECT).collidepoint(position):
            show_agent_hint()
        elif state == "APPLY" and pygame.Rect(MISSION_LIBRARY_BUTTON_RECT).collidepoint(position):
            open_concept_library()
        elif state == "CONCEPT_LIBRARY" and pygame.Rect(CONCEPT_BACK_BUTTON_RECT).collidepoint(position):
            close_concept_library()
        elif state == "CONCEPT_LIBRARY" and pygame.Rect(CONCEPT_TRY_BUTTON_RECT).collidepoint(position):
            start_concept_practice()
        elif state == "CONCEPT_LIBRARY":
            list_rect = pygame.Rect(CONCEPT_LIST_RECT)
            for row in range(len(concept_library)):
                row_rect = pygame.Rect(
                    list_rect.x,
                    list_rect.y + row * 27,
                    list_rect.width,
                    list_rect.height,
                )
                if row_rect.collidepoint(position):
                    selected_concept = row
                    break
        elif state == "CONCEPT_TRY" and pygame.Rect(CONCEPT_BACK_BUTTON_RECT).collidepoint(position):
            set_state("CONCEPT_LIBRARY")
        elif state == "CONCEPT_TRY" and pygame.Rect(CONCEPT_TRY_BUTTON_RECT).collidepoint(position):
            submit_concept_practice()
        elif state == "GAMEOVER_LOSS" and pygame.Rect(LOSS_RETRY_BUTTON_RECT).collidepoint(position):
            restart_current_level()
        elif state == "GAMEOVER_LOSS" and pygame.Rect(LOSS_ROADMAP_BUTTON_RECT).collidepoint(position):
            return_to_roadmap()
        elif state == "MENU" and pygame.Rect(MENU_BUTTON_RECT).collidepoint(position):
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
    elif event.type == pygame.KEYDOWN:
        handle_key(event)
