"""Mission content organized by preset, level, and exercise."""

# ======================================================================
# MASTER DATA
# ----------------------------------------------------------------------
# game_data[preset][level][exercise]
#   - Each level has four normal tasks and a fifth boss task.
#   - Level dicts hold a "title" (string) plus integer keys 1..5 (exercises).
#   - Exercise dict keys:
#       "mode"        : WRITE, DEBUG, CHOOSE, ORDER, SPEED, or BOSS
#       "id"          : stable ticket number
#       "title"       : ticket title
#       "objective"   : player-facing mission description
#       "ticket"      : short task label (maximum 60 characters)
#       "priority"    : LOW, MED, HIGH, or CRITICAL
#       "lesson"      : full teaching text for the F1 briefing
#       "broken_code" : the buggy line for DEBUG mode, or None for WRITE mode
#       "expected"    : the single line of Python the player must type
#       "correct_script": ordered full script lines for Boss challenges
#       "scrambled_blocks": reordered code clues for the Boss reconstruction
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
                          "MISSION: The firewall's clearance field is empty. Policy requires a numeric "
                          "level of ten in the existing security setting. Choose the assignment that "
                          "stores this policy value correctly.",
                "broken_code": None,
                "expected": "security = 10",
                "hint": "name = value   (one = sign, spaces around it)",
                "output": ["> running patch...", "> security = 10 OK", "> firewall restored"]},
            2: {"mode": "ORDER",
                "ticket": "Restore authorized admin access",
                "priority": "MED",
                "lesson": "A check cannot use a value before it exists, and a grant should only follow "
                          "a successful check. MISSION: An authorized operator is identified as admin. "
                          "Reorder the access procedure so the identity is established before the "
                          "comparison and the grant happens last.",
                "broken_code": None,
                "expected": "agent = 'admin'",
                "hint": "Set agent first, compare with ==, then grant access.",
                "output": ["> running patch...", "> admin access checked", "> access granted"]},
            3: {"mode": "WRITE",
                "ticket": "Set system lock status",
                "priority": "HIGH",
                "lesson": "A bool is either True or False (capital first letter, no quotes). "
                          "MISSION: The intrusion report says the lock flag is active, not inactive. "
                          "Update the system's is_locked setting with the correct Boolean value.",
                "broken_code": None,
                "expected": "is_locked = True",
                "hint": "is_locked = True   (capital T, no quotes)",
                "output": ["> running patch...", "> is_locked = True OK", "> access controls active"]},
            4: {"mode": "DEBUG",
                "ticket": "Convert connection speed to float",
                "priority": "MED",
                "lesson": "Quotes turn a value into text (str). A float is a number with a decimal "
                          "point and NO quotes. MISSION: Telemetry expects a numeric speed for "
                          "calculations, but the displayed value is currently text. Repair the line "
                          "so the stored value behaves as the decimal number one and a half.",
                "broken_code": "speed = '1.5'",
                "expected": "speed = 1.5",
                "hint": "Remove the quotes around 1.5 so it is a number.",
                "output": ["> running patch...", "> speed = 1.5 OK", "> telemetry restored"]},
            5: {"mode": "BOSS",
                "ticket": "Configure admin access",
                "priority": "CRITICAL",
                "objective": "Order Ghost's level-5 admin setup; grant access only after the check passes.",
                "lesson": "An operative named ghost is arriving with clearance tier five. The system "
                          "must record the operative, set the tier and admin flag, then print "
                          "'Access Granted' only after the admin check passes.",
                "broken_code": None,
                "scrambled_blocks": [
                    "if is_admin == True:",
                    "access_level = 5",
                    "print('Access Granted')",
                    "agent_name = 'ghost'",
                    "is_admin = True",
                ],
                "correct_script": [
                    "agent_name = 'ghost'",
                    "access_level = 5",
                    "is_admin = True",
                    "if is_admin == True:",
                    "print('Access Granted')",
                ],
                "hint": "Register the agent before setting and checking access.",
                "output": ["> running patch...", "> admin access configured", "> agent authenticated"]},
        },

        # ---------------- LEVEL 2 ----------------
        2: {
            "title": "Selections & Operators",
            1: {"mode": "CHOOSE",
                "ticket": "Repair firewall comparison",
                "priority": "CRITICAL",
                "lesson": "Use != to test that two values are different. "
                          "MISSION: The firewall should flag every account except admin. The current "
                          "comparison uses assignment where a condition is required; choose the "
                          "operator that means the account name is different from admin.",
                "broken_code": "if user = 'admin':",
                "expected": "if user != 'admin':",
                "options": [
                    "if user = 'admin':",
                    "if user != 'admin':",
                    "if user == 'admin':",
                ],
                "answer_index": 1,
                "hint": "!= means not equal.",
                "output": ["> running patch...", "> user access checked", "> intruder scan ready"]},
            2: {"mode": "WRITE",
                "ticket": "Block repeated login attempts",
                "priority": "HIGH",
                "lesson": "Comparison operators: > < >= <= == !=   An if line ends with a colon. "
                          "MISSION: The alert policy activates only after the third failed login; "
                          "three attempts is still allowed. Write the condition that detects the "
                          "first blocked attempt.",
                "broken_code": None,
                "expected": "if attempts > 3:",
                "hint": "if attempts > 3:   (don't forget the colon)",
                "output": ["> running patch...", "> login threshold armed OK", "> brute-force guard active"]},
            3: {"mode": "DEBUG",
                "ticket": "Restore offline status check",
                "priority": "HIGH",
                "lesson": "Every if line must END with a colon : so Python knows a block follows. "
                          "MISSION: The monitor must enter its offline-response branch, but the "
                          "condition is rejected before it can run. Repair the incomplete check.",
                "broken_code": "if status == 'offline'",
                "expected": "if status == 'offline':",
                "hint": "Something is missing at the very end of the line.",
                "output": ["> running patch...", "> status check parsed OK", "> monitor back online"]},
            4: {"mode": "WRITE",
                "ticket": "Enforce clearance threshold",
                "priority": "MED",
                "lesson": ">= means 'greater than or equal to'. "
                          "MISSION: Entry policy sets tier three as the minimum: an agent at exactly "
                          "three must be admitted too. Write the condition that enforces that boundary.",
                "broken_code": None,
                "expected": "if clearance >= 3:",
                "hint": "Use >= (greater sign first, then equals).",
                "output": ["> running patch...", "> clearance policy OK", "> access tier updated"]},
            5: {"mode": "BOSS",
                "ticket": "Configure the threat alarm",
                "priority": "CRITICAL",
                "objective": "Threat is 15; compare it with 10 and print ALARM or Safe in the correct order.",
                "lesson": "A sensor reports threat level fifteen. The warning threshold is ten: "
                          "levels above it must print 'ALARM', while all other levels print 'Safe'. "
                          "Reconstruct the conditional script in the order Python needs it.",
                "broken_code": None,
                "scrambled_blocks": [
                    "print('ALARM')",
                    "if threat > 10:",
                    "threat = 15",
                    "else:",
                    "print('Safe')",
                ],
                "correct_script": [
                    "threat = 15",
                    "if threat > 10:",
                    "print('ALARM')",
                    "else:",
                    "print('Safe')",
                ],
                "hint": "Set threat first, then add the if and else branches.",
                "output": ["> running patch...", "> threat threshold armed", "> alarm ready"]},
        },

        # ---------------- LEVEL 3 ----------------
        3: {
            "title": "Lists & Dictionaries",
            1: {"mode": "WRITE",
                "ticket": "Define approved network ports",
                "priority": "HIGH",
                "lesson": "A LIST holds items in order inside square brackets [ ]. "
                          "MISSION: The network audit approved web ports 80 and 443, in that order. "
                          "Choose the list assignment that records exactly those two numeric ports.",
                "broken_code": None,
                "expected": "ports = [80, 443]",
                "hint": "Square brackets [ ] with a comma between items.",
                "output": ["> running patch...", "> ports 80, 443 approved OK", "> network filter updated"]},
            2: {"mode": "DEBUG",
                "ticket": "Patch administrator database value",
                "priority": "CRITICAL",
                "lesson": "A DICT stores key: value pairs. Change a value with dict['key'] = value. "
                          "Text values need quotes. MISSION: The database's admin record must contain "
                          "the status word patched, not a reference to an undefined variable. Repair "
                          "the update so the stored value is text.",
                "broken_code": "database['admin'] = patched",
                "expected": "database['admin'] = 'patched'",
                "hint": "patched is text, so it needs quotes around it.",
                "output": ["> running patch...", "> administrator record repaired OK", "> database integrity restored"]},
            3: {"mode": "WRITE",
                "ticket": "Read the first approved port",
                "priority": "HIGH",
                "lesson": "Python lists start at index 0, so the first item is at index 0. "
                          "MISSION: The approved port list begins with the standard web port and "
                          "keeps the secure web port second. The current lookup selects the second "
                          "entry; change it to capture the first.",
                "broken_code": "first_port = ports[1]",
                "expected": "first_port = ports[0]",
                "hint": "The first list item is at index 0.",
                "output": ["> running patch...", "> first port selected OK", "> secure service ready"]},
            4: {"mode": "DEBUG",
                "ticket": "Repair user profile dictionary",
                "priority": "HIGH",
                "lesson": "Lists use [ ] but DICTIONARIES use curly braces { } with key: value. "
                          "MISSION: The profile needs a named role field, so it must be a mapping, "
                          "not a list. The account is a guest, not a 'guess'. Repair both the "
                          "container syntax and the misspelled role value.",
                "broken_code": "user = ['role': 'guess']",
                "expected": "user = {'role': 'guest'}",
                "hint": "Dictionaries use curly braces { }.",
                "output": ["> running patch...", "> user profile parsed OK", "> role policy restored"]},
            5: {"mode": "BOSS",
                "ticket": "Add the admin to active users",
                "priority": "CRITICAL",
                "objective": "Create an admin record, add it to active_users, then print its role.",
                "lesson": "An incoming administrator must be represented by a role field. The active "
                          "roster starts empty; add that account before reporting its role. Rebuild "
                          "the statements in dependency order.",
                "broken_code": None,
                "scrambled_blocks": [
                    "print(user['role'])",
                    "active_users.append(user)",
                    "user = {'role': 'admin'}",
                    "active_users = []",
                ],
                "correct_script": [
                    "user = {'role': 'admin'}",
                    "active_users = []",
                    "active_users.append(user)",
                    "print(user['role'])",
                ],
                "hint": "Create the user and list before appending and printing.",
                "output": ["> running patch...", "> admin role assigned", "> active user added"]},
        },

        # ---------------- LEVEL 4 ----------------
        4: {
            "title": "Functions & Exceptions",
            1: {"mode": "DEBUG",
                "ticket": "Restore security function header",
                "priority": "HIGH",
                "lesson": "A FUNCTION is reusable code named with def. "
                          "The def line must end with a colon. "
                          "MISSION: Recovery relies on a reusable routine named secure_system. "
                          "Its header is almost valid, but Python cannot begin the function body "
                          "yet. Repair the declaration.",
                "broken_code": "def secure_system()",
                "expected": "def secure_system():",
                "hint": "Something is missing at the very end of the line.",
                "output": ["> running patch...", "> secure_system() loaded OK", "> recovery routine online"]},
            2: {"mode": "WRITE",
                "ticket": "Define IP blocking function",
                "priority": "MED",
                "lesson": "Parameters go inside the brackets: def name(parameter): "
                          "MISSION: The blocking routine must receive the suspicious address when "
                          "called. Declare block_ip with the single input parameter ip_address.",
                "broken_code": None,
                "expected": "def block_ip(ip_address):",
                "hint": "def function_name(parameter):",
                "output": ["> running patch...", "> block_ip(ip_address) loaded OK", "> threat response ready"]},
            3: {"mode": "DEBUG",
                "ticket": "Repair division error handler",
                "priority": "HIGH",
                "lesson": "try / except catches errors so the program does not crash. "
                          "except ends with a colon too. "
                          "MISSION: The protected calculation can divide by zero. Its dedicated "
                          "handler is present but syntactically incomplete; make the handler header "
                          "valid so the exception can be caught.",
                "broken_code": "except ZeroDivisionError",
                "expected": "except ZeroDivisionError:",
                "hint": "Every except line needs a colon at the end.",
                "output": ["> running patch...", "> division handler parsed OK", "> fault containment active"]},
            4: {"mode": "WRITE",
                "ticket": "Begin protected operation block",
                "priority": "MED",
                "lesson": "Risky code goes inside a try: block. If it fails, except: runs instead. "
                          "MISSION: A recovery routine is about to run an operation that may fail. "
                          "Add the header that opens Python's protected section.",
                "broken_code": None,
                "expected": "try:",
                "hint": "The word try followed by a colon.",
                "output": ["> running patch...", "> protected block initialized OK", "> secure execution path ready"]},
            5: {"mode": "BOSS",
                "ticket": "Complete secure error handling",
                "priority": "CRITICAL",
                "objective": "Rebuild secure_system: return True in try; catch ZeroDivisionError and return False.",
                "lesson": "Reconstruct a recovery routine named secure_system. Its protected path "
                          "returns True; if a ZeroDivisionError occurs, its handler returns False. "
                          "Arrange the function and nested blocks in valid Python order.",
                "broken_code": None,
                "scrambled_blocks": [
                    " return False",
                    "def secure_system():",
                    " except ZeroDivisionError:",
                    " try:",
                    " return True",
                ],
                "correct_script": [
                    "def secure_system():",
                    " try:",
                    " return True",
                    " except ZeroDivisionError:",
                    " return False",
                ],
                "hint": "Start with the function, then add try and except blocks.",
                "output": ["> running patch...", "> division handler installed", "> secure system ready"]},
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

concept_library = {
    "Variables": {
        "explanation": "A variable stores a value under a name. Use one = sign to assign it.",
        "example": "security = 10",
        "task": "Store the number 7 in a variable named alert_level.",
        "answer": "alert_level = 7",
        "why": "The name is on the left. The value is on the right.",
    },
    "Data Types": {
        "explanation": "Numbers, text, and True/False values have different types. Text needs quotes.",
        "example": "name = 'cipher'",
        "task": "Store True in a variable named is_safe.",
        "answer": "is_safe = True",
        "why": "True is a Boolean value. It has a capital T and no quotes.",
    },
    "Comparisons": {
        "explanation": "Comparisons check values. Use == to test equality and > to test a larger value.",
        "example": "threat == 5",
        "task": "Check if threat is equal to 3.",
        "answer": "threat == 3",
        "why": "Two equals signs compare values. One equals sign assigns a value.",
    },
    "If Statements": {
        "explanation": "An if statement runs code only when its condition is true. End the line with a colon.",
        "example": "if attempts > 3:",
        "task": "Check if attempts is greater than 2.",
        "answer": "if attempts > 2:",
        "why": "The if line checks a condition and ends with a colon.",
    },
    "Lists": {
        "explanation": "A list stores items in order. Put its items inside square brackets.",
        "example": "ports = [80, 443]",
        "task": "Make a list named ports with 22 and 80.",
        "answer": "ports = [22, 80]",
        "why": "Square brackets hold the list items, separated by a comma.",
    },
    "Dictionaries": {
        "explanation": "A dictionary stores key and value pairs. Use curly braces and a colon.",
        "example": "user = {'role': 'agent'}",
        "task": "Set config's mode key to the text 'safe'.",
        "answer": "config['mode'] = 'safe'",
        "why": "Use the key in brackets, then assign its new value.",
    },
    "Functions": {
        "explanation": "A function is reusable code. Start its header with def and end with a colon.",
        "example": "def secure_system():",
        "task": "Write a function header named scan with one parameter named target.",
        "answer": "def scan(target):",
        "why": "Put the parameter in parentheses and end the header with a colon.",
    },
    "Exceptions": {
        "explanation": "try and except handle errors so a program can keep running.",
        "example": "try:\n    connect()",
        "task": "Write the line that starts an error-handling block.",
        "answer": "try:",
        "why": "A try block begins with try followed by a colon.",
    },
}


_challenge_modes = {
    (1, 1): "CHOOSE",
    (1, 2): "ORDER",
    (1, 3): "SPEED",
    (2, 3): "SPEED",
    (3, 1): "CHOOSE",
    (3, 3): "SPEED",
    (4, 1): "CHOOSE",
    (4, 3): "SPEED",
}

_speed_questions = {
    1: "The intrusion report says the lock is active. Set the status flag accordingly.",
    2: "The monitor's offline branch is incomplete. Repair its condition header.",
    3: "The secure web port is second in the approved list. Change the lookup to return the earlier port.",
    4: "The division-by-zero recovery branch has an unfinished header. Make it valid Python.",
}

_task_reasons = {
    (1, 1): "Use = to store a value in a named variable.",
    (1, 2): "Assign agent before checking it and granting access.",
    (1, 3): "True is a Boolean value and needs no quotes.",
    (1, 4): "A float is a decimal number, not text.",
    (1, 5): "Register the agent before setting access and checking admin status.",
    (2, 1): "Use != to check that user is not admin.",
    (2, 2): "Set a value before updating and checking it.",
    (2, 3): "An if header ends with a colon.",
    (2, 4): ">= includes the threshold itself.",
    (2, 5): "Set the threat before checking it, then handle both outcomes.",
    (3, 1): "Lists keep ordered items in square brackets.",
    (3, 2): "The replacement status must be text, so quote the value.",
    (3, 3): "Python lists start at index 0, so ports[0] is first.",
    (3, 4): "Dictionaries pair keys and values inside { }.",
    (3, 5): "Create the user and list before appending and printing the role.",
    (4, 1): "Functions start with def and end with a colon.",
    (4, 2): "Define a function before using its block.",
    (4, 3): "try and except handle errors.",
    (4, 4): "Start a try block with try:",
    (4, 5): "Define the function, then return safely inside try and except.",
}

_order_challenges = {
    1: [
        "agent = 'admin'",
        "if agent == 'admin':",
        "print('Access Granted')",
    ],
}

for _level_id, _level in game_data[1].items():
    if not isinstance(_level_id, int):
        continue
    for _exercise_id, _exercise in _level.items():
        if not isinstance(_exercise_id, int):
            continue
        _exercise["why"] = _task_reasons[(_level_id, _exercise_id)]
        if _exercise_id == max(key for key in _level if isinstance(key, int)):
            _exercise["mode"] = "BOSS"
            _exercise["boss_type"] = "SCRIPT_RECONSTRUCTION"
        elif (_level_id, _exercise_id) in _challenge_modes:
            _exercise["mode"] = _challenge_modes[(_level_id, _exercise_id)]
            if _exercise["mode"] == "CHOOSE":
                if "options" not in _exercise:
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
                _exercise["order_goal"] = (
                    "The identity must be known before access is compared or granted."
                )
                _exercise["ticket"] = "Order the security procedure"
                _exercise["lesson"] = (
                    "The access log must identify the operator before evaluating the "
                    "admin check. The grant should only run when that check succeeds; "
                    "reorder the lines to make the procedure safe."
                )
            elif _exercise["mode"] == "SPEED":
                _exercise["question"] = _speed_questions[_level_id]

for _preset_id, _preset in game_data.items():
    for _level_id, _level in _preset.items():
        if not isinstance(_level_id, int):
            continue
        for _exercise_id, _exercise in _level.items():
            if not isinstance(_exercise_id, int):
                continue
            lesson = _exercise["lesson"]
            objective = lesson.partition("MISSION:")[2] or lesson
            objective = objective.split(" BOSS CHALLENGE:", 1)[0].strip()
            _exercise.setdefault(
                "id",
                _preset_id * 1000 + _level_id * 10 + _exercise_id,
            )
            _exercise.setdefault("title", _exercise["ticket"])
            _exercise.setdefault("objective", objective)
