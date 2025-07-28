"""
create_background.py - יצירת תמונת רקע למשחק השח
"""
import cv2
import numpy as np
import pathlib

def create_chess_background():
    """Create a beautiful background for the chess game"""
    
    # גדלי הרקע
    width = 1200
    height = 800
    
    # יצירת gradient יפה
    background = np.zeros((height, width, 3), dtype=np.uint8)
    
    # יצירת gradient מכחול כהה לכחול בהיר
    for y in range(height):
        # חישוב צבע לפי גובה
        ratio = y / height
        
        # כחול כהה למעלה, כחול בהיר למטה
        blue = int(50 + ratio * 100)  # 50-150
        green = int(30 + ratio * 80)  # 30-110
        red = int(20 + ratio * 60)    # 20-80
        
        background[y, :] = [blue, green, red]
    
    # הוספת pattern עדין
    for i in range(0, width, 40):
        cv2.line(background, (i, 0), (i, height), (255, 255, 255), 1, cv2.LINE_AA)
        
    for i in range(0, height, 40):
        cv2.line(background, (0, i), (width, i), (255, 255, 255), 1, cv2.LINE_AA)
    
    # הוספת כותרת יפה
    title_text = "CHESS GAME"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_thickness = 3
    
    # חישוב מיקום הכותרת
    text_size = cv2.getTextSize(title_text, font, font_scale, font_thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = 60
    
    # הוספת צל לטקסט
    cv2.putText(background, title_text, (text_x + 2, text_y + 2), 
                font, font_scale, (0, 0, 0), font_thickness + 1)
    
    # הוספת הטקסט הראשי
    cv2.putText(background, title_text, (text_x, text_y), 
                font, font_scale, (255, 255, 255), font_thickness)
    
    # הוספת אזורי פאנל
    # פאנל שמאל - שחקן 1
    cv2.rectangle(background, (20, 120), (280, 720), (70, 70, 100), 2)
    cv2.putText(background, "PLAYER 1", (40, 150), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 255), 2)
    cv2.putText(background, "(White)", (40, 180), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 255), 1)
    
    # פאנל ימין - שחקן 2
    cv2.rectangle(background, (920, 120), (1180, 720), (100, 70, 70), 2)
    cv2.putText(background, "PLAYER 2", (940, 150), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 200, 200), 2)
    cv2.putText(background, "(Black)", (940, 180), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 200), 1)
    
    # אזור הלוח
    board_x = 300
    board_y = 100
    board_size = 600
    cv2.rectangle(background, (board_x - 10, board_y - 10), 
                  (board_x + board_size + 10, board_y + board_size + 10), 
                  (255, 255, 255), 3)
    
    return background

def save_background():
    """Save the background image"""
    background = create_chess_background()
    
    # נתיב השמירה
    save_path = pathlib.Path(__file__).parent.parent / "background.png"
    
    # שמירה
    success = cv2.imwrite(str(save_path), background)
    
    if success:
        print(f"✅ תמונת הרקע נשמרה בהצלחה: {save_path}")
        return True
    else:
        print(f"❌ שגיאה בשמירת תמונת הרקע")
        return False

if __name__ == "__main__":
    print("🎨 יוצר תמונת רקע למשחק השח...")
    
    # בדוק אם כבר יש תמונת רקע
    bg_path = pathlib.Path(__file__).parent.parent / "background.png"
    if bg_path.exists():
        print(f"⚠️ תמונת רקע כבר קיימת: {bg_path}")
        response = input("האם לדרוס? (y/n): ")
        if response.lower() != 'y':
            print("ביטול היצירה")
            exit()
    
    success = save_background()
    
    if success:
        print("🎉 תמונת הרקע מוכנה!")
        print("🎮 עכשיו אפשר להריץ את המשחק עם:")
        print("   python main_refactored.py")
    else:
        print("❌ שגיאה ביצירת תמונת הרקע")
