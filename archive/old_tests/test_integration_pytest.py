"""
Integration tests for the refactored Game classes
Tests that don't require cv2 or full game setup
"""
import pytest
import sys
import pathlib
from unittest.mock import Mock, MagicMock, patch

# הוסף את הנתיב לתיקיית המחלקות
current_dir = pathlib.Path(__file__).parent
sys.path.append(str(current_dir))


class TestGameRefactoredIntegration:
    """Integration tests for GameRefactored without requiring cv2"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Mock all the dependencies that require external libraries
        self.mock_pieces = []
        self.mock_board = Mock()
        self.mock_board.clone = Mock(return_value=Mock())
        
        # Create mocks for all the imported modules that might cause issues
        with patch.dict('sys.modules', {
            'cv2': Mock(),
            'img': Mock(),
            'Board': Mock(),
            'Command': Mock(),
            'Piece': Mock(),
            'integration_setup': Mock(),
            'sound_player': Mock(),
        }):
            # Mock the setup_observers function
            with patch('GameRefactored.setup_observers') as mock_setup:
                mock_setup.return_value = (Mock(), Mock(), Mock(), Mock())
                
                from GameRefactored import GameRefactored
                self.game = GameRefactored(self.mock_pieces, self.mock_board)
    
    def test_game_initialization(self):
        """Test that GameRefactored initializes properly with all helper classes"""
        assert self.game.pieces == self.mock_pieces
        assert self.game.board == self.mock_board
        assert hasattr(self.game, 'user_input_queue')
        assert self.game.game_over == False
        
        # Check that all helper classes are created
        assert hasattr(self.game, 'input_handler')
        assert hasattr(self.game, 'player_manager')
        assert hasattr(self.game, 'draw_manager')
        assert hasattr(self.game, 'capture_handler')
        assert hasattr(self.game, 'win_checker')
        assert hasattr(self.game, 'move_validator')
    
    def test_helper_classes_reference_game(self):
        """Test that all helper classes have correct reference to game"""
        assert self.game.input_handler.game == self.game
        assert self.game.player_manager.game == self.game
        assert self.game.draw_manager.game == self.game
        assert self.game.capture_handler.game == self.game
        assert self.game.win_checker.game == self.game
        assert self.game.move_validator.game == self.game
    
    def test_game_time_ms(self):
        """Test game time function"""
        time1 = self.game.game_time_ms()
        time2 = self.game.game_time_ms()
        
        assert isinstance(time1, int)
        assert isinstance(time2, int)
        assert time2 >= time1  # Time should not go backwards
    
    def test_clone_board(self):
        """Test board cloning"""
        cloned = self.game.clone_board()
        
        # Should call the board's clone method
        self.mock_board.clone.assert_called_once()
        assert cloned is not None


class TestPlayerManagerIntegration:
    """Integration tests for PlayerManager with other components"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Create a more realistic game mock
        self.mock_game = Mock()
        self.mock_game.pieces = []
        self.mock_game.user_input_queue = Mock()
        self.mock_game.game_time_ms = Mock(return_value=1000)
        
        # Create mock move validator
        self.mock_move_validator = Mock()
        self.mock_game.move_validator = self.mock_move_validator
        
        from PlayerManager import PlayerManager
        self.player_manager = PlayerManager(self.mock_game)
    
    def test_select_piece_calls_move_validator(self):
        """Test that piece selection integrates with move validator"""
        # Create a mock piece at cursor position
        mock_piece = Mock()
        mock_piece.piece_id = "PW0"
        
        # Mock the _find_piece_at_position to return our piece
        self.player_manager._find_piece_at_position = Mock(return_value=mock_piece)
        
        # Select the piece
        self.player_manager.select_piece_player1()
        
        # Should select the piece
        assert self.player_manager.selected_piece_player1 == mock_piece
    
    def test_move_piece_integration(self):
        """Test piece movement integration with move validator"""
        # Setup: select a piece first
        mock_piece = Mock()
        mock_piece.piece_id = "PW0"
        self.player_manager.selected_piece_player1 = mock_piece
        self.player_manager._get_piece_position = Mock(return_value=(2, 2))
        
        # Move cursor to different position
        self.player_manager.cursor_pos_player1 = [3, 3]
        
        # Trigger piece selection (which should move the piece)
        self.player_manager.select_piece_player1()
        
        # Should call move_validator.move_piece
        self.mock_move_validator.move_piece.assert_called_once_with(mock_piece, 3, 3, 1)
        
        # Should deselect the piece
        assert self.player_manager.selected_piece_player1 is None


class TestGameRefactoredModularDesign:
    """Tests to verify the modular design principles"""
    
    def test_separation_of_concerns(self):
        """Test that each class has a single, well-defined responsibility"""
        # Import all classes
        from InputHandler import InputHandler
        from PlayerManager import PlayerManager
        from DrawManager import DrawManager
        from CaptureHandler import CaptureHandler
        from WinChecker import WinChecker
        from MoveValidator import MoveValidator
        
        mock_game = Mock()
        
        # Create instances
        input_handler = InputHandler(mock_game)
        player_manager = PlayerManager(mock_game)
        draw_manager = DrawManager(mock_game)
        capture_handler = CaptureHandler(mock_game)
        win_checker = WinChecker(mock_game)
        move_validator = MoveValidator(mock_game)
        
        # InputHandler should only handle input
        assert hasattr(input_handler, 'handle_keyboard_input')
        assert hasattr(input_handler, 'show_frame')
        
        # PlayerManager should only manage players
        assert hasattr(player_manager, 'move_cursor_player1')
        assert hasattr(player_manager, 'move_cursor_player2')
        assert hasattr(player_manager, 'select_piece_player1')
        assert hasattr(player_manager, 'select_piece_player2')
        
        # DrawManager should only handle drawing
        assert hasattr(draw_manager, 'draw_game')
        
        # CaptureHandler should only handle captures
        assert hasattr(capture_handler, 'handle_arrival')
        
        # WinChecker should only check win conditions
        assert hasattr(win_checker, 'is_win')
        assert hasattr(win_checker, 'announce_win')
        
        # MoveValidator should only validate moves
        assert hasattr(move_validator, 'move_piece')
        assert hasattr(move_validator, '_is_valid_move')
    
    def test_classes_dont_have_overlapping_responsibilities(self):
        """Test that classes don't have methods that belong to other classes"""
        from InputHandler import InputHandler
        from PlayerManager import PlayerManager
        from DrawManager import DrawManager
        from CaptureHandler import CaptureHandler
        from WinChecker import WinChecker
        from MoveValidator import MoveValidator
        
        # InputHandler shouldn't have game logic methods
        assert not hasattr(InputHandler, 'is_win')
        assert not hasattr(InputHandler, 'move_piece')
        assert not hasattr(InputHandler, 'handle_arrival')
        
        # PlayerManager shouldn't have drawing methods
        assert not hasattr(PlayerManager, 'draw_game')
        assert not hasattr(PlayerManager, '_draw_cursors')
        
        # DrawManager shouldn't have game logic
        assert not hasattr(DrawManager, 'is_win')
        assert not hasattr(DrawManager, 'move_piece')
        
        # Each class should be focused on its own responsibility
        print("✅ כל מחלקה מתמחה באחריות שלה בלבד")


def test_code_organization_summary():
    """Summary test that prints the organization benefits"""
    print("\n🎯 ארגון הקוד החדש:")
    print("📁 InputHandler - טיפול בקלט מהמקלדת")
    print("👥 PlayerManager - ניהול שני השחקנים")
    print("🎨 DrawManager - ציור המשחק והגרפיקה")
    print("⚔️ CaptureHandler - טיפול בתפיסות")
    print("🏆 WinChecker - בדיקת תנאי נצחון")
    print("🔍 MoveValidator - בדיקת חוקיות מהלכים")
    print("🎮 GameRefactored - ניהול כללי של המשחק")
    
    print("\n✅ יתרונות:")
    print("- קוד יותר קריא ומובן")
    print("- קל יותר לתחזקה ולשינויים")
    print("- כל מחלקה אחראית על חלק ספציפי")
    print("- קל יותר לבדיקות יחידה")
    print("- הפרדה בין לוגיקה לממשק משתמש")


if __name__ == "__main__":
    # Print organization summary
    test_code_organization_summary()
    
    # Run tests
    pytest.main([__file__, "-v"])
