# Gameplay Guide

## Mission types

Each level has four regular tasks and a final BOSS task.

- **CHOOSE:** Select an answer from a list.
- **ORDER:** Put code lines in the correct sequence.
- **SPEED:** Answer a short coding question before time runs out.
- **WRITE:** Type the required Python line.
- **DEBUG:** Fix an incorrect Python line.
- **BOSS:** Reconstruct a script from its code lines.

## Tasks by level

### Level 1 — Variables & Data Types

1. **CHOOSE:** Select the assignment that stores `10` in `security`.
2. **ORDER:** Set the agent name, check whether it is `admin`, then grant access.
3. **SPEED:** Set `is_locked` to `True`.
4. **DEBUG:** Remove the quotes around `1.5` so `speed` is a number.
5. **BOSS:** Arrange a script that registers an agent, sets its access level, checks its admin status, and grants access.

### Level 2 — Selections & Operators

1. **CHOOSE:** Select the comparison that detects a user who is not `admin` (`!=`).
2. **WRITE:** Write an `if` condition that checks whether `attempts` is greater than `3`.
3. **SPEED:** Repair the offline-status `if` line by adding its missing colon.
4. **WRITE:** Write an `if` condition that checks whether `clearance` is at least `3`.
5. **BOSS:** Arrange a script that checks a threat level and prints `ALARM` or `Safe`.

### Level 3 — Lists & Dictionaries

1. **CHOOSE:** Select the list assignment that stores ports `80` and `443`.
2. **DEBUG:** Put quotes around the text value `'patched'` in a dictionary assignment.
3. **SPEED:** Change the index so `first_port` reads the first item in `ports` (`ports[0]`).
4. **DEBUG:** Replace list-style brackets with dictionary braces for the user profile.
5. **BOSS:** Arrange a script that creates an admin user and active-users list, adds the user, and prints the user's role.

### Level 4 — Functions & Exceptions

1. **CHOOSE:** Select the valid `secure_system` function header, including its colon.
2. **WRITE:** Write the header for `block_ip` with an `ip_address` parameter.
3. **SPEED:** Complete the `ZeroDivisionError` handler line with its missing colon.
4. **WRITE:** Write the line that starts a protected `try` block.
5. **BOSS:** Arrange a `secure_system` function that returns `True` in a `try` block and returns `False` when it catches `ZeroDivisionError`.

## Controls

- **Story:** Press any key to skip.
- **Mode select:** Click a mode or press **1** for Training, **2** for Play Mission, or **3** to resume.
- **Roadmap:** Click a ready or played level, or use **Left/Right** to select; press **Enter** to start.
- **Master Mode:** Complete all four levels to unlock. Choose a level and press **Enter** to go directly to its BOSS challenge.
- **Concept Library:** Open it from the mode screen or with **F2** during a mission. Choose a topic and try its mini task. In its answer field, **Left/Right** move the cursor and **Backspace/Delete** edit.
- **Typed answers:** Press **Enter** to submit; use **Backspace** and **Left/Right** to edit. **Ctrl+C / Ctrl+V** copy and paste.
- **CHOOSE:** **Up/Down** to select, then **Enter**.
- **ORDER:** **Up/Down** to select a line, **Left/Right** to reorder, then **Enter**.
- **BOSS:** Type one script line at a time and press **Enter**. Use **Left/Right** to move the cursor.
- **Hints:** Training hints are unlimited. In Play Mission, the first three hints per task add 10%, 15%, then 20% rogue AI takeover. At 100%, the mission is lost.
- **F1:** Open or close the lesson.
- **F3:** Open settings during a mission. While settings are open, press **M**, **R**, or **+/-** to adjust audio and effects.
- **Escape:** Close a panel or return to the previous screen. **F11:** Toggle fullscreen.

Play Mission progress and Rogue AI takeover are saved. Correct tasks do not reduce takeover; retrying after a loss starts a fresh attempt.
