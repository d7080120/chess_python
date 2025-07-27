from abc import ABC, abstractmethod
from Command import Command
from typing import Callable

class IObserver(ABC):
    @abstractmethod
    def update(self, command: Command):
        pass

    def get_callback(self) -> Callable[[Command], None]:
        return self.update

class ISubject(ABC):
    @abstractmethod
    def subscribe(self, command_type: str, observer: IObserver):
        pass

    @abstractmethod
    def unsubscribe(self, command_type: str, observer: IObserver):
        pass

    @abstractmethod
    def notify(self, command: Command):
        pass
