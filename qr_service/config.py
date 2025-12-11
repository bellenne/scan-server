from pathlib import Path

# VID/PID сканера (подставь свои значения)
SCANNER_VID = 0x1EAB  # пример
SCANNER_PID = 0x3306  # пример

BAUDRATE = 9600

BASE_DIR = Path(__file__).resolve().parent.parent

AUDIO_DIR = BASE_DIR / "audio"

SERVICE_PREFIX = "service:"  # начало сервисной команды

# ==== GLOBAL SOUNDS ====
SOUNDS_GLOBAL = {
    "mode_changed": AUDIO_DIR / "mode_changed.wav",
    "service_error": AUDIO_DIR / "error.wav",
    "service_success": AUDIO_DIR / "success.wav",
    "service_command_error": AUDIO_DIR / "service_command_error.wav",
    "connection_error": AUDIO_DIR / "connection_error.wav",
    "connection_success": AUDIO_DIR / "connection_success.wav"
}

# ==== MODE-SPECIFIC SOUNDS ====
SOUNDS_MODES = {
    "compare": {
        "name": AUDIO_DIR / "compare_name.wav",
        "success": AUDIO_DIR / "compare_success.wav",
        "fail": AUDIO_DIR / "compare_fail.wav",
    },
    "insert": {
        "name": AUDIO_DIR / "insert_name.wav",
        "success": AUDIO_DIR / "insert_success.wav",
        "fail": AUDIO_DIR / "insert_fail.wav",
    },
    "defect": {
        "name": AUDIO_DIR / "defect_name.wav",
        "success": AUDIO_DIR / "defect_success.wav",
        "fail": AUDIO_DIR / "defect_fail.wav",
    },
}