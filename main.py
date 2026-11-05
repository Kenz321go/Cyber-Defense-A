"""Application entry point for Cyber Defense."""

import pygame

from audio import SoundManager
import game_engine as engine
from screens import draw_frame, present
from settings import FPS, H, SCALE, W
from ui_components import init_fonts
from game_engine import handle_event, update_effects

# ======================================================================
# MAIN LOOP
# ======================================================================
def main():
    pygame.init()
    engine.sound_manager = SoundManager()
    if engine.sound_manager.enabled:
        engine.type_sound = engine.sound_manager.sounds["key"]

    pygame.display.set_caption("CYBER DEFENSE: Patch the System")
    screen = pygame.display.set_mode((W * SCALE, H * SCALE))
    canvas = pygame.Surface((W, H))
    clock = pygame.time.Clock()
    pygame.key.set_repeat(400, 40)
    init_fonts()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                handle_event(event)

        update_effects()
        draw_frame(canvas)
        present(screen, canvas)
        clock.tick(FPS)

    if engine.sound_manager:
        engine.sound_manager.shutdown()
    pygame.quit()


if __name__ == "__main__":
    main()
