"""
טסט משולב - פוקוס חלון + דיאלוג שמות
"""
import cv2
from src.ui.WindowFocusManager import WindowFocusManager
from src.ui.PlayerNameDialog import PlayerNameDialog

print("🧪 Testing integrated window focus solution...")

try:
    # בדיקת מנהל הפוקוס
    print("1️⃣ Testing WindowFocusManager...")
    focus_manager = WindowFocusManager("Test Window")
    focus_manager.create_focused_window()
    print("✅ WindowFocusManager works")
    
    # בדיקת דיאלוג השמות
    print("\n2️⃣ Testing PlayerNameDialog...")
    print("📝 Please enter test names in the dialog window:")
    dialog = PlayerNameDialog("Test - Player Names")
    player1, player2 = dialog.get_player_names()
    
    print(f"✅ Names received: {player1}, {player2}")
    
    # מעכשיו חלון המשחק אמור להיות עם פוקוס!
    print("\n3️⃣ Window focus should now be established!")
    print("🎮 The next window should capture keyboard input automatically")
    
    # ניקוי
    cv2.destroyAllWindows()
    print("\n✅ Test completed successfully!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    cv2.destroyAllWindows()
