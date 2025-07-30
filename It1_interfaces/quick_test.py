"""
טסט מהיר של דיאלוג השמות - הרצה פשוטה
"""
import sys
sys.path.append('.')

print("Starting quick test...")

try:
    from PlayerNameDialog import PlayerNameDialog
    print("✅ Import successful")
    
    print("🎮 Creating dialog...")
    dialog = PlayerNameDialog()
    print("✅ Dialog created")
    
    print("📋 You should now see a dialog window!")
    print("📝 Enter names and press ESC when done to test")
    
    names = dialog.get_player_names()
    print(f"✅ Got names: {names}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("🎯 Test finished!")
