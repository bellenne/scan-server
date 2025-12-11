from .base import BaseMode

class CompareMode(BaseMode):
    name = "compare"

    def __init__(self):
        self.first_raw = None
        self.first_norm = None

    def reset(self):
        self.first_raw = None
        self.first_norm = None

    def handle_scan(self, app, raw, norm):
        if self.first_raw is None:
            self.first_raw = raw
            self.first_norm = norm
            print("→ Первый код записан")
            return

        if norm == self.first_norm:
            print("✓ Совпало!")
            app.audio.play_mode(self.name, "success")
        else:
            print("✗ Не совпало!")
            app.audio.play_mode(self.name, "fail")

        self.reset()
