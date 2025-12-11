import serial
import serial.tools.list_ports
import time
import winsound



# Укажи VID/PID своего устройства из диспетчера
SCANNER_VID = 0x1EAB   # пример! заменишь на свои значения
SCANNER_PID = 0x3306


def find_scanner_port():
    """Поиск порта сканера по VID/PID."""
    for port in serial.tools.list_ports.comports():
        if port.vid and port.pid:
            if port.vid == SCANNER_VID and port.pid == SCANNER_PID:
                print(f"➡ Найден сканер на порту: {port.device}")
                return port.device
    print("❌ Сканер не найден. Проверь подключение.")
    return None


def normalize_code(raw: str) -> str:
    """
    Приводит разные форматы к единому виду.
    'AG-BR-010_400x270|0'        -> 'AG-BR-010_400x270'
    '123456|4|AG-BR-010_400x270' -> 'AG-BR-010_400x270'
    """
    raw = raw.strip()
    parts = raw.split("|")

    if len(parts) <= 2:
        return parts[0]
    else:
        return parts[-1]


def success_voice():
    """Проигрывает success.wav — 'Всё верно!'."""
    winsound.PlaySound("success.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)


def error_voice():
    """Проигрывает error.wav — 'Не тот шильд!'."""
    winsound.PlaySound("error.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)


def main():
    port = find_scanner_port()
    if port is None:
        return

    ser = serial.Serial(port, 9600, timeout=0.1)

    first_raw = None
    first_norm = None

    print("=== QR Compare Daemon (Normalize + Voice) ===")
    print("Готов к сканированию...\n")

    while True:
        if ser.in_waiting:
            raw = ser.readline().decode(errors="ignore").strip()
            if not raw:
                continue

            norm = normalize_code(raw)

            print(f"[SCANNED RAW ] {raw}")
            print(f"[NORMALIZED  ] {norm}")

            # первый код
            if first_raw is None:
                first_raw = raw
                first_norm = norm
                print(f"→ Код №1 (raw):  {first_raw}")
                print(f"→ Код №1 (norm): {first_norm}\n")
                continue

            # второй код
            second_raw = raw
            second_norm = norm
            print(f"→ Код №2 (raw):  {second_raw}")
            print(f"→ Код №2 (norm): {second_norm}")

            # сравниваем уже нормализованные значения
            if first_norm == second_norm:
                print("✓ Всё верно!\n")
                success_voice()
            else:
                print("✗ Не тот шильд!\n")
                error_voice()

            # сброс для следующей пары
            first_raw = None
            first_norm = None

        time.sleep(0.01)


if __name__ == "__main__":
    main()