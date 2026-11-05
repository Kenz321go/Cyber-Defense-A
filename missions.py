"""Mission content organized by preset, level, and exercise."""

# ======================================================================
# MASTER DATA
# ----------------------------------------------------------------------
# game_data[preset][level][exercise]
#   - Level dicts hold a "title" (string) plus integer keys 1..5 (exercises).
#   - Exercise dict keys:
#       "mode"        : WRITE, DEBUG, CHOOSE, ORDER, SPEED, or BOSS
#       "ticket"      : short task label (maximum 60 characters)
#       "priority"    : LOW, MED, HIGH, or CRITICAL
#       "lesson"      : full teaching text for the F1 briefing
#       "broken_code" : the buggy line for DEBUG mode, or None for WRITE mode
#       "expected"    : the single line of Python the player must type
#       "hint"        : shown in yellow after HINT_AFTER wrong attempts
#       "output"      : simulated console output; player code is never executed
# ======================================================================
game_data = {

    # ------------------------------------------------------------------
    # PRESET 1
    # ------------------------------------------------------------------
    1: {
        # ---------------- LEVEL 1 ----------------
        1: {
            "title": "Variables & Data Types",
            1: {"mode": "WRITE",
                "ticket": "Assign security clearance",
                "priority": "HIGH",
                "lesson": "A VARIABLE is a named box that stores data. Use = to put a value inside. "
                          "MISSION: The mainframe has NO security level! Create a variable called "
                          "security and store the number 10 in it.",
                "broken_code": None,
                "expected": "security = 10",
                "hint": "name = value   (one = sign, spaces around it)",
                "output": ["> running patch...", "> security = 10 OK", "> firewall restored"]},
            2: {"mode": "DEBUG",
                "ticket": "Repair agent name assignment",
                "priority": "MED",
                "lesson": "= ASSIGNS a value, but == COMPARES two values. "
                          "MISSION: A bug stops the agent name from being saved! "
                          "Fix the line so it STORES 'ghost' in agent_name.",
                "broken_code": "agent_name == 'ghost'",
                "expected": "agent_name = 'ghost'",
                "hint": "Storing a value needs a SINGLE equals sign.",
                "output": ["> running patch...", "> agent_name saved OK", "> identity verified"]},
            3: {"mode": "WRITE",
                "ticket": "Set system lock status",
                "priority": "HIGH",
                "lesson": "A bool is either True or False (capital first letter, no quotes). "
                          "MISSION: Lock down the system! Create a variable called is_locked "
                          "and set it to True.",
                "broken_code": None,
                "expected": "is_locked = True",
                "hint": "is_locked = True   (capital T, no quotes)",
                "output": ["> running patch...", "> is_locked = True OK", "> access controls active"]},
            4: {"mode": "DEBUG",
                "ticket": "Convert connection speed to float",
                "priority": "MED",
                "lesson": "Quotes turn a value into text (str). A float is a number with a decimal "
                          "point and NO quotes. MISSION: Connection speed is stored as text! "
                          "Fix it so it is the number 1.5.",
                "broken_code": "speed = '1.5'",
                "expected": "speed = 1.5",
                "hint": "Remove the quotes around 1.5 so it is a number.",
                "output": ["> running patch...", "> speed = 1.5 OK", "> telemetry restored"]},
            5: {"mode": "WRITE",
                "ticket": "Assign agent codename",
                "priority": "LOW",
                "lesson": "A str stores text and needs quotes around it: 'like this'. "
                          "MISSION: Assign a codename. Create a variable called codename "
                          "and store the text 'cipher' in it.",
                "broken_code": None,
                "expected": "codename = 'cipher'",
                "hint": "codename = 'cipher'   (text goes inside quotes)",
                "output": ["> running patch...", "> codename registered OK", "> agent authenticated"]},
        },

        # ---------------- LEVEL 2 ----------------
        2: {
            "title": "Selections & Operators",
            1: {"mode": "DEBUG",
                "ticket": "Repair firewall comparison",
                "priority": "CRITICAL",
                "lesson": "An IF checks a condition. To COMPARE use ==, not =. "
                          "MISSION: The firewall check is broken! Fix the line so it "
                          "compares threat to 5.",
                "broken_code": "if threat = 5:",
                "expected": "if threat == 5:",
                "hint": "Comparing needs a DOUBLE equals sign (==).",
                "output": ["> running patch...", "> firewall comparison OK", "> threat scan restored"]},
            2: {"mode": "WRITE",
                "ticket": "Block repeated login attempts",
                "priority": "HIGH",
                "lesson": "Comparison operators: > < >= <= == !=   An if line ends with a colon. "
                          "MISSION: Too many login tries! Write an if that checks whether "
                          "attempts is greater than 3.",
                "broken_code": None,
                "expected": "if attempts > 3:",
                "hint": "if attempts > 3:   (don't forget the colon)",
                "output": ["> running patch...", "> login threshold armed OK", "> brute-force guard active"]},
            3: {"mode": "DEBUG",
                "ticket": "Restore offline status check",
                "priority": "HIGH",
                "lesson": "Every if line must END with a colon : so Python knows a block follows. "
                          "MISSION: The status check will not run. Fix the line!",
                "broken_code": "if status == 'offline'",
                "expected": "if status == 'offline':",
                "hint": "Something is missing at the very end of the line.",
                "output": ["> running patch...", "> status check parsed OK", "> monitor back online"]},
            4: {"mode": "WRITE",
                "ticket": "Enforce clearance threshold",
                "priority": "MED",
                "lesson": ">= means 'greater than or equal to'. "
                          "MISSION: Only high-clearance agents may enter. Write an if that "
                          "checks whether clearance is greater than or equal to 3.",
                "broken_code": None,
                "expected": "if clearance >= 3:",
                "hint": "Use >= (greater sign first, then equals).",
                "output": ["> running patch...", "> clearance policy OK", "> access tier updated"]},
            5: {"mode": "WRITE",
                "ticket": "Reject non-admin accounts",
                "priority": "MED",
                "lesson": "!= means 'NOT equal to'. "
                          "MISSION: Spot the intruders! Write an if that checks whether "
                          "user is not equal to the text 'admin'.",
                "broken_code": None,
                "expected": "if user != 'admin':",
                "hint": "if user != 'admin':   (text needs quotes, end with a colon)",
                "output": ["> running patch...", "> account filter OK", "> intruder checks active"]},
        },

        # ---------------- LEVEL 3 ----------------
        3: {
            "title": "Lists & Dictionaries",
            1: {"mode": "WRITE",
                "ticket": "Define approved network ports",
                "priority": "HIGH",
                "lesson": "A LIST holds items in order inside square brackets [ ]. "
                          "MISSION: Define the open network ports. Create a list called "
                          "ports containing 80 and 443.",
                "broken_code": None,
                "expected": "ports = [80, 443]",
                "hint": "Square brackets [ ] with a comma between items.",
                "output": ["> running patch...", "> ports 80, 443 approved OK", "> network filter updated"]},
            2: {"mode": "DEBUG",
                "ticket": "Patch administrator database value",
                "priority": "CRITICAL",
                "lesson": "A DICT stores key: value pairs. Change a value with dict['key'] = value. "
                          "Text values need quotes. "
                          "MISSION: Patch the admin account! Fix the line.",
                "broken_code": "database['admin'] = patched",
                "expected": "database['admin'] = 'patched'",
                "hint": "patched is text, so it needs quotes around it.",
                "output": ["> running patch...", "> administrator record repaired OK", "> database integrity restored"]},
            3: {"mode": "WRITE",
                "ticket": "Open secure service port",
                "priority": "HIGH",
                "lesson": "Add an item to the end of a list with list.append(item). "
                          "MISSION: Open a new port! Add the number 8080 to the "
                          "ports list.",
                "broken_code": None,
                "expected": "ports.append(8080)",
                "hint": "ports.append(8080)   (a dot, then append, then brackets)",
                "output": ["> running patch...", "> port 8080 added OK", "> secure service listening"]},
            4: {"mode": "DEBUG",
                "ticket": "Repair user profile dictionary",
                "priority": "HIGH",
                "lesson": "Lists use [ ] but DICTIONARIES use curly braces { } with key: value. "
                          "MISSION: The user profile was built with the wrong brackets! "
                          "Fix the line.",
                "broken_code": "user = ['role': 'guest']",
                "expected": "user = {'role': 'guest'}",
                "hint": "Dictionaries use curly braces { }.",
                "output": ["> running patch...", "> user profile parsed OK", "> role policy restored"]},
            5: {"mode": "WRITE",
                "ticket": "Set server to secure mode",
                "priority": "CRITICAL",
                "lesson": "Update a dictionary: dict['key'] = 'new value'. "
                          "MISSION: Switch the server mode! Set the 'mode' key of "
                          "config to the text 'secure'.",
                "broken_code": None,
                "expected": "config['mode'] = 'secure'",
                "hint": "config['mode'] = 'secure'   (quotes around key AND value)",
                "output": ["> running patch...", "> server mode = secure OK", "> configuration locked"]},
        },

        # ---------------- LEVEL 4 ----------------
        4: {
            "title": "Functions & Exceptions",
            1: {"mode": "DEBUG",
                "ticket": "Restore security function header",
                "priority": "HIGH",
                "lesson": "A FUNCTION is reusable code named with def. "
                          "The def line must end with a colon. "
                          "MISSION: The function will not run! Fix the line.",
                "broken_code": "def secure_system()",
                "expected": "def secure_system():",
                "hint": "Something is missing at the very end of the line.",
                "output": ["> running patch...", "> secure_system() loaded OK", "> recovery routine online"]},
            2: {"mode": "WRITE",
                "ticket": "Define IP blocking function",
                "priority": "MED",
                "lesson": "Parameters go inside the brackets: def name(parameter): "
                          "MISSION: Write the header of a function called block_ip "
                          "that takes one parameter named ip_address.",
                "broken_code": None,
                "expected": "def block_ip(ip_address):",
                "hint": "def function_name(parameter):",
                "output": ["> running patch...", "> block_ip(ip_address) loaded OK", "> threat response ready"]},
            3: {"mode": "DEBUG",
                "ticket": "Repair division error handler",
                "priority": "HIGH",
                "lesson": "try / except catches errors so the program does not crash. "
                          "except ends with a colon too. "
                          "MISSION: Fix the handler that catches a ZeroDivisionError.",
                "broken_code": "except ZeroDivisionError",
                "expected": "except ZeroDivisionError:",
                "hint": "Every except line needs a colon at the end.",
                "output": ["> running patch...", "> division handler parsed OK", "> fault containment active"]},
            4: {"mode": "WRITE",
                "ticket": "Begin protected operation block",
                "priority": "MED",
                "lesson": "Risky code goes inside a try: block. If it fails, except: runs instead. "
                          "MISSION: Begin an error-handling block. "
                          "Write the line that starts a try block.",
                "broken_code": None,
                "expected": "try:",
                "hint": "The word try followed by a colon.",
                "output": ["> running patch...", "> protected block initialized OK", "> secure execution path ready"]},
            5: {"mode": "WRITE",
                "ticket": "Report successful security check",
                "priority": "CRITICAL",
                "lesson": "return sends a value back out of a function. "
                          "MISSION: Final patch! The secure_system function must report "
                          "success. Write the line that returns True.",
                "broken_code": None,
                "expected": "return True",
                "hint": "return True   (capital T)",
                "output": ["> running patch...", "> security status = True OK", "> mainframe protection restored"]},
        },
    },

    # ------------------------------------------------------------------
    # >>> ADD PRESET 2 HERE <<<
    # Copy the whole "1: { ... }" block above, rename the key to 2, then
    # rewrite the titles / lessons / answers. Keep the same shape:
    #     2: { 1: {"title": ..., 1: {...}, ..., 5: {...}}, 2: {...}, 3: {...}, 4: {...} },
    #
    # >>> ADD PRESET 3 HERE <<<   (key 3, same shape)
    # >>> ADD PRESET 4 HERE <<<   (key 4, same shape)
    # >>> ADD PRESET 5 HERE <<<   (key 5, same shape)
    #
    # Nothing else needs to change: finishing the last level of a preset
    # automatically moves to the next preset key if it exists (see
    # advance() below), and loops back to Preset 1 after the last one.
    # To let players PICK a preset, just set `current_preset` before the
    # game starts (e.g. from a menu screen).
    # ------------------------------------------------------------------
}


_challenge_modes = {
    (1, 1): "CHOOSE",
    (1, 2): "ORDER",
    (1, 3): "SPEED",
    (2, 1): "CHOOSE",
    (2, 2): "ORDER",
    (2, 3): "SPEED",
    (3, 1): "CHOOSE",
    (3, 2): "ORDER",
    (3, 3): "SPEED",
    (4, 1): "CHOOSE",
    (4, 2): "ORDER",
    (4, 3): "SPEED",
}

_speed_questions = {
    1: "Set is_locked to the boolean True.",
    2: "Repair the offline status check line.",
    3: "Add port 8080 to the ports list.",
    4: "Finish the ZeroDivisionError handler line.",
}

_boss_orders = {
    1: [
        "security = 10",
        "is_locked = True",
        "codename = 'cipher'",
    ],
    2: [
        "if attempts > 3:",
        "if clearance >= 3:",
        "if user != 'admin':",
    ],
    3: [
        "ports = [80, 443]",
        "ports.append(8080)",
        "config['mode'] = 'secure'",
    ],
    4: [
        "def secure_system():",
        "    try:",
        "        return True",
        "    except ZeroDivisionError:",
        "        return False",
    ],
}

_order_challenges = {
    1: [
        "security = 10",
        "agent_name = 'ghost'",
        "codename = 'cipher'",
    ],
    2: [
        "if threat == 5:",
        "if attempts > 3:",
        "if clearance >= 3:",
    ],
    3: _boss_orders[3],
    4: [
        "def secure_system():",
        "    try:",
        "        return True",
        "    except ZeroDivisionError:",
        "        return False",
    ],
}

for _level_id, _level in game_data[1].items():
    if not isinstance(_level_id, int):
        continue
    for _exercise_id, _exercise in _level.items():
        if not isinstance(_exercise_id, int):
            continue
        if _exercise_id == max(key for key in _level if isinstance(key, int)):
            _exercise["mode"] = "BOSS"
            _exercise["boss_type"] = "ORDER"
            _exercise["boss_order"] = _boss_orders[_level_id]
            _exercise["lesson"] += (
                " BOSS CHALLENGE: combine the level concepts in the correct order."
            )
        elif (_level_id, _exercise_id) in _challenge_modes:
            _exercise["mode"] = _challenge_modes[(_level_id, _exercise_id)]
            if _exercise["mode"] == "CHOOSE":
                correct = _exercise["expected"]
                _exercise["options"] = [
                    correct.replace(" = ", " == ", 1) if " = " in correct else correct + ";",
                    correct,
                    correct.rstrip(":") if correct.endswith(":") else correct + ":",
                ]
                _exercise["answer_index"] = 1
            elif _exercise["mode"] == "ORDER":
                _exercise["order_lines"] = list(_order_challenges[_level_id])
                _exercise["expected_order"] = list(_exercise["order_lines"])
                _exercise["ticket"] = "Order the security procedure"
                _exercise["lesson"] = (
                    "Arrange the related Python statements into a secure sequence."
                )
            elif _exercise["mode"] == "SPEED":
                _exercise["question"] = _speed_questions[_level_id]
