from abc import ABC, abstractmethod


class BaseServiceCommand(ABC):
    """
    Сервисная команда вида: service:<name>_<arg?>
    Например: service:setmode_compare
    """

    name: str  # имя команды, после 'service:', до '_'

    @abstractmethod
    def execute(self, app, arg: str | None) -> None:
        ...
