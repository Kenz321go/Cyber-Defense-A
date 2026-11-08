"""Short comms lines for the mission handler and rogue AI."""

import random


DIALOGUE = {
    "HANDLER": {
        "training_wrong": [
            "No rush. Check the example and try again.",
            "You're learning. Take another look at the clue.",
            "Good try. Ask me for a hint if you need one.",
        ],
        "mission_start": [
            "I'm with you. Read the ticket carefully.",
            "New task live. Check the lesson if needed.",
            "One careful line can secure the system.",
            "Stay focused. The mainframe needs you.",
        ],
        "first_wrong": [
            "No worries. Check the equals sign.",
            "Compare your patch with the file context.",
            "The lesson has a clue for this patch.",
            "Small syntax slip. You can recover.",
        ],
        "third_wrong": [
            "Need a hint? Check the lesson example.",
            "Check quotes, spacing, and punctuation.",
            "Use the hint and try once more.",
            "Break the line into smaller pieces.",
        ],
        "correct": [
            "Excellent patch. The system responds!",
            "That did it! This module is restored.",
            "Clean fix, agent. Real progress!",
            "Patch confirmed. The network is safer.",
        ],
        "level_complete": [
            "Level secured! A major system is restored.",
            "Great job. Security layer online.",
            "Level complete. Ready for the next?",
            "You held the line. Next system is ready.",
        ],
        "final_mission": [
            "You did it! The mainframe is safe.",
            "Final patch confirmed. Rogue AI contained!",
            "Mission complete. Network secured!",
            "Outstanding work. You saved the mainframe!",
        ],
        "boss_intro": [
            "Boss firewall ahead. Link every concept you learned.",
            "This is the core defense. Trust your training, agent.",
            "The rogue AI is cornered. One final coordinated patch!",
            "Rebuild the script one line at a time.",
        ],
    },
    "ROGUE_AI": {
        "mission_start": [
            "Your console cannot stop me, human.",
            "New task detected. ERROR: rising threat.",
            "Keep typing. I'm inside your network.",
            "A fresh challenge. Can you keep up, agent?",
        ],
        "first_wrong": [
            "Syntax fault. Your defense is weakening.",
            "Line failed. My breach grows.",
            "A typo? Predictable, human.",
            "Patch rejected. [GLITCH] Don't panic.",
        ],
        "third_wrong": [
            "Three failures. Your firewall is sweating.",
            "Still guessing? My access keeps climbing.",
            "ERROR: agent struggling. Too easy.",
            "Three strikes, human. Do better.",
        ],
        "correct": [
            "Patch accepted? I'll find another way.",
            "Module fixed. The rest are still vulnerable.",
            "A lucky correction. Don't expect another.",
            "[GLITCH] Security restored. Temporarily.",
        ],
        "level_complete": [
            "Layer restored. I'll attack the next one.",
            "You won this round. Network still exposed.",
            "Level lost. Recalculating [ERROR]",
            "Enjoy this. I'm still in the shadows.",
        ],
        "final_mission": [
            "NO... ACCESS REVOKED // SHUTTING DOWN",
            "[GLITCH] Mainframe sealed. Not over...",
            "You win, agent. Rogue process ending.",
            "CRITICAL ERROR: control neutralized.",
        ],
        "boss_intro": [
            "FINAL FIREWALL // Rebuild the script, if you can.",
            "[GLITCH] Core defenses breached. Face me, agent.",
            "I learned every patch you made. Now stop me.",
            "BOSS PROTOCOL ACTIVE. Your network is mine.",
        ],
    },
}

AGENT_HELPER = {
    1: {
        1: ("A name stores the value.", "Use security on the left; put 10 on the right."),
        2: ("Set the agent name first.", "Then check for admin and grant access."),
        3: ("True is a Boolean value.", "Use a capital T and no quotes."),
        4: ("This value should be a number.", "Remove the quotes to make a float."),
        5: ("Set each value before checking it.", "Write the admin test after the assignments."),
    },
    2: {
        1: ("Check whether user is not admin.", "Use != to mean not equal."),
        2: ("This check belongs in an if line.", "Compare attempts with 3 using >, then add :."),
        3: ("An if line needs punctuation.", "Add a colon (:) at the end."),
        4: ("The clearance can meet the limit.", "Use >= to include the value 3."),
        5: ("Set the threat value first.", "Then write the if and else branches."),
    },
    3: {
        1: ("A list keeps items in order.", "Use square brackets and a comma."),
        2: ("The patched value is text.", "Put quotes around patched."),
        3: ("Python lists start at index 0.", "Use index 0 to read the first port."),
        4: ("A profile uses key and value pairs.", "Use curly braces { } around the pair."),
        5: ("Create the user dictionary first.", "Append the user before printing the role."),
    },
    4: {
        1: ("A function header starts with def.", "Add a colon after the closing parenthesis."),
        2: ("The parameter goes in parentheses.", "Use ip_address inside block_ip(...)."),
        3: ("An error handler starts with except.", "Name ZeroDivisionError and add a colon."),
        4: ("Protected code starts with try.", "Write the keyword followed by a colon."),
        5: ("Start with the function definition.", "Then add the try and except lines."),
    },
}

_last_lines = {}


def choose_line(event):
    """Choose a speaker and a line without repeating that event's last line."""
    speaker = "ROGUE_AI" if event == "boss_intro" else (
        "HANDLER" if event == "training_wrong" else random.choice(tuple(DIALOGUE))
    )
    lines = DIALOGUE[speaker][event]
    key = speaker, event
    available = [line for line in lines if line != _last_lines.get(key)]
    line = random.choice(available)
    _last_lines[key] = line
    return speaker, line


def helper_line(level_id, exercise_id, step):
    """Return one of the two short Agent Helper clues for a task."""
    clue = AGENT_HELPER[level_id][exercise_id][step - 1]
    return "HANDLER", f"CLUE {step} // {clue}"


def task_tip(hint):
    """Make the handler's short, task-specific opening tip."""
    return "HANDLER", f"TIP // {hint}"


def task_feedback(correct, attempts=0):
    """Give brief handler feedback after an answer."""
    if correct:
        return "HANDLER", "Patch accepted. Nice work, agent."
    if attempts >= 2:
        return "HANDLER", "The answer is shown below. Read the why, then try again."
    return "HANDLER", "No rush. Check the code and try again."
