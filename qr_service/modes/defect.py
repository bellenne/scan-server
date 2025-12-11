from .base import BaseMode


class DefectMode(BaseMode):
    name = "defect"

    def handle_scan(self, app, raw: str, norm: str) -> None:
        print(f"[DEFECT MODE] RAW:  {raw}")
        print(f"[DEFECT MODE] NORM: {norm}")
        # сюда потом можно писать инфу о браке и т.д.
        app.audio.play_mode(self.name, "success")
