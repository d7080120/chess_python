"""
טסט פשוט ל-PlayerNameDialog עם pytest
"""
import sys
import os
from pathlib import Path

# הוספת נתיב It1_interfaces
current_dir = Path(__file__).parent
it1_dir = current_dir.parent / "It1_interfaces"
sys.path.insert(0, str(it1_dir))

def test_simple_import():
    """טסט פשוט לבדיקת import של PlayerNameDialog"""
    try:
        from PlayerNameDialog import PlayerNameDialog
        assert PlayerNameDialog is not None
        print("✅ PlayerNameDialog imported successfully")
    except ImportError as e:
        assert False, f"Failed to import PlayerNameDialog: {e}"

def test_dialog_creation():
    """טסט יצירת דיאלוג"""
    try:
        from PlayerNameDialog import PlayerNameDialog
        
        dialog = PlayerNameDialog()
        assert dialog is not None
        assert dialog.window_width == 800
        assert dialog.window_height == 600
        assert dialog.player1_name == ""
        assert dialog.player2_name == ""
        print("✅ PlayerNameDialog created successfully")
        
        # ניקוי
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass
            
    except Exception as e:
        assert False, f"Failed to create PlayerNameDialog: {e}"

def test_key_handling():
    """טסט טיפול במקשים"""
    try:
        from PlayerNameDialog import PlayerNameDialog
        
        dialog = PlayerNameDialog()
        
        # בדיקת ESC key
        result = dialog._handle_key(27)  # ESC
        assert result == True
        assert dialog.is_complete == True
        assert dialog.player1_name == "Player 1"
        assert dialog.player2_name == "Player 2"
        print("✅ Key handling works correctly")
        
        # ניקוי
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass
            
    except Exception as e:
        assert False, f"Key handling test failed: {e}"

def test_background_image():
    """טסט טעינת תמונת רקע"""
    try:
        from PlayerNameDialog import PlayerNameDialog
        
        dialog = PlayerNameDialog()
        
        assert dialog.background_image is not None
        height, width = dialog.background_image.shape[:2]
        assert width == 800
        assert height == 600
        print("✅ Background image loaded successfully")
        
        # ניקוי
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass
            
    except Exception as e:
        assert False, f"Background image test failed: {e}"

if __name__ == "__main__":
    print("🧪 Running PlayerNameDialog tests...")
    
    try:
        test_simple_import()
        test_dialog_creation()
        test_key_handling()
        test_background_image()
        print("\n🎉 All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
