# Cyber Defense

**Cyber Defense** is a small 2D pixel-art cybersecurity and Python-learning game built with Pygame. Play as an agent defending a mainframe from a rogue AI: solve short coding missions, repair bugs, and restore the system through a neon terminal interface.

## Features

- WRITE and DEBUG missions, plus CHOOSE, ORDER, SPEED, and end-of-level BOSS challenges.
- Short lessons, hints, simulated terminal output, and character dialogue.
- Ticketed mission objectives with progress and rogue AI takeover meters, streaks, and audio-visual feedback.
- Optional sound files, with generated tones as a fallback.

## Exam review: mission types by level

Each level has four regular tasks and a final BOSS task. Task types work as follows:

- **CHOOSE:** Select the correct answer from a list.
- **ORDER:** Put code lines in the correct sequence.
- **SPEED:** Quickly answer a short coding question.
- **WRITE:** Type the required Python line.
- **DEBUG:** Fix an incorrect Python line.
- **BOSS:** Reconstruct a complete script by arranging its code lines.

### Level 1 — Variables & Data Types

1. **CHOOSE:** Select the assignment that stores `10` in `security`.
2. **ORDER:** Arrange the statements to assign the agent name, check whether it is `admin`, and grant access.
3. **SPEED:** Set `is_locked` to the Boolean value `True`.
4. **DEBUG:** Remove the quotes around `1.5` so `speed` is a number, not text.
5. **BOSS:** Arrange a script that registers an agent, sets its access level, checks its admin status, and grants access.

### Level 2 — Selections & Operators

1. **CHOOSE:** Select the comparison that detects a user who is not `admin` (`!=`).
2. **WRITE:** Write an `if` condition that checks whether `attempts` is greater than `3`.
3. **SPEED:** Repair the offline-status `if` line by adding its missing colon.
4. **WRITE:** Write an `if` condition that checks whether `clearance` is at least `3`.
5. **BOSS:** Arrange a script that sets a threat level, checks it, and prints `ALARM` or `Safe`.

### Level 3 — Lists & Dictionaries

1. **CHOOSE:** Select the list assignment that stores ports `80` and `443`.
2. **DEBUG:** Fix a dictionary assignment by putting quotes around the text value `'patched'`.
3. **SPEED:** Change the index so `first_port` reads the first item in `ports` (`ports[0]`).
4. **DEBUG:** Replace the list-style brackets with dictionary braces for the user profile.
5. **BOSS:** Arrange a script that creates an admin user and an active-users list, adds the user, and prints the user's role.

### Level 4 — Functions & Exceptions

1. **CHOOSE:** Select the valid `secure_system` function header, including its colon.
2. **WRITE:** Write the header for `block_ip` with an `ip_address` parameter.
3. **SPEED:** Complete the `ZeroDivisionError` handler line with its missing colon.
4. **WRITE:** Write the line that starts a protected `try` block.
5. **BOSS:** Arrange a `secure_system` function that returns `True` in a `try` block and returns `False` when it catches `ZeroDivisionError`.

## Run the game

Install Python and Pygame Community Edition, then run:

```bash
python -m pip install pygame-ce
python main.py
```

## Controls

- **Story:** Press any key to skip.
- **Mode select:** Click a mode or press **1** for Training, **2** for Play Mission, or **3** to resume.
- **Master Mode:** Unlock it by completing all four levels. Choose **MASTER MODE**, select any level, and press **Enter** to go straight to that level's BOSS challenge. After each of the first three bosses, return to the roadmap to choose any level; completing the Level 4 boss shows the Master celebration.
- **Concept Library:** Click **CONCEPT LIBRARY** on the mode screen, or **LIBRARY** during a mission. Pick a topic and try its mini task. In the answer field, **Left/Right** move the cursor; **Backspace/Delete** edit around it. Letters such as **R** and symbols such as **_** are entered normally.
- **Roadmap:** Click a ready or played level to select it. Press **Enter** or click **START LEVEL** to begin; use **Left/Right** to select levels with the keyboard.
- **Training:** Learn with no timer and no fail.
- **Play Mission:** Timed challenges can fail. Your progress is saved so you can resume.
- Rogue AI takeover progress is saved and restored with your mission. Correct tasks do not reduce takeover. Leaving an active task preserves the meter; retrying or returning to the roadmap after a loss starts a fresh attempt with a reset meter.
- **Mission failure:** Choose **1** to retry the level or **2** to return to the roadmap.
- **After two wrong answers:** The correct answer and a short reason appear in the console.
- Answers flash **CORRECT** or **WRONG** with a short reason.
- Mission progress saves the current level, next task, and XP after each completed task.
- **During a mission:** Type your answer and press **Enter**. Use **Backspace** and the **Left/Right** arrows to edit.
- **Agent Helper:** In Training, click **HINT** as often as you need. In Play Mission, the first three hints per task add 10%, 15%, then 20% rogue AI takeover. The red hint notice shows the actual increase; reaching 100% takeover loses the mission.
- **CHOOSE:** Use **Up/Down**, then **Enter**.
- **SPEED:** Timed tasks allow 40 seconds in Play Mission. The first **HINT** names the relevant variable or exception and gives a starting example.
- **ORDER:** Use **Up/Down** to select a line, **Left/Right** to reorder, then **Enter**.
- **BOSS:** Type each script line and press **Enter** to submit. Use **Left/Right** to move the cursor and **Backspace** to delete before the cursor.
- **F1:** Open or close the lesson.
- **Mode select:** **F1** starts Play Mission, **F2** opens the Concept Library, and **F3** opens settings.
- **F3:** Open settings during a mission; press **M**, **R**, or **+/-** while settings are open. **Escape:** Close a panel or return to the previous screen.
- The game starts fullscreen. Press **F11** to switch between fullscreen and windowed mode.
- **Ctrl+C / Ctrl+V:** Copy the current answer or paste text into typed-answer missions.

## Project layout

- `main.py` — Initializes Pygame and runs the main loop.
- `game_engine.py` — Game states, mission progression, input, and effects.
- `missions.py` — Mission content and challenge data.
- `screens.py` and `ui_components.py` — Screen rendering and reusable UI elements.
- `dialogue.py` — Handler and rogue AI dialogue.
- `audio.py` — Optional audio playback and generated sound fallbacks.
- `settings.py` — Display, input, and color settings.

The game uses a 450 × 350 logical canvas, scaled to fit the display while keeping its aspect ratio. To use custom audio, place supported sound files in `assets/sounds/`; the game can also run without them.
