"""
טסטים ל-PlayerNameDialog עם unittest
"""
import unittest
import sys
import os
from pathlib import Path

# הוספת נתיב It1_interfaces
current_dir = Path(__file__).parent
it1_dir = current_dir.parent / "It1_interfaces"
sys.path.insert(0, str(it1_dir))

class TestPlayerNameDialog(unittest.TestCase):
    """בדיקות ל-PlayerNameDialog"""
    
    def setUp(self):
        """הכנה לפני כל טסט"""
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass
    
    def tearDown(self):
        """ניקוי אחרי כל טסט"""
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass
    
    def test_import_player_dialog(self):
        """בדיקת import של PlayerNameDialog"""
        try:
            from PlayerNameDialog import PlayerNameDialog
            self.assertIsNotNone(PlayerNameDialog)
            print("✅ PlayerNameDialog imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import PlayerNameDialog: {e}")
    
    def test_dialog_creation(self):
        """בדיקת יצירת דיאלוג"""
        try:
            from PlayerNameDialog import PlayerNameDialog
            
            dialog = PlayerNameDialog()
            
            # בדיקות בסיסיות
            self.assertIsNotNone(dialog)
            self.assertEqual(dialog.window_width, 800)
            self.assertEqual(dialog.window_height, 600) 
            self.assertEqual(dialog.player1_name, "")
            self.assertEqual(dialog.player2_name, "")
            self.assertEqual(dialog.current_input, 1)
            self.assertFalse(dialog.is_complete)
            
            print("✅ PlayerNameDialog created with correct properties")
            
        except Exception as e:
            self.fail(f"Dialog creation failed: {e}")
    
    def test_background_image_loading(self):
        """בדיקת טעינת תמונת רקע"""
        try:
            from PlayerNameDialog import PlayerNameDialog
            
            dialog = PlayerNameDialog()
            
            # בדיקת קיום תמונת רקע
            self.assertIsNotNone(dialog.background_image)
            
            # בדיקת גודל
            height, width = dialog.background_image.shape[:2]
            self.assertEqual(width, 800)
            self.assertEqual(height, 600)
            
            print("✅ Background image loaded correctly")
            
        except Exception as e:
            self.fail(f"Background loading failed: {e}")
    
    def test_key_handling_esc(self):
        """בדיקת טיפול במקש ESC"""
        try:
            from PlayerNameDialog import PlayerNameDialog
            
            dialog = PlayerNameDialog()
            
            # בדיקת ESC key
            result = dialog._handle_key(27)  # ESC
            
            self.assertTrue(result)
            self.assertTrue(dialog.is_complete)
            self.assertEqual(dialog.player1_name, "Player 1")
            self.assertEqual(dialog.player2_name, "Player 2")
            
            print("✅ ESC key handling works correctly")
            
        except Exception as e:
            self.fail(f"ESC key handling failed: {e}")
    
    def test_key_handling_enter(self):
        """בדיקת טיפול במקש ENTER"""
        try:
            from PlayerNameDialog import PlayerNameDialog
            
            dialog = PlayerNameDialog()
            
            # בדיקת ENTER בשחקן 1
            result = dialog._handle_key(13)  # ENTER
            self.assertTrue(result)
            self.assertEqual(dialog.current_input, 2)
            self.assertEqual(dialog.player1_name, "Player 1")  # שם ברירת מחדל
            
            # בדיקת ENTER בשחקן 2
            result = dialog._handle_key(13)  # ENTER
            self.assertTrue(result)
            self.assertTrue(dialog.is_complete)
            self.assertEqual(dialog.player2_name, "Player 2")  # שם ברירת מחדל
            
            print("✅ ENTER key handling works correctly")
            
        except Exception as e:
            self.fail(f"ENTER key handling failed: {e}")
    
    def test_key_handling_regular_chars(self):
        """בדיקת טיפול בתווים רגילים"""
        try:
            from PlayerNameDialog import PlayerNameDialog
            
            dialog = PlayerNameDialog()
            
            # הוספת תו 'A'
            result = dialog._handle_key(65)  # 'A'
            self.assertTrue(result)
            self.assertEqual(dialog.player1_name, "A")
            
            # הוספת תו 'l'
            result = dialog._handle_key(108)  # 'l'
            self.assertTrue(result)
            self.assertEqual(dialog.player1_name, "Al")
            
            print("✅ Regular character input works correctly")
            
        except Exception as e:
            self.fail(f"Character input failed: {e}")
    
    def test_name_length_limit(self):
        """בדיקת הגבלת אורך שמות"""
        try:
            from PlayerNameDialog import PlayerNameDialog
            
            dialog = PlayerNameDialog()
            
            # הוספת 15 תווים (המקסימום)
            for i in range(15):
                dialog._handle_key(65)  # 'A'
            
            self.assertEqual(len(dialog.player1_name), 15)
            
            # ניסיון הוספת תו נוסף
            dialog._handle_key(65)  # 'A'
            
            # הגבלה פועלת - עדיין 15
            self.assertEqual(len(dialog.player1_name), 15)
            
            print("✅ Name length limit works correctly")
            
        except Exception as e:
            self.fail(f"Length limit test failed: {e}")

if __name__ == "__main__":
    print("🧪 Running PlayerNameDialog tests with unittest...")
    print("=" * 60)
    
    # הרצת הטסטים
    unittest.main(verbosity=2)
