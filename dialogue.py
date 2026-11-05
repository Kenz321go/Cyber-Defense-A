"""Short comms lines for the mission handler and rogue AI."""

import random


DIALOGUE = {
    "HANDLER": {
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
            "Stay calm. Rebuild the security chain in order.",
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
            "FINAL FIREWALL // Your training will not save you.",
            "[GLITCH] Core defenses breached. Face me, agent.",
            "I learned every patch you made. Now stop me.",
            "BOSS PROTOCOL ACTIVE. Your network is mine.",
        ],
    },
}

_last_lines = {}


def choose_line(event):
    """Choose a speaker and a line without repeating that event's last line."""
    speaker = "ROGUE_AI" if event == "boss_intro" else random.choice(tuple(DIALOGUE))
    lines = DIALOGUE[speaker][event]
    key = speaker, event
    available = [line for line in lines if line != _last_lines.get(key)]
    line = random.choice(available)
    _last_lines[key] = line
    return speaker, line
