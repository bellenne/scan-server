import serial
import serial.tools.list_ports


class Scanner:
    def __init__(
        self,
        use_vid_pid: bool,
        vid: int,
        pid: int,
        keywords: list[str],
        baudrate: int,
        fallback_search: bool = True,
        timeout: float = 0.1
    ):
        self.use_vid_pid = use_vid_pid
        self.vid = vid
        self.pid = pid
        self.keywords = [kw.lower() for kw in (keywords or [])]
        self.baudrate = baudrate
        self.timeout = timeout
        self.fallback_search = fallback_search
        self._ser: serial.Serial | None = None

    # --------------------------------------------
    # PORT SEARCH
    # --------------------------------------------

    def _find_port(self) -> str | None:
        ports = list(serial.tools.list_ports.comports())

        # 1) SEARCH BY VID/PID
        if self.use_vid_pid and self.vid and self.pid:
            for port in ports:
                if port.vid == self.vid and port.pid == self.pid:
                    return port.device

        # 2) FALLBACK SEARCH
        if self.fallback_search:
            for port in ports:
                desc = (port.description or "").lower()
                name = (port.name or "").lower()

                for kw in self.keywords:
                    if kw in desc or kw in name:
                        return port.device

        return None

    # --------------------------------------------
    # TRY CONNECT (NO ERRORS)
    # --------------------------------------------

    def try_open(self) -> bool:
        """Attempt to open the scanner once. Return True if successful."""
        port = self._find_port()
        if not port:
            return False

        try:
            self._ser = serial.Serial(port, self.baudrate, timeout=self.timeout)
            return True
        except:
            return False

    # --------------------------------------------

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
