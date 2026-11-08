# Cyber Defense

Cyber Defense is a pixel-art game for learning Python and cybersecurity basics. Defend a mainframe from a rogue AI by solving coding missions and repairing bugs.

## Features

- WRITE, DEBUG, CHOOSE, ORDER, SPEED, and BOSS challenges
- Short lessons, hints, and simulated terminal feedback
- Training, campaign progression, saved progress, and Master Mode
- Optional audio with generated tones as a fallback

## Run

Requires Python and Pygame Community Edition:

```bash
python -m pip install pygame-ce
python main.py
```

## Getting started

Choose **Training** to learn without a timer or failure, or **Play Mission** for timed challenges and campaign progress. Complete all four levels to unlock Master Mode and replay each level's BOSS challenge.

Use the arrow keys to navigate, **Enter** to select or submit, and **Escape** to go back. Press **F1** for a lesson and **F2** to open the Concept Library.

For level-by-level mission descriptions and the full controls, see [the gameplay guide](docs/GAMEPLAY.md).

## Project layout

- `main.py` — starts the game
- `game_engine.py` — game state, progression, and input
- `missions.py` — mission and concept content
- `screens.py`, `ui_components.py` — rendering and interface
- `dialogue.py`, `audio.py` — dialogue and sound
- `settings.py` — display and gameplay settings

The game renders on a 450 × 350 logical canvas, scaled to fit the display. Optional custom audio files go in `assets/sounds/`.
