"""
טסטים פשוטים ל-PlayerNameDialog ללא pytest
Simple tests for PlayerNameDialog without pytest dependency
"""
import sys
import os
from pathlib import Path

# הוספת נתיב It1_interfaces
current_dir = Path(__file__).parent
it1_dir = current_dir.parent / "It1_interfaces"
sys.path.insert(0, str(it1_dir))

def test_player_dialog_import():
    """בדיקת import של PlayerNameDialog"""
    try:
        from PlayerNameDialog import PlayerNameDialog
        print("✅ Test 1: PlayerNameDialog import - PASSED")
        return True
    except ImportError as e:
        print(f"❌ Test 1: PlayerNameDialog import - FAILED: {e}")
        return False

def test_player_dialog_creation():
    """בדיקת יצירת דיאלוג"""
    try:
        from PlayerNameDialog import PlayerNameDialog
        dialog = PlayerNameDialog()
        
        # בדיקות בסיסיות
        assert dialog.window_width == 800, f"Expected width 800, got {dialog.window_width}"
        assert dialog.window_height == 600, f"Expected height 600, got {dialog.window_height}"
        assert dialog.player1_name == "", f"Expected empty player1_name, got '{dialog.player1_name}'"
        assert dialog.player2_name == "", f"Expected empty player2_name, got '{dialog.player2_name}'"
        assert dialog.current_input == 1, f"Expected current_input 1, got {dialog.current_input}"
        assert dialog.is_complete == False, f"Expected is_complete False, got {dialog.is_complete}"
        
        # ניקוי
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass
            
        print("✅ Test 2: PlayerNameDialog creation - PASSED")
        return True
    except Exception as e:
        print(f"❌ Test 2: PlayerNameDialog creation - FAILED: {e}")
        return False

def test_background_loading():
    """בדיקת טעינת רקע"""
    try:
        from PlayerNameDialog import PlayerNameDialog
        dialog = PlayerNameDialog()
        
        assert dialog.background_image is not None, "Background image is None"
        height, width = dialog.background_image.shape[:2]
        assert width == 800, f"Background width expected 800, got {width}"
        assert height == 600, f"Background height expected 600, got {height}"
        
        # ניקוי
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass
            
        print("✅ Test 3: Background loading - PASSED")
        return True
    except Exception as e:
        print(f"❌ Test 3: Background loading - FAILED: {e}")
        return False

def test_key_handling():
    """בדיקת טיפול במקשים"""
    try:
        from PlayerNameDialog import PlayerNameDialog
        dialog = PlayerNameDialog()
        
        # בדיקת ESC key (27)
        result = dialog._handle_key(27)
        assert result == True, "ESC key should return True"
        assert dialog.is_complete == True, "Dialog should be complete after ESC"
        assert dialog.player1_name == "Player 1", f"Expected 'Player 1', got '{dialog.player1_name}'"
        assert dialog.player2_name == "Player 2", f"Expected 'Player 2', got '{dialog.player2_name}'"
        
        # ניקוי
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass
            
        print("✅ Test 4: Key handling - PASSED")
        return True
    except Exception as e:
        print(f"❌ Test 4: Key handling - FAILED: {e}")
        return False

def test_character_input():
    """בדיקת קלט תווים"""
    try:
        from PlayerNameDialog import PlayerNameDialog
        dialog = PlayerNameDialog()
        
        # הוספת תו 'A' (65)
        result = dialog._handle_key(65)
        assert result == True, "Character input should return True"
        assert dialog.player1_name == "A", f"Expected 'A', got '{dialog.player1_name}'"
        
        # הוספת תו 'l' (108)
        result = dialog._handle_key(108)
        assert result == True, "Character input should return True"
        assert dialog.player1_name == "Al", f"Expected 'Al', got '{dialog.player1_name}'"
        
        # בדיקת BACKSPACE (8)
        result = dialog._handle_key(8)
        assert result == True, "Backspace should return True"
        assert dialog.player1_name == "A", f"Expected 'A' after backspace, got '{dialog.player1_name}'"
        
        # ניקוי
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass
            
        print("✅ Test 5: Character input - PASSED")
        return True
    except Exception as e:
        print(f"❌ Test 5: Character input - FAILED: {e}")
        return False

def test_dialog_image_creation():
    """בדיקת יצירת תמונת דיאלוג"""
    try:
        from PlayerNameDialog import PlayerNameDialog
        dialog = PlayerNameDialog()
        
        dialog_img = dialog._create_dialog_image()
        assert dialog_img is not None, "Dialog image should not be None"
        
        height, width = dialog_img.shape[:2]
        assert width == 800, f"Dialog image width expected 800, got {width}"
        assert height == 600, f"Dialog image height expected 600, got {height}"
        
        # ניקוי
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass
            
        print("✅ Test 6: Dialog image creation - PASSED")
        return True
    except Exception as e:
        print(f"❌ Test 6: Dialog image creation - FAILED: {e}")
        return False

def run_all_tests():
    """הרצת כל הטסטים"""
    print("🧪 Running PlayerNameDialog Tests")
    print("=" * 40)
    
    tests = [
        test_player_dialog_import,
        test_player_dialog_creation,
        test_background_loading,
        test_key_handling,
        test_character_input,
        test_dialog_image_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests PASSED!")
        return True
    else:
        print(f"⚠️ {total - passed} tests FAILED!")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
