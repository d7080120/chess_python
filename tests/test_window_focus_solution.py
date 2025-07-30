"""
test_window_focus_solution.py - טסטים לפתרון הפוקוס החדש
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import pathlib

# הוסף את תיקיית המקור ל-path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "It1_interfaces"))

from WindowFocusManager import WindowFocusManager
from PlayerNameDialog import PlayerNameDialog


class TestWindowFocusManager:
    """טסטים למנהל הפוקוס החדש"""
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty')
    @patch('cv2.moveWindow')
    def test_window_focus_manager_creation(self, mock_move, mock_prop, mock_window):
        """Test WindowFocusManager creation"""
        manager = WindowFocusManager("Test Window")
        
        assert manager.window_name == "Test Window"
        assert manager.focus_attempts == 0
        assert manager.max_focus_attempts == 3
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty')
    @patch('cv2.moveWindow')
    def test_create_focused_window(self, mock_move, mock_prop, mock_window):
        """Test focused window creation"""
        manager = WindowFocusManager()
        result = manager.create_focused_window()
        
        assert result is True
        mock_window.assert_called_once()
        mock_prop.assert_called()
        mock_move.assert_called_once()
    
    def test_smart_focus_check_tracking(self):
        """Test that focus attempts are tracked correctly"""
        with patch('cv2.namedWindow'), patch('cv2.setWindowProperty'), patch('cv2.moveWindow'):
            manager = WindowFocusManager()
            
            # מדמה שהפוקוס לא עובד
            with patch.object(manager, 'is_window_focused', return_value=False):
                with patch.object(manager, 'ensure_focus', return_value=True):
                    manager.smart_focus_check()
                    assert manager.focus_attempts == 1
                    
                    manager.smart_focus_check()
                    assert manager.focus_attempts == 2


class TestPlayerNameDialog:
    """טסטים לדיאלוג שמות השחקנים"""
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty')
    @patch('cv2.moveWindow')
    def test_dialog_creation(self, mock_move, mock_prop, mock_window):
        """Test dialog creation"""
        dialog = PlayerNameDialog("Test Dialog")
        
        assert dialog.window_name == "Test Dialog"
        assert dialog.player1_name == ""
        assert dialog.player2_name == ""
        assert dialog.current_input == 1
        assert dialog.is_complete is False
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty') 
    @patch('cv2.moveWindow')
    def test_handle_key_regular_chars(self, mock_move, mock_prop, mock_window):
        """Test handling regular character input"""
        dialog = PlayerNameDialog()
        
        # מוסיף תו לשחקן 1
        result = dialog._handle_key(65)  # 'A'
        assert result is True
        assert dialog.player1_name == "A"
        
        # מוסיף עוד תו
        dialog._handle_key(66)  # 'B'
        assert dialog.player1_name == "AB"
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty')
    @patch('cv2.moveWindow')
    def test_handle_key_backspace(self, mock_move, mock_prop, mock_window):
        """Test backspace functionality"""
        dialog = PlayerNameDialog()
        dialog.player1_name = "Test"
        
        result = dialog._handle_key(8)  # Backspace
        assert result is True
        assert dialog.player1_name == "Tes"
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty')
    @patch('cv2.moveWindow')
    def test_handle_key_enter_progression(self, mock_move, mock_prop, mock_window):
        """Test Enter key progresses through inputs"""
        dialog = PlayerNameDialog()
        dialog.player1_name = "Player1"
        
        # Enter על שחקן 1 - עובר לשחקן 2
        result = dialog._handle_key(13)  # Enter
        assert result is True
        assert dialog.current_input == 2
        assert dialog.is_complete is False
        
        # Enter על שחקן 2 - מסיים
        dialog.player2_name = "Player2"
        result = dialog._handle_key(13)  # Enter
        assert result is True
        assert dialog.is_complete is True
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty')
    @patch('cv2.moveWindow')
    def test_handle_key_escape_defaults(self, mock_move, mock_prop, mock_window):
        """Test ESC key sets default names"""
        dialog = PlayerNameDialog()
        
        result = dialog._handle_key(27)  # ESC
        assert result is True
        assert dialog.player1_name == "Player 1"
        assert dialog.player2_name == "Player 2"
        assert dialog.is_complete is True
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty')
    @patch('cv2.moveWindow')
    def test_name_length_limit(self, mock_move, mock_prop, mock_window):
        """Test name length is limited"""
        dialog = PlayerNameDialog()
        
        # מוסיף 16 תווים (מעבר לגבול)
        for i in range(16):
            dialog._handle_key(65)  # 'A'
        
        # צריך להיות רק 15 תווים
        assert len(dialog.player1_name) == 15
        assert dialog.player1_name == "A" * 15


class TestPlayerNameDialogIntegration:
    """טסטי אינטגרציה לדיאלוג"""
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty')
    @patch('cv2.moveWindow')
    @patch('cv2.destroyWindow')
    @patch('cv2.imshow')
    @patch('cv2.waitKey')
    def test_complete_dialog_flow(self, mock_waitkey, mock_imshow, mock_destroy, 
                                  mock_move, mock_prop, mock_window):
        """Test complete dialog interaction flow"""
        dialog = PlayerNameDialog()
        
        # מדמה רצף מקשים: "Bob" + Enter + "Alice" + Enter
        key_sequence = [
            66, 111, 98,  # "Bob"
            13,           # Enter
            65, 108, 105, 99, 101,  # "Alice"
            13            # Enter
        ]
        
        mock_waitkey.side_effect = key_sequence + [255] * 10  # מספיק 255 לסיום
        
        names = dialog.get_player_names()
        
        assert names == ("Bob", "Alice")
        mock_destroy.assert_called_once()
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty')
    @patch('cv2.moveWindow')
    @patch('cv2.destroyWindow')
    @patch('cv2.imshow')
    @patch('cv2.waitKey')
    def test_dialog_with_empty_names(self, mock_waitkey, mock_imshow, mock_destroy,
                                     mock_move, mock_prop, mock_window):
        """Test dialog with empty names uses defaults"""
        dialog = PlayerNameDialog()
        
        # מדמה רצף: Enter + Enter (שמות ריקים)
        key_sequence = [13, 13]  # Enter, Enter
        mock_waitkey.side_effect = key_sequence + [255] * 10
        
        names = dialog.get_player_names()
        
        assert names == ("Player 1", "Player 2")
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty')
    @patch('cv2.moveWindow')
    @patch('cv2.destroyWindow')
    @patch('cv2.imshow')
    @patch('cv2.waitKey')
    def test_dialog_with_escape(self, mock_waitkey, mock_imshow, mock_destroy,
                                mock_move, mock_prop, mock_window):
        """Test dialog with ESC key"""
        dialog = PlayerNameDialog()
        
        # מדמה ESC
        mock_waitkey.side_effect = [27] + [255] * 10  # ESC
        
        names = dialog.get_player_names()
        
        assert names == ("Player 1", "Player 2")
