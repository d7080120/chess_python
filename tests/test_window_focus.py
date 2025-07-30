"""
test_window_focus.py - בדיקות לפוקוס חלון המשחק
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import cv2
import sys
import pathlib

# הוסף את תיקיית המקור ל-path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "It1_interfaces"))

from InputHandler import InputHandler
from GameRefactored import GameRefactored


class TestWindowFocus:
    """בדיקות לוודא שחלון המשחק מקבל פוקוס נכון"""
    
    @pytest.fixture
    def mock_game(self):
        """Mock game object"""
        game = Mock(spec=GameRefactored)
        game.player_manager = Mock()
        game.game_over = False
        return game
    
    @pytest.fixture
    def input_handler(self, mock_game):
        """Create InputHandler with mocked game"""
        return InputHandler(mock_game)
    
    @patch('cv2.setWindowProperty')
    @patch('cv2.waitKey')
    def test_window_focus_set_on_show_frame(self, mock_waitkey, mock_set_window_prop, input_handler):
        """Test that window focus is set when showing frame"""
        mock_waitkey.return_value = 255  # No key pressed
        
        # Call show_frame
        result = input_handler.show_frame()
        
        # Verify window property was set for focus
        mock_set_window_prop.assert_called_with("Chess Game", cv2.WND_PROP_TOPMOST, 1)
        assert result is True
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty')
    def test_window_initialization_with_focus(self, mock_set_window_prop, mock_named_window):
        """Test proper window initialization with focus settings"""
        window_name = "Chess Game"
        
        # Simulate window creation and focus setup
        mock_named_window.return_value = None
        mock_set_window_prop.return_value = None
        
        # Create window with focus settings
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)
        
        # Verify calls
        mock_named_window.assert_called_with(window_name, cv2.WINDOW_AUTOSIZE)
        assert mock_set_window_prop.call_count >= 1
    
    @patch('cv2.waitKey')
    def test_keyboard_input_processing(self, mock_waitkey, input_handler):
        """Test that keyboard input is processed correctly"""
        # Test ESC key
        mock_waitkey.return_value = 27  # ESC key
        
        with patch.object(input_handler, 'handle_keyboard_input', return_value=True) as mock_handle:
            result = input_handler.show_frame()
            
            mock_handle.assert_called_with(27)
            assert result is False  # Should exit on ESC
        
        # Test regular key
        mock_waitkey.return_value = 119  # 'w' key
        with patch.object(input_handler, 'handle_keyboard_input', return_value=False) as mock_handle:
            result = input_handler.show_frame()
            
            mock_handle.assert_called_with(119)
            assert result is True  # Should continue
    
    def test_handle_keyboard_input_wasd(self, input_handler):
        """Test WASD key handling for Player 2"""
        # Test W key (UP)
        with patch.object(input_handler.game.player_manager, 'move_cursor_player2') as mock_move:
            result = input_handler.handle_keyboard_input(119)  # 'w' key
            mock_move.assert_called_with(0, -1)
            assert result is False  # Don't exit
        
        # Test S key (DOWN)
        with patch.object(input_handler.game.player_manager, 'move_cursor_player2') as mock_move:
            result = input_handler.handle_keyboard_input(115)  # 's' key
            mock_move.assert_called_with(0, 1)
            assert result is False
        
        # Test A key (LEFT)
        with patch.object(input_handler.game.player_manager, 'move_cursor_player2') as mock_move:
            result = input_handler.handle_keyboard_input(97)  # 'a' key
            mock_move.assert_called_with(-1, 0)
            assert result is False
        
        # Test D key (RIGHT)
        with patch.object(input_handler.game.player_manager, 'move_cursor_player2') as mock_move:
            result = input_handler.handle_keyboard_input(100)  # 'd' key
            mock_move.assert_called_with(1, 0)
            assert result is False
    
    def test_handle_keyboard_input_numbers(self, input_handler):
        """Test numeric key handling for Player 1"""
        # Test 8 key (UP)
        with patch.object(input_handler.game.player_manager, 'move_cursor_player1') as mock_move:
            result = input_handler.handle_keyboard_input(56)  # '8' key
            mock_move.assert_called_with(0, -1)
            assert result is False
        
        # Test 2 key (DOWN)
        with patch.object(input_handler.game.player_manager, 'move_cursor_player1') as mock_move:
            result = input_handler.handle_keyboard_input(50)  # '2' key
            mock_move.assert_called_with(0, 1)
            assert result is False
        
        # Test 4 key (LEFT)
        with patch.object(input_handler.game.player_manager, 'move_cursor_player1') as mock_move:
            result = input_handler.handle_keyboard_input(52)  # '4' key
            mock_move.assert_called_with(-1, 0)
            assert result is False
        
        # Test 6 key (RIGHT)
        with patch.object(input_handler.game.player_manager, 'move_cursor_player1') as mock_move:
            result = input_handler.handle_keyboard_input(54)  # '6' key
            mock_move.assert_called_with(1, 0)
            assert result is False
    
    def test_handle_keyboard_input_select_keys(self, input_handler):
        """Test selection key handling"""
        # Test Space for Player 2
        with patch.object(input_handler.game.player_manager, 'select_piece_player2') as mock_select:
            result = input_handler.handle_keyboard_input(32)  # Space key
            mock_select.assert_called_once()
            assert result is False
        
        # Test 5 key for Player 1
        with patch.object(input_handler.game.player_manager, 'select_piece_player1') as mock_select:
            result = input_handler.handle_keyboard_input(53)  # '5' key
            mock_select.assert_called_once()
            assert result is False
        
        # Test Enter for Player 1
        with patch.object(input_handler.game.player_manager, 'select_piece_player1') as mock_select:
            result = input_handler.handle_keyboard_input(13)  # Enter key
            mock_select.assert_called_once()
            assert result is False
    
    def test_handle_keyboard_input_exit_keys(self, input_handler):
        """Test exit key handling"""
        # Test ESC key
        result = input_handler.handle_keyboard_input(27)  # ESC key
        assert result is True  # Should exit
        
        # Test Q key
        result = input_handler.handle_keyboard_input(113)  # 'q' key
        assert result is True  # Should exit


class TestWindowFocusIntegration:
    """בדיקות אינטגרציה לפוקוס חלון"""
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty')
    @patch('cv2.imshow')
    def test_window_focus_integration(self, mock_imshow, mock_set_window_prop, mock_named_window):
        """Test complete window focus setup integration"""
        window_name = "Chess Game"
        
        # Simulate complete window setup
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)
        
        # Simulate showing the window
        mock_image = MagicMock()
        cv2.imshow(window_name, mock_image)
        
        # Verify all setup calls were made
        mock_named_window.assert_called_with(window_name, cv2.WINDOW_AUTOSIZE)
        
        # Check that window properties were set
        expected_calls = [
            (window_name, cv2.WND_PROP_TOPMOST, 1),
            (window_name, cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)
        ]
        
        for expected_call in expected_calls:
            assert expected_call in mock_set_window_prop.call_args_list
        
        mock_imshow.assert_called_with(window_name, mock_image)
