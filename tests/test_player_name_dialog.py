"""
pytest test for PlayerNameDialog visual improvements
בדיקות לדיאלוג הכנסת שמות השחקנים עם השינויים החזותיים
"""
import pytest
import cv2
import numpy as np
import sys
from pathlib import Path

# Add the It1_interfaces directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "It1_interfaces"))

from PlayerNameDialog import PlayerNameDialog


class TestPlayerNameDialog:
    """Test suite for PlayerNameDialog with visual improvements"""
    
    def setup_method(self):
        """Setup before each test"""
        self.dialog = None
    
    def teardown_method(self):
        """Cleanup after each test"""
        if self.dialog:
            try:
                cv2.destroyAllWindows()
            except:
                pass
    
    def test_dialog_creation(self):
        """Test that PlayerNameDialog can be created successfully"""
        self.dialog = PlayerNameDialog()
        
        assert self.dialog is not None
        assert self.dialog.window_name == "Chess Game - Player Names"
        assert self.dialog.window_width == 800
        assert self.dialog.window_height == 600
        assert self.dialog.player1_name == ""
        assert self.dialog.player2_name == ""
        assert self.dialog.current_input == 1
        assert self.dialog.is_complete == False
    
    def test_background_image_loading(self):
        """Test that background image loads correctly"""
        self.dialog = PlayerNameDialog()
        
        assert self.dialog.background_image is not None
        height, width = self.dialog.background_image.shape[:2]
        assert width == 800
        assert height == 600
        assert len(self.dialog.background_image.shape) == 3  # RGB image
    
    def test_gradient_fallback(self):
        """Test gradient background creation when logo.jpg is not available"""
        self.dialog = PlayerNameDialog()
        gradient = self.dialog._create_gradient_background()
        
        assert gradient is not None
        height, width = gradient.shape[:2]
        assert width == 800
        assert height == 600
        assert len(gradient.shape) == 3  # RGB image
    
    def test_dialog_image_creation(self):
        """Test that dialog image is created successfully"""
        self.dialog = PlayerNameDialog()
        dialog_img = self.dialog._create_dialog_image()
        
        assert dialog_img is not None
        height, width = dialog_img.shape[:2]
        assert width == 800
        assert height == 600
        assert len(dialog_img.shape) == 3  # RGB image
    
    def test_key_handling_esc(self):
        """Test ESC key handling (default names)"""
        self.dialog = PlayerNameDialog()
        
        # Test ESC key (27)
        result = self.dialog._handle_key(27)
        
        assert result == True
        assert self.dialog.player1_name == "Player 1"
        assert self.dialog.player2_name == "Player 2" 
        assert self.dialog.is_complete == True
    
    def test_key_handling_enter(self):
        """Test ENTER key handling (confirm names)"""
        self.dialog = PlayerNameDialog()
        
        # Test ENTER on player 1
        result = self.dialog._handle_key(13)
        assert result == True
        assert self.dialog.current_input == 2
        assert self.dialog.player1_name == "Player 1"  # Default name
        
        # Test ENTER on player 2  
        result = self.dialog._handle_key(13)
        assert result == True
        assert self.dialog.is_complete == True
        assert self.dialog.player2_name == "Player 2"  # Default name
    
    def test_key_handling_backspace(self):
        """Test BACKSPACE key handling"""
        self.dialog = PlayerNameDialog()
        
        # Add some text first
        self.dialog.player1_name = "Test"
        
        # Test BACKSPACE (8)
        result = self.dialog._handle_key(8)
        
        assert result == True
        assert self.dialog.player1_name == "Tes"
    
    def test_key_handling_regular_chars(self):
        """Test regular character input"""
        self.dialog = PlayerNameDialog()
        
        # Test adding character 'A' (65)
        result = self.dialog._handle_key(65)
        
        assert result == True
        assert self.dialog.player1_name == "A"
        
        # Test adding character 'l' (108)
        result = self.dialog._handle_key(108)
        
        assert result == True
        assert self.dialog.player1_name == "Al"
    
    def test_name_length_limit(self):
        """Test that names are limited to 15 characters"""
        self.dialog = PlayerNameDialog()
        
        # Add 15 characters
        for i in range(15):
            self.dialog._handle_key(65)  # 'A'
        
        assert len(self.dialog.player1_name) == 15
        
        # Try to add 16th character
        self.dialog._handle_key(65)
        
        assert len(self.dialog.player1_name) == 15  # Still 15, not 16
    
    def test_visual_elements_properties(self):
        """Test that visual elements have correct properties"""
        self.dialog = PlayerNameDialog()
        
        # Test window properties
        assert self.dialog.window_width == 800
        assert self.dialog.window_height == 600
        
        # Test that background exists
        assert self.dialog.background_image is not None
        
        # Test that dialog image can be created
        img = self.dialog._create_dialog_image()
        assert img is not None
    
    def test_cleanup(self):
        """Test proper cleanup of dialog"""
        self.dialog = PlayerNameDialog()
        
        # Test __del__ method doesn't crash
        try:
            self.dialog.__del__()
        except Exception as e:
            pytest.fail(f"Dialog cleanup failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
