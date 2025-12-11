from .base import BaseServiceCommand


class SetModeCommand(BaseServiceCommand):
    name = "setmode"

    def execute(self, app, arg: str | None) -> None:
        if not arg:
            print("⚠ setmode: не передан режим")
            app.audio.play_global("service_error")
            return

        mode = app.get_mode(arg)
        if mode is None:
            print(f"⚠ Неизвестный режим: {arg}")
            app.audio.play_global("service_error")
            return

        # сбрасываем состояние режима сравнения, если надо
        from qr_service.modes.compare import CompareMode
        if isinstance(app.current_mode, CompareMode):
            app.current_mode.reset()

        app.current_mode = mode
        print(f"🔁 Режим переключён на: {mode.name}")
        app.audio.play_global_sync("mode_changed")
        app.audio.play_mode_sync(mode.name, "name")
