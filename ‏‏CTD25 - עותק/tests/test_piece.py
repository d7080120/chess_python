import pytest
from unittest.mock import MagicMock
from interfaces.Piece import Piece
from interfaces.Command import Command
from interfaces.Board import Board

@pytest.fixture
def dummy_state():
    state = MagicMock()
    state._graphics.get_img.return_value = "mock_img"
    state._physics.get_pos.return_value = (2, 3)
    state.update.side_effect = lambda now: state  # state = state.update()
    state.process_command.side_effect = lambda cmd, now: state
    return state

def test_piece_init(dummy_state):
    piece = Piece("p1", dummy_state)
    assert piece._piece_id == "p1"
    assert piece._state == dummy_state

def test_command_not_for_this_piece(dummy_state):
    piece = Piece("p1", dummy_state)
    cmd = Command(timestamp=0, piece_id="other", type="move", params=[])
    piece.on_command(cmd, now_ms=1000)
    dummy_state.process_command.assert_not_called()

def test_command_for_this_piece(dummy_state):
    piece = Piece("p1", dummy_state)
    cmd = Command(timestamp=0, piece_id="p1", type="move", params=[])
    piece.on_command(cmd, now_ms=1000)
    dummy_state.process_command.assert_called_once_with(cmd, 1000)

def test_piece_reset(dummy_state):
    piece = Piece("p1", dummy_state)
    piece.reset(start_ms=500)
    dummy_state.reset.assert_called_once_with(500)

def test_piece_update(dummy_state):
    piece = Piece("p1", dummy_state)
    piece.update(now_ms=1200)
    dummy_state.update.assert_called_once_with(1200)

def test_draw_on_board(dummy_state):
    board = MagicMock()
    piece = Piece("p1", dummy_state)
    piece.draw_on_board(board, now_ms=0)
    board.draw.assert_called_once_with((2, 3), "mock_img")
