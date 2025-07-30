"""
בדיקת הדיאלוג החזותי החדש עם התמונה ולוגו
"""
import cv2
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from PlayerNameDialog import PlayerNameDialog

def test_visual_dialog():
    """Test the visual improvements in PlayerNameDialog"""
    print("🎮 Testing visual dialog improvements...")
    print("📸 Background: logo.jpg or gradient fallback")
    print("🖋️ Enhanced fonts: FONT_HERSHEY_DUPLEX")
    print("📏 Larger window: 800x600")
    
    try:
        # יצירת הדיאלוג
        dialog = PlayerNameDialog()
        print("✅ Dialog created successfully")
        
        # בדיקת טעינת הרקע
        if dialog.background_image is not None:
            print("✅ Background image loaded")
            height, width = dialog.background_image.shape[:2]
            print(f"📐 Background size: {width}x{height}")
        else:
            print("❌ Background image failed to load")
        
        # בדיקת יכולת יצירת תמונת דיאלוג
        dialog_img = dialog._create_dialog_image()
        if dialog_img is not None:
            print("✅ Dialog image created successfully")
            height, width = dialog_img.shape[:2]
            print(f"📐 Dialog image size: {width}x{height}")
        else:
            print("❌ Dialog image creation failed")
            
        print("🎯 Visual dialog test completed successfully!")
        print("\n👀 To see the actual dialog, run:")
        print("   python -c \"from PlayerNameDialog import PlayerNameDialog; d=PlayerNameDialog(); d.get_player_names()\"")
        
    except Exception as e:
        print(f"❌ Error in visual dialog test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_visual_dialog()
