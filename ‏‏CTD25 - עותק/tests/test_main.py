import pytest
from interfaces.Game import Game
from interfaces.Board import Board
from interfaces.Piece import Piece
from interfaces.State import State
from interfaces.Graphics import Graphics
from interfaces.Physics import Physics
from interfaces.mock_img import MockImg  # הוספה

class FakePhysics(Physics):
    def __init__(self): self.update_called = 0
    def update(self, now):
        self.update_called += 1
        if self.update_called > 5:
            return "done"
        return None

class FakeGraphics(Graphics):
    def draw_on_board(self, board, now): pass
    def get_img(self): return None

class DummyState(State):
    def __init__(self):
        self.name = "idle"
        self.transition = {}
        self.updated = 0

    def update(self, now):
        self.updated += 1
        return self if self.updated < 5 else self.transition.get("move", self)

    def add_transition(self, action, state):
        self.transition[action] = state

class DummyPiece(Piece):
    def __init__(self, piece_id):
        self.piece_id = piece_id
        self.updated = False
        self.reset_called = False

    def reset(self, t): self.reset_called = True
    def update(self, t): self.updated = True
    def draw_on_board(self, board, now): pass
    def on_command(self, cmd, now=None): self.last_cmd = cmd

def test_WhenGameTimeIncreases():
    board = Board(64, 64, 1, 1, 8, 8, MockImg())
    game = Game([], board)
    t1 = game.game_time_ms()
    t2 = game.game_time_ms()
    assert t2 >= t1

def test_WhenResetCalledInRun():
    board = Board(64, 64, 1, 1, 8, 8, MockImg())
    p = DummyPiece("A")
    game = Game([p], board)
    game._is_win = lambda: True
    game._show = lambda: False
    game._announce_win = lambda: None
    game.run()
    assert p.reset_called

def test_WhenUpdateCalledInLoop():
    board = Board(64, 64, 1, 1, 8, 8, MockImg())
    p = DummyPiece("A")
    game = Game([p], board)
    game._is_win = lambda: game.game_time_ms() > 10
    game._show = lambda: False
    game._announce_win = lambda: None
    game.run()
    assert p.updated
