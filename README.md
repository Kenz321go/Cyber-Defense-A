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

- **Menu:** Click the mission button to start.
- **During a mission:** Type your answer and press **Enter**. Use **Backspace** and the **Left/Right** arrows to edit.
- **CHOOSE:** Use **Up/Down**, then **Enter**.
- **ORDER/BOSS:** Use **Up/Down** to select a line, **Left/Right** to reorder, then **Enter**.
- **F1:** Open or close the lesson.
- **M:** Mute/unmute audio; **+/-:** Adjust volume; **R:** Toggle reduced visual effects.
- While entering a typed answer, use **Ctrl+M**, **Ctrl+R**, and **Ctrl +/-** for those controls so the unmodified characters remain available to type.
- **Ctrl+C / Ctrl+V:** Copy the current answer or paste text into typed-answer missions.
- **Escape:** Quit.

## Project layout

- `main.py` — Initializes Pygame and runs the main loop.
- `game_engine.py` — Game states, mission progression, input, and effects.
- `missions.py` — Mission content and challenge data.
- `screens.py` and `ui_components.py` — Screen rendering and reusable UI elements.
- `dialogue.py` — Handler and rogue AI dialogue.
- `audio.py` — Optional audio playback and generated sound fallbacks.
- `settings.py` — Display, input, and color settings.

The game uses a 450 × 350 logical canvas, scaled up for display. To use custom audio, place supported sound files in `assets/sounds/`; the game can also run without them.
