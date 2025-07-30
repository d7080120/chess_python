"""
conftest.py - Pytest configuration and shared fixtures
"""
import sys
import pathlib
import pytest
from unittest.mock import Mock

# הוסף את נתיב הIt1_interfaces לPython path
current_dir = pathlib.Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root / "It1_interfaces"))

@pytest.fixture
def mock_game():
    """Mock game object for testing"""
    game = Mock()
    game.pieces = []
    return game

@pytest.fixture
def sample_command():
    """Sample Command for testing"""
    from Command import Command
    import time
    
    return Command(
        timestamp=int(time.time() * 1000),
        piece_id="PW0",
        type="move",
        from_pos=(0, 6),
        to_pos=(0, 5),
        captured_piece=None,
        target=(0, 5)
    )

@pytest.fixture
def capture_command():
    """Sample capture Command for testing"""
    from Command import Command
    import time
    
    return Command(
        timestamp=int(time.time() * 1000),
        piece_id="NB0",
        type="move",
        from_pos=(1, 0),
        to_pos=(2, 2),
        captured_piece="PW1",
        target=(2, 2)
    )
