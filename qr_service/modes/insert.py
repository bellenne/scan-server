from .base import BaseMode


class InsertMode(BaseMode):
    name = "insert"

    def handle_scan(self, app, raw: str, norm: str) -> None:
        print(f"[INSERT MODE] RAW:  {raw}")
        print(f"[INSERT MODE] NORM: {norm}")
        # сюда потом добавишь запись в БД / отправку в API
        app.audio.play_mode(self.name, "success")
