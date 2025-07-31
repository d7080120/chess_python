"""
conftest.py - Pytest configuration and shared fixtures
Enhanced for chess game visual improvements and focus solution
"""
import sys
import pathlib
import pytest
from unittest.mock import Mock, MagicMock
import importlib.util

# הוסף את נתיב הIt1_interfaces לPython path
current_dir = pathlib.Path(__file__).parent
project_root = current_dir.parent
IT1_INTERFACES_PATH = project_root / "It1_interfaces"
sys.path.insert(0, str(IT1_INTERFACES_PATH))


def check_module_available(module_name):
    """Check if a module is available for import"""
    try:
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except (ImportError, ValueError):
        return False


@pytest.fixture
def mock_game():
    """Enhanced mock game object for testing with visual components"""
    game = MagicMock()
    game.pieces = []
    
    # Mock player name manager
    game.player_name_manager.get_player1_name.return_value = "Player 1"
    game.player_name_manager.get_player2_name.return_value = "Player 2"
    
    # Mock score manager  
    game.score_manager.get_scores.return_value = (0, 0)
    game.score_manager.get_player1_recent_moves.return_value = ["e2-e4", "Nf3"]
    game.score_manager.get_player2_recent_moves.return_value = ["e7-e5", "Nc6"]
    
    # Mock board
    game.board.width = 8
    game.board.height = 8
    
    return game


@pytest.fixture
def cleanup_cv2():
    """Fixture to cleanup OpenCV windows after tests"""
    yield
    try:
        import cv2
        cv2.destroyAllWindows()
    except ImportError:
        pass


@pytest.fixture
def mock_player_dialog():
    """Create a mock PlayerNameDialog for testing"""
    if check_module_available("PlayerNameDialog"):
        try:
            from PlayerNameDialog import PlayerNameDialog
            return PlayerNameDialog()
        except Exception:
            pass
    
    # Return mock if creation fails or not available
    mock = MagicMock()
    mock.window_width = 800
    mock.window_height = 600
    mock.player1_name = ""
    mock.player2_name = ""
    mock.current_input = 1
    mock.is_complete = False
    return mock


# Skip markers for missing dependencies
skip_if_no_cv2 = pytest.mark.skipif(
    not check_module_available("cv2"),
    reason="OpenCV (cv2) not available"
)

skip_if_no_player_dialog = pytest.mark.skipif(
    not check_module_available("PlayerNameDialog"),
    reason="PlayerNameDialog not available"
)

skip_if_no_focus_manager = pytest.mark.skipif(
    not check_module_available("WindowFocusManager"),
    reason="WindowFocusManager not available"  
)

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
