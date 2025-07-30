"""
test_focus_solution.py - בדיקת הפתרון לפוקוס אוטומטי
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import pathlib

# הוסף את תיקיית המקור ל-path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "It1_interfaces"))

# Mock Windows API imports before importing InputHandler
with patch.dict('sys.modules', {
    'ctypes': MagicMock(),
    'ctypes.wintypes': MagicMock(),
}):
    from InputHandler import InputHandler


class TestFocusSolution:
    """בדיקות לפתרון הפוקוס האוטומטי"""
    
    @pytest.fixture
    def mock_game(self):
        """Mock game object"""
        game = Mock()
        game.player_manager = Mock()
        return game
    
    @patch('InputHandler.platform.system')
    @patch('InputHandler.cv2.namedWindow')
    @patch('InputHandler.cv2.setWindowProperty')
    @patch('InputHandler.cv2.moveWindow')
    def test_input_handler_initialization(self, mock_move, mock_set_prop, mock_named, mock_platform, mock_game):
        """Test that InputHandler initializes with focus setup"""
        mock_platform.return_value = "Windows"
        
        # Create InputHandler
        handler = InputHandler(mock_game)
        
        # Verify window was created
        mock_named.assert_called_with("Chess Game", 1)  # cv2.WINDOW_AUTOSIZE
        
        # Verify initial focus attempts
        assert handler.focus_attempts == 0
        assert handler.max_focus_attempts == 5
        assert handler.window_name == "Chess Game"
    
    @patch('InputHandler.WINDOWS_API_AVAILABLE', True)
    @patch('InputHandler.cv2.namedWindow')
    @patch('InputHandler.cv2.setWindowProperty')
    def test_windows_api_setup(self, mock_set_prop, mock_named, mock_game):
        """Test Windows API setup when available"""
        with patch('InputHandler.ctypes') as mock_ctypes:
            mock_ctypes.windll.user32 = Mock()
            
            handler = InputHandler(mock_game)
            
            # Verify Windows API functions were set up
            assert hasattr(handler, 'FindWindow')
            assert hasattr(handler, 'SetForegroundWindow')
            assert hasattr(handler, 'ShowWindow')
            assert hasattr(handler, 'SetFocus')
    
    @patch('InputHandler.cv2.waitKey')
    @patch('InputHandler.cv2.setWindowProperty')
    def test_show_frame_with_focus(self, mock_set_prop, mock_waitkey, mock_game):
        """Test show_frame method handles focus automatically"""
        handler = InputHandler(mock_game)
        handler.focus_attempts = 0  # Reset for test
        
        mock_waitkey.return_value = 255  # No key pressed
        
        # Call show_frame
        result = handler.show_frame()
        
        # Should continue (not exit)
        assert result is True
        
        # Focus attempts should increase (called _force_window_focus)
        assert handler.focus_attempts > 0
    
    @patch('InputHandler.cv2.waitKey')
    @patch('InputHandler.time.time')
    def test_focus_throttling(self, mock_time, mock_waitkey, mock_game):
        """Test that focus attempts are throttled"""
        handler = InputHandler(mock_game)
        
        # Mock time to simulate rapid calls
        mock_time.side_effect = [0.0, 0.1, 0.2, 0.3]  # Within throttle window
        mock_waitkey.return_value = 255
        
        # Call show_frame multiple times rapidly
        handler.show_frame()
        initial_attempts = handler.focus_attempts
        
        handler.show_frame()  # Should be throttled
        
        # Focus attempts shouldn't increase due to throttling
        assert handler.focus_attempts == initial_attempts
    
    @patch('InputHandler.cv2.waitKey')
    def test_focus_stops_after_successful_input(self, mock_waitkey, mock_game):
        """Test that focus attempts stop after successful keyboard input"""
        handler = InputHandler(mock_game)
        handler.focus_attempts = 2  # Partially through attempts
        
        # Simulate key press
        mock_waitkey.return_value = 119  # 'w' key
        
        with patch.object(handler, 'handle_keyboard_input', return_value=False):
            result = handler.show_frame()
        
        # Should stop focus attempts after successful input
        assert handler.focus_attempts == handler.max_focus_attempts
        assert result is True
    
    @patch('InputHandler.WINDOWS_API_AVAILABLE', True)
    @patch('InputHandler.cv2.setWindowProperty')
    @patch('InputHandler.time.time')
    def test_windows_force_focus(self, mock_time, mock_set_prop, mock_game):
        """Test Windows API force focus method"""
        mock_time.return_value = 1.0
        
        handler = InputHandler(mock_game)
        handler.last_focus_time = 0.0  # Ensure throttle passes
        
        # Mock Windows API
        handler.FindWindow = Mock(return_value=12345)  # Mock window handle
        handler.ShowWindow = Mock(return_value=True)
        handler.SetForegroundWindow = Mock(return_value=True)
        handler.SetFocus = Mock(return_value=12345)
        
        # Call force focus
        handler._force_window_focus()
        
        # Verify Windows API calls
        handler.FindWindow.assert_called_once()
        handler.ShowWindow.assert_called_with(12345, 9)  # SW_RESTORE
        handler.SetForegroundWindow.assert_called_with(12345)
        handler.SetFocus.assert_called_with(12345)
    
    def test_focus_max_attempts_respected(self, mock_game):
        """Test that focus attempts respect maximum limit"""
        handler = InputHandler(mock_game)
        handler.focus_attempts = handler.max_focus_attempts
        
        with patch.object(handler, '_windows_force_focus') as mock_windows_focus:
            handler._force_window_focus()
            
            # Should not attempt focus after max attempts reached
            mock_windows_focus.assert_not_called()
    
    @patch('InputHandler.cv2.namedWindow')
    @patch('InputHandler.cv2.imshow')
    @patch('InputHandler.cv2.waitKey')
    @patch('InputHandler.np.zeros')
    def test_dummy_image_refresh(self, mock_zeros, mock_waitkey_inner, mock_imshow, mock_named, mock_game):
        """Test that dummy image is used for window refresh"""
        mock_zeros.return_value = "dummy_image"
        mock_waitkey_inner.return_value = -1
        
        handler = InputHandler(mock_game)
        handler.last_focus_time = 0.0
        
        with patch('InputHandler.time.time', return_value=1.0):
            handler._force_window_focus()
        
        # Verify dummy image was shown
        mock_zeros.assert_called_with((100, 100, 3), dtype="uint8")
        mock_imshow.assert_called_with("Chess Game", "dummy_image")


class TestIntegrationWithGame:
    """בדיקות אינטגרציה עם המשחק"""
    
    @patch('InputHandler.cv2.namedWindow')
    @patch('InputHandler.cv2.setWindowProperty')
    def test_game_integration(self, mock_set_prop, mock_named, mock_game):
        """Test integration with game object"""
        handler = InputHandler(mock_game)
        
        # Verify game reference is stored
        assert handler.game == mock_game
        
        # Verify window setup
        mock_named.assert_called_once()
        assert mock_set_prop.call_count >= 1
