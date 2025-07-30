"""
conftest.py - הגדרות משותפות לכל הטסטים
"""
import pytest
import sys
import pathlib
from unittest.mock import Mock

# הוסף את הנתיב לתיקיית המחלקות
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "It1_interfaces"))

@pytest.fixture
def mock_game():
    """Mock game object for testing"""
    return Mock()

@pytest.fixture
def sample_command():
    """Sample command for testing"""
    from Command import Command
    import time
    
    return Command(
        timestamp=int(time.time() * 1000),
        piece_id="PW",
        type="move",
        from_pos=(0, 6),
        to_pos=(0, 5),
        captured_piece=None,
        target=(0, 5)
    )

@pytest.fixture
def capture_command():
    """Sample capture command for testing"""
    from Command import Command
    import time
    
    return Command(
        timestamp=int(time.time() * 1000),
        piece_id="NW",
        type="move",
        from_pos=(2, 7),
        to_pos=(1, 1),
        captured_piece="PB",
        target=(1, 1)
    )

@pytest.fixture
def score_manager(mock_game):
    """ScoreManager instance for testing"""
    from ScoreManager import ScoreManager
    return ScoreManager(mock_game)

@pytest.fixture
def observer_setup(mock_game):
    """Setup observers for testing"""
    from integration_setup import setup_observers
    return setup_observers(mock_game)
