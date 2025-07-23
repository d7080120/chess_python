
import numpy as np
import pathlib
from interfaces.Physics import Physics
from interfaces.Board import Board
from interfaces.Command import Command

class DummyPiece:
    def __init__(self, piece_type="rook"):
        self.type = piece_type

class DummyPhysics(Physics):
    def __init__(self, start_cell, board, speed_m_s=1.0):
        super().__init__(start_cell, board, speed_m_s)
        self._pos = start_cell

    def update(self, now_ms):
        return Command(timestamp=now_ms, piece_id="test", type="idle", params=[])

    def reset(self, cmd):
        self._pos = tuple(cmd.params[0])

    def get_pos(self):
        return self._pos

    def can_capture(self):
        return False

    def can_be_captured(self):
        return True

def test_physics_update():
    board = Board(cell_H_pix=100, cell_W_pix=100, cell_H_m=1, cell_W_m=1, W_cells=8, H_cells=8, img=None)
    physics = DummyPhysics(start_cell=(0, 0), board=board)
    cmd = physics.update(1000)
    assert isinstance(cmd, Command)
    assert cmd.timestamp == 1000

def test_physics_reset_and_get_pos():
    board = Board(cell_H_pix=100, cell_W_pix=100, cell_H_m=1, cell_W_m=1, W_cells=8, H_cells=8, img=None)
    physics = DummyPhysics(start_cell=(2, 3), board=board)
    new_cmd = Command(timestamp=0, piece_id="p1", type="move", params=[(5, 5)])
    physics.reset(new_cmd)
    assert physics.get_pos() == (5, 5)

def test_capture_abilities():
    board = Board(cell_H_pix=100, cell_W_pix=100, cell_H_m=1, cell_W_m=1, W_cells=8, H_cells=8, img=None)
    physics = DummyPhysics(start_cell=(0, 0), board=board)
    assert physics.can_capture() is False
    assert physics.can_be_captured() is True
