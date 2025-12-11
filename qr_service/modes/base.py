from abc import ABC, abstractmethod


class BaseMode(ABC):
    """
    Каждый режим реализует этот интерфейс.
    """

    name: str  # строковое имя режима, например "compare"

    @abstractmethod
    def handle_scan(self, app, raw: str, norm: str) -> None:
        """
        Обработка обычного скана (НЕ сервисной команды).
        app — ссылка на QRServiceApp, можно вызывать его методы.
        """
        ...
