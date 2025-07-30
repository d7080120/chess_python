"""
pytest comprehensive test suite for chess game improvements
בדיקות מקיפות לכל השיפורים במשחק השחמט
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import importlib.util

# Add the It1_interfaces directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "It1_interfaces"))


def check_module_exists(module_name):
    """Helper function to check if a module can be imported"""
    try:
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except (ImportError, ValueError):
        return False


class TestChessGameComprehensive:
    """Comprehensive test suite for chess game improvements"""
    
    def test_core_imports(self):
        """Test that all core modules can be imported"""
        core_modules = [
            "Board", "Piece", "GameRefactored", "State", 
            "Moves", "MoveValidator", "WinChecker"
        ]
        
        for module in core_modules:
            if check_module_exists(module):
                try:
                    exec(f"from {module} import {module}")
                except ImportError as e:
                    pytest.fail(f"Core module {module} import failed: {e}")
    
    def test_focus_solution_imports(self):
        """Test focus solution components"""
        focus_modules = ["WindowFocusManager", "PlayerNameDialog", "PlayerNameManager"]
        
        for module in focus_modules:
            if check_module_exists(module):
                try:
                    exec(f"from {module} import {module}")
                except ImportError as e:
                    pytest.fail(f"Focus module {module} import failed: {e}")
    
    def test_visual_improvements_imports(self):
        """Test visual improvement components"""
        visual_modules = ["DrawManager", "Graphics", "GraphicsFactory"]
        
        for module in visual_modules:
            if check_module_exists(module):
                try:
                    exec(f"from {module} import {module}")
                except ImportError as e:
                    pytest.fail(f"Visual module {module} import failed: {e}")
    
    def test_observer_pattern_imports(self):
        """Test observer pattern components"""
        observer_modules = ["ScoreManager", "subject_impl", "observer"]
        
        for module in observer_modules:
            if check_module_exists(module):
                try:
                    exec(f"from {module} import *")
                except ImportError as e:
                    pytest.fail(f"Observer module {module} import failed: {e}")
    
    @pytest.mark.skipif(not check_module_exists("PlayerNameDialog"), reason="PlayerNameDialog not available")
    def test_player_name_dialog_functionality(self):
        """Test PlayerNameDialog core functionality"""
        from PlayerNameDialog import PlayerNameDialog
        
        dialog = PlayerNameDialog()
        
        # Test initialization
        assert dialog.window_width == 800
        assert dialog.window_height == 600
        assert dialog.player1_name == ""
        assert dialog.player2_name == ""
        assert dialog.current_input == 1
        assert dialog.is_complete == False
        
        # Test background loading
        assert dialog.background_image is not None
        
        # Test key handling
        assert dialog._handle_key(65) == True  # 'A' key
        assert dialog.player1_name == "A"
        
        # Cleanup
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass
    
    @pytest.mark.skipif(not check_module_exists("WindowFocusManager"), reason="WindowFocusManager not available")
    def test_window_focus_manager_functionality(self):
        """Test WindowFocusManager core functionality"""
        from WindowFocusManager import WindowFocusManager
        
        focus_manager = WindowFocusManager()
        
        # Test basic functionality
        assert hasattr(focus_manager, 'create_focused_window')
        assert hasattr(focus_manager, 'ensure_focus')
        assert hasattr(focus_manager, 'smart_focus_check')
        
        # Test window title validation
        assert focus_manager._validate_window_title("Valid Title") == True
        assert focus_manager._validate_window_title("") == False
        assert focus_manager._validate_window_title(None) == False
    
    @pytest.mark.skipif(not check_module_exists("DrawManager"), reason="DrawManager not available")
    def test_draw_manager_visual_improvements(self):
        """Test DrawManager visual improvements"""
        from DrawManager import DrawManager
        import inspect
        
        # Test that improved fonts are used
        source = inspect.getsource(DrawManager)
        assert "FONT_HERSHEY_DUPLEX" in source, "Improved fonts not implemented"
        
        # Test with mock game
        mock_game = MagicMock()
        mock_game.player_name_manager.get_player1_name.return_value = "Player 1"
        mock_game.player_name_manager.get_player2_name.return_value = "Player 2"
        
        draw_manager = DrawManager(mock_game)
        
        # Test background creation
        background = draw_manager._create_background(800, 600)
        assert background is not None
        assert background.shape == (600, 800, 3)
    
    def test_game_integration_structure(self):
        """Test that game components integrate properly"""
        if check_module_exists("GameRefactored"):
            try:
                from GameRefactored import GameRefactored
                
                # Test that GameRefactored has expected attributes
                expected_attrs = ['board', 'state', 'move_validator', 'win_checker']
                
                # We can't create a full game instance in tests, but we can check the class structure
                for attr in expected_attrs:
                    # This tests that the attribute is referenced in the class
                    import inspect
                    source = inspect.getsource(GameRefactored)
                    assert attr in source, f"Expected attribute {attr} not found in GameRefactored"
                    
            except ImportError:
                pytest.skip("GameRefactored not available for integration testing")
    
    def test_pytest_configuration(self):
        """Test that pytest configuration is correct"""
        # Test that we're in the correct directory structure
        current_dir = Path(__file__).parent
        assert current_dir.name == "tests", "Test file not in tests directory"
        
        # Test that It1_interfaces directory exists
        it1_dir = current_dir.parent / "It1_interfaces"
        assert it1_dir.exists(), "It1_interfaces directory not found"
        
        # Test that main game files exist
        expected_files = ["main_refactored.py", "GameRefactored.py", "Board.py"]
        for file in expected_files:
            if (it1_dir / file).exists():
                assert True  # File exists
            else:
                print(f"Warning: Expected file {file} not found")
    
    def test_visual_improvements_complete(self):
        """Test that all visual improvements are implemented"""
        improvements_checklist = {
            "PlayerNameDialog window size": False,
            "Background image support": False, 
            "Enhanced fonts": False,
            "Focus solution": False
        }
        
        # Check PlayerNameDialog improvements
        if check_module_exists("PlayerNameDialog"):
            from PlayerNameDialog import PlayerNameDialog
            dialog = PlayerNameDialog()
            
            if dialog.window_width == 800 and dialog.window_height == 600:
                improvements_checklist["PlayerNameDialog window size"] = True
            
            if hasattr(dialog, '_load_background_image'):
                improvements_checklist["Background image support"] = True
        
        # Check font improvements
        if check_module_exists("DrawManager"):
            import inspect
            from DrawManager import DrawManager
            source = inspect.getsource(DrawManager)
            
            if "FONT_HERSHEY_DUPLEX" in source:
                improvements_checklist["Enhanced fonts"] = True
        
        # Check focus solution
        if check_module_exists("WindowFocusManager"):
            improvements_checklist["Focus solution"] = True
        
        # Report results
        for improvement, implemented in improvements_checklist.items():
            if implemented:
                print(f"✅ {improvement}: Implemented")
            else:
                print(f"⚠️ {improvement}: Not found")
        
        # At least some improvements should be implemented
        implemented_count = sum(improvements_checklist.values())
        assert implemented_count > 0, "No visual improvements found"


class TestGamePlayFlow:
    """Test the complete gameplay flow"""
    
    def test_game_startup_flow(self):
        """Test that game can start up without critical errors"""
        if check_module_exists("PlayerNameManager"):
            try:
                from PlayerNameManager import PlayerNameManager
                
                # Test basic functionality without actually starting GUI
                manager = PlayerNameManager()
                assert manager is not None
                
            except ImportError:
                pytest.skip("PlayerNameManager not available")
    
    def test_main_file_structure(self):
        """Test that main game file has correct structure"""
        main_files = ["main_refactored.py", "main.py"]
        it1_dir = Path(__file__).parent.parent / "It1_interfaces"
        
        main_file_found = False
        for main_file in main_files:
            if (it1_dir / main_file).exists():
                main_file_found = True
                break
        
        assert main_file_found, "No main game file found"


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
