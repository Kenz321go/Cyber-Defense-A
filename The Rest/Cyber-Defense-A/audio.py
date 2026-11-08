"""Optional game audio with generated fallbacks for missing sound assets."""

import math
import os
from array import array

import pygame

try:
    import numpy as np
except ImportError:
    np = None


class SoundManager:
    SOUND_FILES = {
        "key": "key.wav",
        "submit": "submit.wav",
        "success": "success.wav",
        "error": "error.wav",
        "combo": "combo.wav",
        "level_complete": "level_complete.wav",
        "boss_intro": "boss_intro.wav",
        "alarm": "alarm.wav",
        "menu_hover": "menu_hover.wav",
        "menu_click": "menu_click.wav",
        "ambient": "ambient.wav",
    }

    TONES = {
        "key": (1050, 0.025),
        "submit": (620, 0.075),
        "success": (880, 0.24),
        "error": (150, 0.2),
        "combo": (1250, 0.3),
        "level_complete": (740, 0.48),
        "boss_intro": (90, 0.65),
        "alarm": (420, 0.3),
        "menu_hover": (1450, 0.035),
        "menu_click": (520, 0.09),
        "ambient": (48, 1.0),
    }

    def __init__(self, assets_dir="assets\\sounds"):
        self.sounds = {}
        self.muted = False
        self.volume = 0.35
        self.ambient_channel = None
        self.alarm_channel = None
        self.enabled = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1)
            self.enabled = True
        except pygame.error:
            return

        for name, filename in self.SOUND_FILES.items():
            path = os.path.join(assets_dir, filename)
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except (OSError, pygame.error):
                self.sounds[name] = self._make_tone(*self.TONES[name])

        self.ambient_channel = self.sounds["ambient"].play(loops=-1)
        self.update_volume()

    @staticmethod
    def _make_tone(frequency, duration):
        mixer_info = pygame.mixer.get_init()
        if mixer_info is None:
            raise pygame.error("Mixer is not initialized")
        sample_rate, sample_format, channels = mixer_info
        if sample_format != -16:
            sample_rate = 22050
            channels = max(channels, 1)
        sample_count = max(1, round(sample_rate * duration))
        if np is not None:
            positions = np.arange(sample_count, dtype=np.float64) / sample_rate
            envelope = np.linspace(1.0, 0.0, sample_count, dtype=np.float64)
            wave = (np.sin(2 * np.pi * frequency * positions) * envelope * 5000).astype(np.int16)
            samples = np.repeat(wave[:, None], channels, axis=1).tobytes()
        else:
            samples_array = array("h")
            for index in range(sample_count):
                envelope = 1 - index / sample_count
                value = int(5000 * envelope * math.sin(2 * math.pi * frequency * index / sample_rate))
                samples_array.extend([value] * channels)
            samples = samples_array.tobytes()
        return pygame.mixer.Sound(buffer=samples)

    def update_volume(self):
        if not self.enabled:
            return
        effective = 0.0 if self.muted else self.volume
        for sound in self.sounds.values():
            sound.set_volume(effective)

    def play(self, event):
        if not self.enabled or self.muted:
            return None
        sound = self.sounds.get(event)
        if sound is None:
            return None
        return sound.play()

    def update_alarm(self, takeover_percent):
        if not self.enabled:
            return
        if self.muted:
            if self.alarm_channel:
                self.alarm_channel.stop()
                self.alarm_channel = None
            return
        if takeover_percent > 70 and self.alarm_channel is None:
            self.alarm_channel = self.sounds["alarm"].play(loops=-1)
        elif takeover_percent <= 70 and self.alarm_channel is not None:
            self.alarm_channel.stop()
            self.alarm_channel = None

    def toggle_mute(self):
        self.muted = not self.muted
        self.update_volume()
        if self.muted:
            if self.alarm_channel:
                self.alarm_channel.stop()
                self.alarm_channel = None
        elif self.ambient_channel is None:
            self.ambient_channel = self.sounds["ambient"].play(loops=-1)

    def adjust_volume(self, delta):
        self.volume = max(0.0, min(1.0, self.volume + delta))
        self.update_volume()

    def shutdown(self):
        if self.ambient_channel:
            self.ambient_channel.stop()
            self.ambient_channel = None
        if self.alarm_channel:
            self.alarm_channel.stop()
            self.alarm_channel = None
