from observer import IObserver
from Command import Command

PIECE_VALUES = {
    "P": 1,  # Pawn
    "N": 3,  # Knight
    "B": 3,  # Bishop
    "R": 5,  # Rook
    "Q": 9   # Queen
}

class ScoreObserver(IObserver):
    def __init__(self):
        self.score = {"Player1": 0, "Player2": 0}

    def update(self, command: Command):
        if command.type == "capture" and command.params and len(command.params) >= 2:
            captured_id = command.params[1]  # assuming params = [attacker_id, captured_id]
            piece_type = captured_id[0].upper()
            value = PIECE_VALUES.get(piece_type, 0)

            if "W" in command.piece_id:
                self.score["Player1"] += value
            elif "B" in command.piece_id:
                self.score["Player2"] += value

    def get_score(self):
        return self.score