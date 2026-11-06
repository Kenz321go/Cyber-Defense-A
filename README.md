# Cyber Defense

**Cyber Defense** is a small 2D pixel-art cybersecurity and Python-learning game built with Pygame. Play as an agent defending a mainframe from a rogue AI: solve short coding missions, repair bugs, and restore the system through a neon terminal interface.

## Features

- WRITE and DEBUG missions, plus CHOOSE, ORDER, SPEED, and end-of-level BOSS challenges.
- Short lessons, hints, simulated terminal output, and character dialogue.
- A progress meter, rogue AI takeover meter, streaks, and audio-visual feedback.
- Optional sound files, with generated tones as a fallback.

## Run the game

Install Python and Pygame Community Edition, then run:

```bash
python -m pip install pygame-ce
python main.py
```

## Controls

- **Story:** Press any key to skip.
- **Mode select:** Click a mode or press **1** for Training, **2** for Play Mission, or **3** to resume.
- **Concept Library:** Click **CONCEPT LIBRARY** on the mode screen, or **LIBRARY** during a mission. Pick a topic and try its mini task.
- **Roadmap:** Click a ready or played level to select it. Press **Enter** or click **START LEVEL** to begin; use **Left/Right** to select levels with the keyboard.
- **Training:** Learn with no timer and no fail.
- **Play Mission:** Timed challenges can fail. Your progress is saved so you can resume.
- **Mission failure:** Choose **1** to retry the level or **2** to return to the roadmap.
- **After two wrong answers:** The correct answer and a short reason appear in the console.
- Answers flash **CORRECT** or **WRONG** with a short reason.
- Mission progress saves the current level, next task, and XP after each completed task.
- **During a mission:** Type your answer and press **Enter**. Use **Backspace** and the **Left/Right** arrows to edit.
- **Agent Helper:** Click **HINT** in COMMS for two clues, then the answer and why.
- **CHOOSE:** Use **Up/Down**, then **Enter**.
- **ORDER/BOSS:** Use **Up/Down** to select a line, **Left/Right** to reorder, then **Enter**.
- **F1:** Open or close the lesson.
- **Settings icon:** Open mission audio and visual-effect controls. Press **M**, **R**, or **+/-** while settings are open.
- **F3:** Open settings; **Escape:** Close a panel or return to the previous screen.
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
