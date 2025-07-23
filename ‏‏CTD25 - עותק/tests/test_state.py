# import pytest
# from interfaces.State import State
# from interfaces.Command import Command
# from interfaces.mock_img import MockImg
# from interfaces.Board import Board
# from interfaces.Physics import Physics
# from interfaces.Graphics import Graphics
# from interfaces.Moves import Moves

# class DummyPhysics(Physics):
#     def __init__(self, pos, board):
#         super().__init__(pos, board)
#         self._cmd = None
#         self._now = 0

#     def reset(self, cmd):
#         self._cmd = cmd

#     def update(self, now_ms):
#         if now_ms - self._now >= 1000:
#             return self._cmd
#         return None

# class DummyGraphics(Graphics):
#     def __init__(self, sprites_folder, board):
#         super().__init__(sprites_folder, board)
#         self.updated = False
#         self.last_cmd = None

#     def reset(self, cmd):
#         self.last_cmd = cmd

#     def update(self, now_ms):
#         self.updated = True

# def create_dummy_state():
#     board = Board(100, 100, 1, 1, 8, 8, MockImg())
#     graphics = DummyGraphics(sprites_folder="CTD25/pieces/RB/states/idle/sprites", board=board)
#     physics = DummyPhysics((0, 0), board)
#     moves = Moves()
#     return State(moves, graphics, physics)

# def test_reset_sets_command_and_delegates():
#     state = create_dummy_state()
#     cmd = Command(timestamp=0, piece_id="BB", type="move", params=[(0, 0), (1, 2)])
#     state.reset(cmd)
#     assert state.get_command() == cmd
#     assert state._graphics.last_cmd == cmd
#     assert state._physics._cmd == cmd

# def test_update_calls_update_and_processes_transition():
#     s1 = create_dummy_state()
#     s2 = create_dummy_state()
#     cmd = Command(timestamp=0, piece_id="BB", type="move", params=[(0, 0), (1, 2)])
#     s1.set_transition("move", s2)
#     s1.reset(cmd)
#     result_state = s1.update(now_ms=1500)
#     assert result_state == s2

# def test_can_transition_logic():
#     s = create_dummy_state()
#     cmd = Command(timestamp=0, piece_id="BB", type="move", params=[(0, 0), (1, 1)])
#     s.reset(cmd)
#     assert s.can_transition(now_ms=0) is False
#     assert s.can_transition(now_ms=1500) is True

# def test_no_transition_returns_same_state():
#     s1 = create_dummy_state()
#     cmd = Command(timestamp=0, piece_id="BB", type="jump", params=[])
#     s1.reset(cmd)
#     result = s1.update(now_ms=1500)
#     assert result == s1


import pathlib
import pytest
from interfaces.State import State
from interfaces.Moves import Moves
from interfaces.Command import Command
from interfaces.mock_img import MockImg
from interfaces.Board import Board
from interfaces.Graphics import Graphics
from interfaces.Physics import Physics


class DummyPhysics(Physics):
    def __init__(self, start_cell, board):
        super().__init__(start_cell, board)
        self._cmd = None
        self._updated = False

    def reset(self, cmd):
        self._cmd = cmd

    def update(self, now_ms):
        if not self._updated:
            self._updated = True
            return self._cmd
        return None


class DummyGraphics(Graphics):
    def __init__(self, sprites_folder, board):
        super().__init__(sprites_folder, board)

    def reset(self, cmd):
        self._cmd = cmd

    def update(self, now_ms):
        self._updated = True


@pytest.fixture
def dummy_state():
    board = Board(100, 100, 1, 1, 8, 8, img=MockImg())
    moves = Moves(pathlib.Path("CTD25/pieces/RB/moves.txt"), dims=(8, 8))
    graphics = DummyGraphics(pathlib.Path("CTD25/pieces/RB/states/idle/sprites"), board)
    physics = DummyPhysics((0, 0), board)
    return State(moves, graphics, physics)


def test_state_reset_sets_command(dummy_state):
    cmd = Command(timestamp=0, piece_id="test", type="move", params=[(0, 0), (1, 1)])
    dummy_state.reset(cmd)
    assert dummy_state.get_command() == cmd


def test_state_update_triggers_transition(dummy_state):
    cmd = Command(timestamp=123, piece_id="test", type="move", params=[(0, 0), (1, 1)])
    dummy_state.reset(cmd)

    new_state = dummy_state  # looping state to simulate transition
    dummy_state.set_transition("move", new_state)
    updated_state = dummy_state.update(now_ms=999)

    assert updated_state is new_state


def test_state_no_transition_if_command_type_unknown(dummy_state):
    cmd = Command(timestamp=123, piece_id="test", type="fly", params=[])
    dummy_state.reset(cmd)
    updated_state = dummy_state.update(now_ms=1000)
    assert updated_state is dummy_state


def test_state_can_transition_returns_false_by_default(dummy_state):
    assert dummy_state.can_transition(0) is False


def test_get_command_returns_last_command(dummy_state):
    cmd = Command(timestamp=5, piece_id="g1", type="idle", params=[])
    dummy_state.reset(cmd)
    assert dummy_state.get_command().type == "idle"

