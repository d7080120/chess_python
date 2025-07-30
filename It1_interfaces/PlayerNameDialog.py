"""
PlayerNameDialog - חלון GUI לקבלת שמות השחקנים
פותר את בעיית הפוקוס ומספק חוויה טובה יותר
"""
import cv2
import numpy as np
import time
from pathlib import Path
from window_utils import center_window


class PlayerNameDialog:
    """Simple GUI dialog for getting player names using OpenCV"""
    
    def __init__(self, window_name="Chess Game - Player Names", window_position="center"):
        self.window_name = window_name
        self.window_position = window_position  # "center" או "top-left"
        self.player1_name = ""
        self.player2_name = ""
        self.current_input = 1  # 1 for player1, 2 for player2
        self.is_complete = False
        self.window_width = 800  # הגדלנו מ-600 ל-800
        self.window_height = 600  # הגדלנו מ-400 ל-600
        
        # טעינת תמונת הרקע
        self.background_image = self._load_background_image()
        
        # יצירת החלון והבטחת פוקוס
        self._create_window()
    
    def _create_window(self):
        """Create the dialog window with focus"""
        cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 1)
        
        # מיקום החלון לפי הבחירה
        center_window(self.window_name, self.window_width, self.window_height, self.window_position)
        
        print(f"🖥️ Player name dialog created: '{self.window_name}'")
        print("📝 Please enter player names in the dialog window")
    
    def _load_background_image(self):
        """Load logo.jpg as background image with fallback"""
        try:
            # נחפש את logo.jpg באותה תיקייה או בתיקיית הבסיס
            current_dir = Path(__file__).parent
            logo_paths = [
                current_dir / "logo.jpg",
                current_dir.parent / "logo.jpg",
                Path("logo.jpg")
            ]
            
            for logo_path in logo_paths:
                if logo_path.exists():
                    print(f"🖼️ Loading background image from: {logo_path}")
                    background = cv2.imread(str(logo_path))
                    if background is not None:
                        # שינוי גודל לחלון
                        background = cv2.resize(background, (self.window_width, self.window_height))
                        # הוספת שכבת שקיפות עדינה כדי שהטקסט יהיה קריא
                        overlay = np.zeros_like(background)
                        overlay[:] = (255, 255, 255)  # רקע לבן חלקי
                        background = cv2.addWeighted(background, 0.3, overlay, 0.7, 0)
                        return background
            
            print("⚠️ Logo.jpg not found, using gradient background")
            return self._create_gradient_background()
            
        except Exception as e:
            print(f"❌ Error loading background image: {e}")
            return self._create_gradient_background()
    
    def _create_gradient_background(self):
        """Create a nice gradient background as fallback"""
        background = np.zeros((self.window_height, self.window_width, 3), dtype=np.uint8)
        for i in range(self.window_height):
            # גרדיאנט מכחול בהיר לכחול כהה
            ratio = i / self.window_height
            blue_val = int(240 - 40 * ratio)
            green_val = int(230 - 30 * ratio)
            red_val = int(200 - 50 * ratio)
            background[i, :] = (blue_val, green_val, red_val)
        return background
    
    def _create_dialog_image(self):
        """Create the dialog image with background and enhanced fonts"""
        # התחלה עם תמונת הרקע
        img = self.background_image.copy()
        
        # כותרת מעוצבת עם צל
        title = "Chess Game - Enter Player Names"
        # צל לכותרת
        cv2.putText(img, title, (52, 82), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 0), 3)
        # כותרת עיקרית
        cv2.putText(img, title, (50, 80), cv2.FONT_HERSHEY_DUPLEX, 1.2, (255, 255, 255), 2)
        
        # הוראות
        instructions = "Type names and press ENTER to confirm each name"
        cv2.putText(img, instructions, (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 50, 50), 2)
        
        # רקע לשדות הקלט
        cv2.rectangle(img, (40, 160), (760, 200), (255, 255, 255), -1)  # רקע לבן לשחקן 1
        cv2.rectangle(img, (40, 160), (760, 200), (100, 100, 100), 2)   # מסגרת
        
        cv2.rectangle(img, (40, 220), (760, 260), (255, 255, 255), -1)  # רקע לבן לשחקן 2
        cv2.rectangle(img, (40, 220), (760, 260), (100, 100, 100), 2)   # מסגרת
        
        # שדה שחקן 1
        player1_label = f"Player 1 (White pieces): {self.player1_name}"
        if self.current_input == 1:
            player1_label += "_"  # קרסור מהבהב
        color1 = (0, 120, 0) if self.player1_name else (200, 0, 0)
        cv2.putText(img, player1_label, (50, 185), cv2.FONT_HERSHEY_DUPLEX, 0.8, color1, 2)
        
        # מסגרת מודגשת לשחקן פעיל
        if self.current_input == 1:
            cv2.rectangle(img, (40, 160), (760, 200), (0, 0, 255), 3)
        
        # שדה שחקן 2
        player2_label = f"Player 2 (Black pieces): {self.player2_name}"
        if self.current_input == 2:
            player2_label += "_"  # קרסור מהבהב
        color2 = (0, 120, 0) if self.player2_name else (200, 0, 0)
        cv2.putText(img, player2_label, (50, 245), cv2.FONT_HERSHEY_DUPLEX, 0.8, color2, 2)
        
        # מסגרת מודגשת לשחקן פעיל
        if self.current_input == 2:
            cv2.rectangle(img, (40, 220), (760, 260), (0, 0, 255), 3)
        
        # הוראות נוספות עם רקע
        instruction_y = 320
        cv2.rectangle(img, (40, 300), (760, 370), (240, 240, 240), -1)  # רקע אפור בהיר
        cv2.rectangle(img, (40, 300), (760, 370), (150, 150, 150), 2)   # מסגרת
        
        if not self.is_complete:
            if self.current_input == 1:
                instruction = "Enter name for Player 1 (White), then press ENTER"
            else:
                instruction = "Enter name for Player 2 (Black), then press ENTER"
            cv2.putText(img, instruction, (50, instruction_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 150), 2)
        else:
            cv2.putText(img, "Names entered successfully! Starting game...", 
                       (50, instruction_y), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 150, 0), 2)
        
        # הוראות מקשים מעוצבות
        key_instructions = [
            "BACKSPACE: Delete last character",
            "ENTER: Confirm current name", 
            "ESC: Use default names"
        ]
        
        for i, instruction in enumerate(key_instructions):
            y_pos = 420 + i * 30
            cv2.putText(img, instruction, (50, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (80, 80, 80), 2)
        
        return img
    
    def _handle_key(self, key):
        """Handle keyboard input for name entry"""
        # ESC - השתמש בשמות ברירת מחדל
        if key == 27:
            if not self.player1_name:
                self.player1_name = "Player 1"
            if not self.player2_name:
                self.player2_name = "Player 2"
            self.is_complete = True
            return True
        
        # ENTER - אשר שם נוכחי
        if key == 13 or key == 10:
            if self.current_input == 1:
                if not self.player1_name:
                    self.player1_name = "Player 1"  # ברירת מחדל
                self.current_input = 2
            elif self.current_input == 2:
                if not self.player2_name:
                    self.player2_name = "Player 2"  # ברירת מחדל
                self.is_complete = True
            return True
        
        # BACKSPACE - מחק תו אחרון
        if key == 8:
            if self.current_input == 1 and self.player1_name:
                self.player1_name = self.player1_name[:-1]
            elif self.current_input == 2 and self.player2_name:
                self.player2_name = self.player2_name[:-1]
            return True
        
        # תווים רגילים - הוסף לשם
        if 32 <= key <= 126:  # תווים ASCII הדפיסים
            char = chr(key)
            if self.current_input == 1:
                if len(self.player1_name) < 15:  # הגבלת אורך
                    self.player1_name += char
            elif self.current_input == 2:
                if len(self.player2_name) < 15:  # הגבלת אורך
                    self.player2_name += char
            return True
        
        return False
    
    def get_player_names(self):
        """Main method to get player names through GUI"""
        print("🎮 Starting player name dialog...")
        print("👥 Please enter player names in the dialog window")
        
        while not self.is_complete:
            # יצירת תמונת הדיאלוג
            dialog_img = self._create_dialog_image()
            
            # הצגה
            cv2.imshow(self.window_name, dialog_img)
            
            # המתנה לקלט
            key = cv2.waitKey(50) & 0xFF
            
            if key != 255:  # מקש נלחץ
                if self._handle_key(key):
                    continue  # מקש טופל בהצלחה
        
        # סגירת החלון
        cv2.destroyWindow(self.window_name)
        
        # הבטחת שמות תקינים
        if not self.player1_name.strip():
            self.player1_name = "Player 1"
        if not self.player2_name.strip():
            self.player2_name = "Player 2"
        
        print(f"✅ Player names entered:")
        print(f"   🏳️ Player 1 (White): {self.player1_name}")
        print(f"   ⚫ Player 2 (Black): {self.player2_name}")
        
        return self.player1_name.strip(), self.player2_name.strip()
    
    def __del__(self):
        """Cleanup on destruction"""
        try:
            cv2.destroyWindow(self.window_name)
        except:
            pass
