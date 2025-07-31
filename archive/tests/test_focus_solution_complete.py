"""
pytest test for WindowFocusManager and focus solution
בדיקות לפתרון בעיית הפוקוס באמצעות Windows API
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the It1_interfaces directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "It1_interfaces"))

try:
    from WindowFocusManager import WindowFocusManager
    WINDOWS_API_AVAILABLE = True
except ImportError:
    WINDOWS_API_AVAILABLE = False
    WindowFocusManager = None


@pytest.mark.skipif(not WINDOWS_API_AVAILABLE, reason="Windows API not available")
class TestWindowFocusManager:
    """Test suite for WindowFocusManager"""
    
    def setup_method(self):
        """Setup before each test"""
        self.focus_manager = None
    
    def teardown_method(self):
        """Cleanup after each test"""
        if self.focus_manager:
            self.focus_manager = None
    
    def test_focus_manager_creation(self):
        """Test that WindowFocusManager can be created"""
        self.focus_manager = WindowFocusManager()
        
        assert self.focus_manager is not None
        assert hasattr(self.focus_manager, 'user32')
        assert hasattr(self.focus_manager, 'create_focused_window')
        assert hasattr(self.focus_manager, 'ensure_focus')
    
    @patch('cv2.namedWindow')
    @patch('cv2.setWindowProperty')
    def test_create_focused_window(self, mock_set_prop, mock_named_window):
        """Test window creation with focus"""
        self.focus_manager = WindowFocusManager()
        
        result = self.focus_manager.create_focused_window("Test Window")
        
        assert result == True
        mock_named_window.assert_called_once()
        mock_set_prop.assert_called()
    
    def test_window_title_validation(self):
        """Test window title validation"""
        self.focus_manager = WindowFocusManager()
        
        # Test valid title
        result = self.focus_manager._validate_window_title("Valid Title")
        assert result == True
        
        # Test empty title
        result = self.focus_manager._validate_window_title("")
        assert result == False
        
        # Test None title
        result = self.focus_manager._validate_window_title(None)
        assert result == False
    
    @patch('ctypes.windll.user32.FindWindowW')
    def test_find_window(self, mock_find_window):
        """Test finding window by title"""
        self.focus_manager = WindowFocusManager()
        mock_find_window.return_value = 12345  # Mock window handle
        
        result = self.focus_manager._find_window("Test Window")
        
        assert result == 12345
        mock_find_window.assert_called_once_with(None, "Test Window")
    
    @patch('ctypes.windll.user32.SetForegroundWindow')
    @patch('ctypes.windll.user32.FindWindowW')
    def test_ensure_focus_success(self, mock_find_window, mock_set_foreground):
        """Test successful focus setting"""
        self.focus_manager = WindowFocusManager()
        mock_find_window.return_value = 12345
        mock_set_foreground.return_value = True
        
        result = self.focus_manager.ensure_focus("Test Window")
        
        assert result == True
        mock_find_window.assert_called_once()
        mock_set_foreground.assert_called_once_with(12345)
    
    @patch('ctypes.windll.user32.FindWindowW')
    def test_ensure_focus_window_not_found(self, mock_find_window):
        """Test focus when window is not found"""
        self.focus_manager = WindowFocusManager()
        mock_find_window.return_value = 0  # Window not found
        
        result = self.focus_manager.ensure_focus("Non-existent Window")
        
        assert result == False
    
    def test_smart_focus_check(self):
        """Test smart focus checking logic"""
        self.focus_manager = WindowFocusManager()
        
        with patch.object(self.focus_manager, 'ensure_focus') as mock_ensure:
            mock_ensure.return_value = True
            
            result = self.focus_manager.smart_focus_check("Test Window")
            
            assert result == True
            mock_ensure.assert_called_once_with("Test Window")


class TestFocusSolutionIntegration:
    """Integration tests for the complete focus solution"""
    
    def test_focus_solution_imports(self):
        """Test that all focus solution components can be imported"""
        try:
            from WindowFocusManager import WindowFocusManager
            from PlayerNameDialog import PlayerNameDialog  
            from InputHandler import InputHandler
            assert True
        except ImportError as e:
            pytest.fail(f"Focus solution import failed: {e}")
    
    def test_focus_solution_integration_structure(self):
        """Test that focus solution has proper integration structure"""
        if WINDOWS_API_AVAILABLE:
            focus_manager = WindowFocusManager()
            
            # Test that focus manager has required methods
            required_methods = [
                'create_focused_window',
                'ensure_focus', 
                'smart_focus_check',
                '_find_window',
                '_validate_window_title'
            ]
            
            for method in required_methods:
                assert hasattr(focus_manager, method), f"Missing method: {method}"
    
    @pytest.mark.skipif(not WINDOWS_API_AVAILABLE, reason="Windows API not available")
    def test_focus_manager_with_player_dialog(self):
        """Test integration between WindowFocusManager and PlayerNameDialog"""
        try:
            from PlayerNameDialog import PlayerNameDialog
            
            focus_manager = WindowFocusManager()
            dialog = PlayerNameDialog()
            
            # Test that dialog can be created alongside focus manager
            assert focus_manager is not None
            assert dialog is not None
            
            # Cleanup
            try:
                import cv2
                cv2.destroyAllWindows()
            except:
                pass
                
        except ImportError:
            pytest.skip("PlayerNameDialog not available for integration test")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
