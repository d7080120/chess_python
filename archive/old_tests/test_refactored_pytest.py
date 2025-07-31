"""
Test suite for the refactored Game classes using pytest
"""
import pytest
import sys
import pathlib
from unittest.mock import Mock, MagicMock

# הוסף את הנתיב לתיקיית המחלקות
current_dir = pathlib.Path(__file__).parent
sys.path.append(str(current_dir))


class TestPlayerManager:
    """Tests for PlayerManager class"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Create a mock game object
        self.mock_game = Mock()
        self.mock_game.pieces = []
        self.mock_game.user_input_queue = Mock()
        self.mock_game.game_time_ms = Mock(return_value=1000)
        
        # Import and create PlayerManager
        from PlayerManager import PlayerManager
        self.player_manager = PlayerManager(self.mock_game)
    
    def test_initialization(self):
        """Test PlayerManager initialization"""
        assert self.player_manager.game == self.mock_game
        assert self.player_manager.cursor_pos_player1 == [0, 7]
        assert self.player_manager.cursor_pos_player2 == [0, 0]
        assert self.player_manager.selected_piece_player1 is None
        assert self.player_manager.selected_piece_player2 is None
    
    def test_move_cursor_player1(self):
        """Test player 1 cursor movement"""
        # Test normal movement
        self.player_manager.move_cursor_player1(1, 0)
        assert self.player_manager.cursor_pos_player1 == [1, 7]
        
        # Test boundary conditions
        self.player_manager.move_cursor_player1(-2, 0)  # Should stop at 0
        assert self.player_manager.cursor_pos_player1 == [0, 7]
        
        # Test upper boundary
        for _ in range(10):
            self.player_manager.move_cursor_player1(1, 0)
        assert self.player_manager.cursor_pos_player1 == [7, 7]  # Should stop at 7
    
    def test_move_cursor_player2(self):
        """Test player 2 cursor movement"""
        # Test normal movement
        self.player_manager.move_cursor_player2(1, 1)
        assert self.player_manager.cursor_pos_player2 == [1, 1]
        
        # Test boundary conditions
        self.player_manager.move_cursor_player2(-2, -2)  # Should stop at [0, 0]
        assert self.player_manager.cursor_pos_player2 == [0, 0]
    
    def test_is_player_piece(self):
        """Test piece ownership detection"""
        # Create mock pieces
        white_piece = Mock()
        white_piece.piece_id = "PW0"
        
        black_piece = Mock()
        black_piece.piece_id = "PB0"
        
        # Test player 1 (white pieces)
        assert self.player_manager._is_player_piece(white_piece, 1) == True
        assert self.player_manager._is_player_piece(black_piece, 1) == False
        
        # Test player 2 (black pieces)
        assert self.player_manager._is_player_piece(white_piece, 2) == False
        assert self.player_manager._is_player_piece(black_piece, 2) == True


class TestWinChecker:
    """Tests for WinChecker class"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.mock_game = Mock()
        
        from WinChecker import WinChecker
        self.win_checker = WinChecker(self.mock_game)
    
    def test_initialization(self):
        """Test WinChecker initialization"""
        assert self.win_checker.game == self.mock_game
    
    def test_is_win_both_kings_alive(self):
        """Test win condition when both kings are alive"""
        # Create mock pieces with both kings
        white_king = Mock()
        white_king.piece_id = "KW0"
        black_king = Mock()
        black_king.piece_id = "KB0"
        other_piece = Mock()
        other_piece.piece_id = "PW0"
        
        self.mock_game.pieces = [white_king, black_king, other_piece]
        
        assert self.win_checker.is_win() == False
    
    def test_is_win_white_king_missing(self):
        """Test win condition when white king is captured"""
        # Create mock pieces without white king
        black_king = Mock()
        black_king.piece_id = "KB0"
        other_piece = Mock()
        other_piece.piece_id = "PW0"
        
        self.mock_game.pieces = [black_king, other_piece]
        
        assert self.win_checker.is_win() == True
    
    def test_is_win_black_king_missing(self):
        """Test win condition when black king is captured"""
        # Create mock pieces without black king
        white_king = Mock()
        white_king.piece_id = "KW0"
        other_piece = Mock()
        other_piece.piece_id = "PB0"
        
        self.mock_game.pieces = [white_king, other_piece]
        
        assert self.win_checker.is_win() == True


class TestMoveValidator:
    """Tests for MoveValidator class"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.mock_game = Mock()
        self.mock_game.pieces = []
        self.mock_game.user_input_queue = Mock()
        self.mock_game.game_time_ms = Mock(return_value=1000)
        
        from MoveValidator import MoveValidator
        self.move_validator = MoveValidator(self.mock_game)
    
    def test_initialization(self):
        """Test MoveValidator initialization"""
        assert self.move_validator.game == self.mock_game
    
    def test_get_piece_position_with_physics(self):
        """Test getting piece position from physics state"""
        # Create mock piece with physics state
        mock_piece = Mock()
        mock_piece._state = Mock()
        mock_piece._state._physics = Mock()
        mock_piece._state._physics.cell = (3, 4)
        
        position = self.move_validator._get_piece_position(mock_piece)
        assert position == (3, 4)
    
    def test_get_piece_position_with_xy(self):
        """Test getting piece position from x,y attributes"""
        # Create mock piece with x,y attributes
        mock_piece = Mock()
        del mock_piece._state  # Remove _state to test fallback
        mock_piece.x = 2
        mock_piece.y = 5
        
        position = self.move_validator._get_piece_position(mock_piece)
        assert position == (2, 5)
    
    def test_get_piece_position_none(self):
        """Test getting piece position when no position data available"""
        mock_piece = Mock()
        del mock_piece._state
        del mock_piece.x
        del mock_piece.y
        del mock_piece.board_position
        
        position = self.move_validator._get_piece_position(mock_piece)
        assert position is None
    
    def test_is_player_piece(self):
        """Test player piece identification"""
        white_piece = Mock()
        white_piece.piece_id = "QW0"
        
        black_piece = Mock()
        black_piece.piece_id = "QB0"
        
        # Test player 1 (white)
        assert self.move_validator._is_player_piece(white_piece, 1) == True
        assert self.move_validator._is_player_piece(black_piece, 1) == False
        
        # Test player 2 (black)
        assert self.move_validator._is_player_piece(white_piece, 2) == False
        assert self.move_validator._is_player_piece(black_piece, 2) == True


class TestCaptureHandler:
    """Tests for CaptureHandler class"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.mock_game = Mock()
        self.mock_game.pieces = []
        self.mock_game.win_checker = Mock()
        self.mock_game.win_checker.is_win = Mock(return_value=False)
        
        from CaptureHandler import CaptureHandler
        self.capture_handler = CaptureHandler(self.mock_game)
    
    def test_initialization(self):
        """Test CaptureHandler initialization"""
        assert self.capture_handler.game == self.mock_game
    
    def test_check_pawn_promotion_not_pawn(self):
        """Test pawn promotion check with non-pawn piece"""
        mock_piece = Mock()
        mock_piece.piece_id = "QW0"  # Not a pawn
        
        # Should not do anything for non-pawn pieces
        result = self.capture_handler._check_pawn_promotion(mock_piece, (4, 0))
        assert result is None  # Should return None and not crash


if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])
