"""
pytest test for visual improvements in DrawManager
בדיקות לשינויים החזותיים בניהול התצוגה
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the It1_interfaces directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "It1_interfaces"))


class TestDrawManagerVisualImprovements:
    """Test suite for DrawManager visual improvements"""
    
    def setup_method(self):
        """Setup before each test"""
        self.draw_manager = None
        self.mock_game = None
    
    def teardown_method(self):
        """Cleanup after each test"""
        self.draw_manager = None
        self.mock_game = None
    
    def test_draw_manager_import(self):
        """Test that DrawManager can be imported"""
        try:
            from DrawManager import DrawManager
            assert DrawManager is not None
        except ImportError as e:
            pytest.fail(f"DrawManager import failed: {e}")
    
    def test_font_improvements_structure(self):
        """Test that DrawManager has the expected font improvement structure"""
        try:
            from DrawManager import DrawManager
            import cv2
            
            # Create mock game
            mock_game = MagicMock()
            mock_game.player_name_manager.get_player1_name.return_value = "Player 1"
            mock_game.player_name_manager.get_player2_name.return_value = "Player 2"
            mock_game.score_manager.get_scores.return_value = (0, 0)
            mock_game.score_manager.get_player1_recent_moves.return_value = ["e2-e4", "Nf3"]
            mock_game.score_manager.get_player2_recent_moves.return_value = ["e7-e5", "Nc6"]
            
            draw_manager = DrawManager(mock_game)
            
            # Test that DrawManager has required methods
            required_methods = [
                'render_board_with_panels',
                '_create_background',
                '_draw_left_panel',
                '_draw_right_panel'
            ]
            
            for method in required_methods:
                assert hasattr(draw_manager, method), f"Missing method: {method}"
                
        except ImportError:
            pytest.skip("DrawManager not available for testing")
    
    def test_background_creation(self):
        """Test background creation functionality"""
        try:
            from DrawManager import DrawManager
            import numpy as np
            
            mock_game = MagicMock()
            draw_manager = DrawManager(mock_game)
            
            # Test background creation
            background = draw_manager._create_background(800, 600)
            
            assert background is not None
            assert background.shape == (600, 800, 3)  # height, width, channels
            assert background.dtype == np.uint8
            
        except ImportError:
            pytest.skip("DrawManager not available for testing")
    
    def test_font_constants_usage(self):
        """Test that improved fonts are used in the code"""
        try:
            import inspect
            from DrawManager import DrawManager
            
            # Get the source code of DrawManager
            source = inspect.getsource(DrawManager)
            
            # Check that FONT_HERSHEY_DUPLEX is used (improved font)
            assert "FONT_HERSHEY_DUPLEX" in source, "FONT_HERSHEY_DUPLEX not found in DrawManager"
            
            # Check that font improvements are documented
            assert "גופן מעוצב" in source or "מעוצבת יותר" in source, "Font improvement comments not found"
            
        except ImportError:
            pytest.skip("DrawManager not available for font testing")
    
    @patch('cv2.imread')
    def test_background_loading_with_fallback(self, mock_imread):
        """Test background loading with fallback"""
        try:
            from DrawManager import DrawManager
            import numpy as np
            
            # Mock failed image loading
            mock_imread.return_value = None
            
            mock_game = MagicMock()
            draw_manager = DrawManager(mock_game)
            
            # Test fallback background creation
            background = draw_manager._create_background(800, 600)
            
            assert background is not None
            assert background.shape == (600, 800, 3)
            # Should be dark gray fallback
            assert np.all(background == (40, 40, 40))
            
        except ImportError:
            pytest.skip("DrawManager not available for background testing")
    
    def test_panel_drawing_structure(self):
        """Test that panel drawing methods exist and work"""
        try:
            from DrawManager import DrawManager
            import numpy as np
            
            mock_game = MagicMock()
            mock_game.player_name_manager.get_player1_name.return_value = "Alice"
            mock_game.player_name_manager.get_player2_name.return_value = "Bob"
            mock_game.score_manager.get_scores.return_value = (5, 3)
            mock_game.score_manager.get_player1_recent_moves.return_value = ["e2-e4"]
            mock_game.score_manager.get_player2_recent_moves.return_value = ["e7-e5"]
            
            draw_manager = DrawManager(mock_game)
            
            # Create test image
            test_img = np.zeros((600, 800, 3), dtype=np.uint8)
            
            # Test panel drawing methods exist and can be called
            try:
                draw_manager._draw_left_panel(test_img, 0, 300, 600)
                draw_manager._draw_right_panel(test_img, 500, 300, 600)
            except Exception as e:
                pytest.fail(f"Panel drawing failed: {e}")
                
        except ImportError:
            pytest.skip("DrawManager not available for panel testing")


class TestVisualImprovementsIntegration:
    """Integration tests for all visual improvements"""
    
    def test_all_visual_components_import(self):
        """Test that all visual improvement components can be imported"""
        components = [
            "PlayerNameDialog",
            "DrawManager", 
            "PlayerNameManager"
        ]
        
        for component in components:
            try:
                exec(f"from {component} import {component}")
            except ImportError as e:
                pytest.fail(f"Visual component {component} import failed: {e}")
    
    def test_visual_improvements_constants(self):
        """Test that visual improvements use better constants"""
        try:
            from PlayerNameDialog import PlayerNameDialog
            
            dialog = PlayerNameDialog()
            
            # Test improved window dimensions
            assert dialog.window_width == 800, "Window width not upgraded to 800"
            assert dialog.window_height == 600, "Window height not upgraded to 600"
            
        except ImportError:
            pytest.skip("PlayerNameDialog not available for constants testing")
    
    def test_background_image_support(self):
        """Test that background image support works"""
        try:
            from PlayerNameDialog import PlayerNameDialog
            
            dialog = PlayerNameDialog()
            
            # Test background image loading method exists
            assert hasattr(dialog, '_load_background_image')
            assert hasattr(dialog, '_create_gradient_background')
            
            # Test background is loaded
            assert dialog.background_image is not None
            
        except ImportError:
            pytest.skip("PlayerNameDialog not available for background testing")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
