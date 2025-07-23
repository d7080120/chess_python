import pytest
from interfaces.Game import Game
from interfaces.Board import Board
from interfaces.Command import Command
from interfaces.Piece import Piece
from interfaces.State import State
from interfaces.Graphics import Graphics
from interfaces.Physics import Physics
from interfaces.Moves import Moves
from interfaces.mock_img import MockImg
import time
import pathlib

class DummyGraphics(Graphics):
    def __init__(self): pass
    def reset(self, *args): pass
    def update(self, *args): pass
    def get_img(self): return None
    def draw_on_board(self, board, now): pass

class DummyPhysics(Physics):
    def __init__(self): pass
    def reset(self, *args): return None
    def update(self, *args): return None

class DummyState(State):
    def __init__(self): pass
    def reset(self, *args): pass
    def update(self, now): return self
    def process_command(self, cmd, now=None): return self
    def get_command(self): return None

class DummyPiece(Piece):
    def __init__(self, piece_id="P"):
        self.piece_id = piece_id
        self.reset_called = False
        self.updated = False

    def reset(self, t): self.reset_called = True
    def update(self, t): self.updated = True
    def draw_on_board(self, board, now): pass
    def on_command(self, cmd, now=None): self.last_cmd = cmd


def test_game_init():
    board = Board(100, 100, 1, 1, 8, 8, None)
    p = DummyPiece("a1")
    game = Game([p], board)
    assert "a1" in game.pieces
    assert game.board == board


def test_game_time_increases():
    board = Board(100, 100, 1, 1, 8, 8, None)
    game = Game([], board)
    t1 = game.game_time_ms()
    time.sleep(0.1)
    t2 = game.game_time_ms()
    assert t2 > t1


def test_clone_board_returns_copy():
    board = Board(100, 100, 1, 1, 8, 8, None)
    board.clone = lambda: "copy!"
    game = Game([], board)
    assert game.clone_board() == "copy!"

def test_reset_on_start():
    board = Board(100, 100, 1, 1, 8, 8, None)
    p = DummyPiece("p1")
    game = Game([p], board)
    game.start_user_input_thread()
    game._is_win = lambda: True  # skip loop
    game._show = lambda: False
    game._announce_win = lambda: None
    game.run()
    assert p.reset_called


def test_update_called_in_loop():
    mock_img = MockImg()
    board = Board(100, 100, 1, 1, 8, 8, mock_img)
    p = DummyPiece("p1")
    game = Game([p], board)
    game._is_win = lambda: game.game_time_ms() > 10  # run for 10 ms
    game._show = lambda: False
    game._announce_win = lambda: None
    game.run()
    assert p.updated


def test_process_command_dispatch():
    board = Board(100, 100, 1, 1, 8, 8, None)
    p = DummyPiece("p1")
    game = Game([p], board)
    cmd = Command(timestamp=0, piece_id="p1", type="move", params=[(0, 0), (1, 1)])
    game._process_input(cmd, now=0)
    assert p.last_cmd == cmd
