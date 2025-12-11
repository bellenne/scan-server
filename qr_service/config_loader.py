import json
from pathlib import Path


DEFAULT_CONFIG = {
    "scanner": {
        "use_vid_pid": True,
        "vid": None,
        "pid": None,
        "fallback_search": True,
        "fallback_keywords": []
    },
    "audio": {
        "enabled": True
    },
    "debug": {
        "list_ports_on_start": False
    }
}


def load_config(runtime_dir: Path):
    config_path = runtime_dir / "config.json"

    if not config_path.exists():
        print("⚠ config.json не найден. Используются настройки по умолчанию.")
        return DEFAULT_CONFIG

    try:
        with config_path.open("r", encoding="utf-8") as f:
            user_config = json.load(f)

        return _merge_dicts(DEFAULT_CONFIG, user_config)

    except Exception as e:
        print(f"⚠ Ошибка чтения config.json: {e}")
        return DEFAULT_CONFIG


def _merge_dicts(base, override):
    """Рекурсивное объединение словарей."""
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and key in result:
            result[key] = _merge_dicts(result[key], value)
        else:
            result[key] = value
    return result
