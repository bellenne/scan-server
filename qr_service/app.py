import time

from .config import SOUNDS_GLOBAL, SOUNDS_MODES, SERVICE_PREFIX
from .scanner import Scanner
from .audio import AudioPlayer
from .normalizer import normalize_code
from .modes import ALL_MODES
from .services import ALL_COMMANDS


class QRServiceApp:
    def __init__(self, vid: int, pid: int, baudrate: int):
        self.scanner = Scanner(vid=vid, pid=pid, baudrate=baudrate)
        self.audio = AudioPlayer(SOUNDS_GLOBAL, SOUNDS_MODES)

        # регистрируем режимы
        self._modes_by_name: dict[str, object] = {}
        for mode_cls in ALL_MODES:
            mode_obj = mode_cls()
            self._modes_by_name[mode_obj.name] = mode_obj

        # режим по умолчанию
        self.current_mode = self._modes_by_name["compare"]

        # регистрируем сервисные команды
        self._commands_by_name: dict[str, object] = {}
        for cmd_cls in ALL_COMMANDS:
            cmd_obj = cmd_cls()
            self._commands_by_name[cmd_obj.name] = cmd_obj

    # --- работа с режимами ---

    def get_mode(self, name: str):
        return self._modes_by_name.get(name.lower())

    # --- сервисные команды ---

    def _is_service_command(self, raw: str) -> bool:
        return raw.strip().lower().startswith(SERVICE_PREFIX)

    def _handle_service_command(self, raw: str) -> None:
        text = raw.strip()
        payload = text.split(":", 1)[1] if ":" in text else ""
        payload = payload.strip()

        if not payload:
            print("⚠ Пустая сервисная команда")
            self.audio.play_global("service_error")
            return

        if "_" in payload:
            cmd_name, arg = payload.split("_", 1)
        else:
            cmd_name, arg = payload, None

        cmd_name = cmd_name.lower()
        cmd = self._commands_by_name.get(cmd_name)

        if cmd is None:
            print(f"⚠ Неизвестная сервисная команда: {cmd_name}")
            self.audio.play_global("service_command_error")
            return

        print(f"[SERVICE CMD] {cmd_name} (arg={arg})")
        cmd.execute(self, arg)

    # --- главный цикл ---

    def run(self):
        print("=== QR Service App Started ===")
        print(f"Текущий режим: {self.current_mode.name}")
        self.scanner.open()
        print("Готов к сканированию...\n")

        while True:
            raw = self.scanner.read_line()
            if raw is None:
                time.sleep(0.01)
                continue

            if self._is_service_command(raw):
                self._handle_service_command(raw)
                continue

            norm = normalize_code(raw)
            self.current_mode.handle_scan(self, raw, norm)
