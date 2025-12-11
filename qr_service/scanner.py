import serial
import serial.tools.list_ports


class Scanner:
    def __init__(self, vid: int, pid: int, baudrate: int, timeout: float = 0.1):
        self.vid = vid
        self.pid = pid
        self.baudrate = baudrate
        self.timeout = timeout
        self._ser: serial.Serial | None = None

    def _find_port(self) -> str | None:
        for port in serial.tools.list_ports.comports():
            if port.vid and port.pid and port.vid == self.vid and port.pid == self.pid:
                print(f"➡ Найден сканер на порту: {port.device}")
                return port.device
        return None

    def open(self):
        port = self._find_port()
        if port is None:
            raise RuntimeError("Сканер не найден. Проверь VID/PID и подключение.")
        self._ser = serial.Serial(port, self.baudrate, timeout=self.timeout)

    @property
    def is_open(self) -> bool:
        return self._ser is not None and self._ser.is_open

    def read_line(self) -> str | None:
        if not self.is_open:
            return None
        if self._ser.in_waiting:
            raw = self._ser.readline().decode(errors="ignore").strip()
            return raw or None
        return None
