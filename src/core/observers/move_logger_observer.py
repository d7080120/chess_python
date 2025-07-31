from src.core.observers.observer import IObserver
from src.core.game_logic.Command import Command

class MoveLoggerObserver(IObserver):
    def __init__(self):
        self.logs: list[str] = []

    def update(self, command: Command):
        line = f"[{command.timestamp}] {command.piece_id}: {command.type} → {command.target or ''}"
        self.logs.append(line)

    def get_log(self):
        return self.logs
