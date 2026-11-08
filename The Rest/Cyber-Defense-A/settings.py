"""Display, input, and color settings for Cyber Defense."""

# ======================================================================
# SETTINGS
# ======================================================================
W, H = 450, 350         # small "pixel" surface everything is drawn on
SCALE = 2               # default windowed scale (900 x 700)
FPS = 60
MAX_INPUT = 40          # max characters in the console
HINT_AFTER = 2          # wrong attempts before the hint appears
MENU_BUTTON_RECT = (25, 250, 400, 44)
VICTORY_BUTTON_RECT = (75, 250, 300, 44)
LOSS_RETRY_BUTTON_RECT = (42, 250, 176, 44)
LOSS_ROADMAP_BUTTON_RECT = (232, 250, 176, 44)
TRAINING_BUTTON_RECT = (43, 109, 170, 42)
MISSION_BUTTON_RECT = (237, 109, 170, 42)
RESUME_BUTTON_RECT = (233, 238, 182, 30)
MASTER_BUTTON_RECT = (35, 238, 182, 30)
ROADMAP_BUTTON_RECT = (90, 294, 270, 38)
LEVEL_COMPLETE_BUTTON_RECT = (90, 286, 270, 38)
LIBRARY_BUTTON_RECT = (145, 276, 160, 29)
CONCEPT_TRY_BUTTON_RECT = (245, 296, 184, 34)
CONCEPT_BACK_BUTTON_RECT = (20, 296, 184, 34)
CONCEPT_LIST_RECT = (15, 66, 128, 24)
HELPER_BUTTON_RECT = (338, 92, 44, 16)
MISSION_LIBRARY_BUTTON_RECT = (386, 92, 52, 16)
MISSION_SETTINGS_BUTTON_RECT = (420, 2, 22, 16)
BOSS_HELPER_BUTTON_RECT = (15, 294, 58, 18)
BOSS_LIBRARY_BUTTON_RECT = (78, 294, 67, 18)

# Neon cyberpunk palette
BG = (10, 10, 24)
GRID = (22, 24, 52)
PANEL = (16, 16, 40)
CYAN = (0, 255, 255)
PINK = (255, 45, 149)
GREEN = (57, 255, 20)
RED = (255, 40, 60)
YELLOW = (255, 225, 60)
WHITE = (230, 230, 245)
DIM = (155, 165, 195)


def get_viewport(window_size):
    """Return the centered, aspect-preserving canvas viewport in a window."""
    window_width, window_height = window_size
    scale = min(window_width / W, window_height / H)
    width = round(W * scale)
    height = round(H * scale)
    return (window_width - width) // 2, (window_height - height) // 2, width, height


def screen_to_canvas(position, window_size):
    """Map a window position to logical canvas coordinates."""
    left, top, width, height = get_viewport(window_size)
    return (
        (position[0] - left) * W / width,
        (position[1] - top) * H / height,
    )
