from observer import ISubject, IObserver
from collections import defaultdict
from Command import Command
from typing import Callable

class CommandSubject(ISubject):
    def __init__(self):
        self._subscribers = defaultdict(dict)  # type: dict[str, dict[IObserver, Callable[[Command], None]]]

    def subscribe(self, command_type: str, observer: IObserver):
        self._subscribers[command_type][observer] = observer.get_callback()

    def unsubscribe(self, command_type: str, observer: IObserver):
        if observer in self._subscribers[command_type]:
            del self._subscribers[command_type][observer]

    def notify(self, command: Command):
        for callback in self._subscribers.get(command.type, {}).values():
            callback(command)
