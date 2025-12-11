import time
import sys
from pathlib import Path

from .config_loader import load_config
from .config import SOUNDS_GLOBAL, SOUNDS_MODES, SERVICE_PREFIX
from .scanner import Scanner
from .audio import AudioPlayer
from .normalizer import normalize_code
from .modes import ALL_MODES
from .services import ALL_COMMANDS


class QRServiceApp:
    def __init__(self, default_vid: int, default_pid: int, baudrate: int):
        # --------------------------------------------
        #  RUNTIME DIRECTORY
        # --------------------------------------------
        if getattr(sys, "frozen", False):
            # EXE mode
            self.runtime_dir = Path(sys.executable).resolve().parent
        else:
            # Python mode
            self.runtime_dir = Path(__file__).resolve().parent.parent

        # --------------------------------------------
        #  LOAD CONFIG
        # --------------------------------------------
        self.config = load_config(self.runtime_dir)
        scan_cfg = self.config["scanner"]

        # --------------------------------------------
        #  INIT SCANNER (WITH CONFIG)
        # --------------------------------------------
        self.scanner = Scanner(
            use_vid_pid=scan_cfg["use_vid_pid"],
            vid=int(scan_cfg["vid"], 16) if scan_cfg["vid"] else default_vid,
            pid=int(scan_cfg["pid"], 16) if scan_cfg["pid"] else default_pid,
            keywords=scan_cfg["fallback_keywords"],
            baudrate=baudrate,
            fallback_search=scan_cfg["fallback_search"]
        )

        # --------------------------------------------
        #  AUDIO SYSTEM
        # --------------------------------------------
        self.audio = AudioPlayer(SOUNDS_GLOBAL, SOUNDS_MODES)

        # --------------------------------------------
        #  REGISTER MODES
        # --------------------------------------------
        self._modes_by_name = {}
        for mode_cls in ALL_MODES:
            mode_obj = mode_cls()
            self._modes_by_name[mode_obj.name] = mode_obj

        self.current_mode = self._modes_by_name["compare"]

        # --------------------------------------------
        #  REGISTER SERVICE COMMANDS
        # --------------------------------------------
        self._commands_by_name = {}
        for cmd_cls in ALL_COMMANDS:
            cmd_obj = cmd_cls()
            self._commands_by_name[cmd_obj.name] = cmd_obj

    # --------------------------------------------
    #  MODES
    # --------------------------------------------

    def get_mode(self, name: str):
        return self._modes_by_name.get(name.lower())

    # --------------------------------------------
    #  SERVICE COMMANDS
    # --------------------------------------------

    def _is_service_command(self, raw: str) -> bool:
        return raw.strip().lower().startswith(SERVICE_PREFIX)

    def _handle_service_command(self, raw: str) -> None:
        text = raw.strip()
        payload = text.split(":", 1)[1].strip()

        if not payload:
            print("⚠ Пустая сервисная команда")
            self.audio.play_global("service_error")
            return

        # split into cmd + arg
        cmd_name, arg = (payload.split("_", 1) + [None])[:2]
        cmd_name = cmd_name.lower()

        cmd = self._commands_by_name.get(cmd_name)
        if cmd is None:
            print(f"⚠ Неизвестная сервисная команда: {cmd_name}")
            self.audio.play_global("service_command_error")
            return

        print(f"[SERVICE CMD] {cmd_name} (arg={arg})")
        cmd.execute(self, arg)

    # --------------------------------------------
    #  MAIN LOOP
    # --------------------------------------------

    def run(self):
        print("=== QR Service App Started ===")
        print(f"Текущий режим: {self.current_mode.name}")

        # -------------------------------------------------------
        # WAIT FOR SCANNER CONNECTION
        # -------------------------------------------------------
        print("Ожидание подключения сканера...")
        connectionErrorIsPlayed = False

        while True:
            if self.scanner.try_open():
                print("📡 Сканер подключён!")
                self.audio.play_global("connection_success")
                break

            print("⚠ Сканер не найден. Повтор через 3 сек...")
            if connectionErrorIsPlayed == False:
                self.audio.play_global("connection_error")
                connectionErrorIsPlayed = True
            time.sleep(3)

        print("Готов к сканированию!\n")

        # -------------------------------------------------------
        # MAIN READ LOOP
        # -------------------------------------------------------
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
