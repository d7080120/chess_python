"""
InputHandler - מחלקה לטיפול בקלט מהמקלדת עם תמיכה בפוקוס אוטומטי
"""
import cv2
import time
from WindowFocusManager import WindowFocusManager


class InputHandler:
    def __init__(self, game_ref):
        """Initialize the input handler with reference to game."""
        self.game = game_ref
        self.window_name = "Chess Game"
        self.focus_attempts = 0
        self.max_focus_attempts = 5
        self.last_focus_time = 0
        
        # הגדרות Windows API
        if WINDOWS_API_AVAILABLE:
            self._setup_windows_api()
        
        # אתחול חלון עם פוקוס
        self._initialize_window_with_focus()
    
    def _setup_windows_api(self):
        """Setup Windows API functions for window focus"""
        if not WINDOWS_API_AVAILABLE:
            return
            
        try:
            # הגדרת פונקציות Windows API
            user32 = ctypes.windll.user32
            self.FindWindow = user32.FindWindowW
            self.FindWindow.argtypes = [ctypes.wintypes.LPCWSTR, ctypes.wintypes.LPCWSTR]
            self.FindWindow.restype = ctypes.wintypes.HWND
            
            self.SetForegroundWindow = user32.SetForegroundWindow
            self.SetForegroundWindow.argtypes = [ctypes.wintypes.HWND]
            self.SetForegroundWindow.restype = ctypes.wintypes.BOOL
            
            self.ShowWindow = user32.ShowWindow
            self.ShowWindow.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
            self.ShowWindow.restype = ctypes.wintypes.BOOL
            
            self.SetFocus = user32.SetFocus
            self.SetFocus.argtypes = [ctypes.wintypes.HWND]
            self.SetFocus.restype = ctypes.wintypes.HWND
            
            print("🔧 Windows API setup successful for window focus")
        except Exception as e:
            print(f"⚠️ Windows API setup failed, using fallback methods: {e}")
            
    def _initialize_window_with_focus(self):
        """Initialize window with automatic focus"""
        try:
            # יצירת החלון
            cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
            
            # הגדרות בסיסיות
            cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 1)
            
            # חישוב מיקום מרכזי במסך
            try:
                import tkinter as tk
                root = tk.Tk()
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                root.destroy()
                
                # גודל חלון משחק משוער
                game_window_width = 800
                game_window_height = 800
                
                # מיקום מרכזי
                center_x = (screen_width - game_window_width) // 2
                center_y = (screen_height - game_window_height) // 2
                
                cv2.moveWindow(self.window_name, center_x, center_y)
            except Exception as e:
                # fallback למיקום ברירת מחדל
                cv2.moveWindow(self.window_name, 100, 100)
            
            # נסיון להבטיח פוקוס מיידי
            self._force_window_focus()
            
        except Exception as e:
            print(f"⚠️ Window initialization warning: {e}")
    
    def _force_window_focus(self):
        """Force the game window to receive focus using multiple methods"""
        if self.focus_attempts >= self.max_focus_attempts:
            return
            
        current_time = time.time()
        if current_time - self.last_focus_time < 0.5:  # לא יותר מפעמיים בשנייה
            return
            
        self.last_focus_time = current_time
        self.focus_attempts += 1
        
        try:
            # שיטה 1: OpenCV מובנה
            cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 1)
            
            # שיטה 2: Windows API (אם זמין)
            if WINDOWS_API_AVAILABLE:
                self._windows_force_focus()
                
            # שיטה 3: הצגת תמונה ריקה לכפיית רענון
            import numpy as np
            dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
            cv2.imshow(self.window_name, dummy_img)
            cv2.waitKey(1)  # רענון מיידי
            
        except Exception as e:
            pass  # לא קריטי
    
    def _windows_force_focus(self):
        """Use Windows API to force focus on the game window"""
        if not WINDOWS_API_AVAILABLE:
            return
            
        try:
            # חפש את החלון
            hwnd = self.FindWindow(None, self.window_name)
            if hwnd:
                # הצג את החלון ו force focus
                self.ShowWindow(hwnd, 9)  # SW_RESTORE
                self.SetForegroundWindow(hwnd)
                self.SetFocus(hwnd)
                
        except Exception as e:
            pass  # לא קריטי

    def handle_keyboard_input(self, key):
        """Handle keyboard input for both players."""
        print(f"\n=== KEY PRESSED: {key} ===")
        if 32 <= key <= 126:
            print(f"Character: '{chr(key)}'")
        else:
            print(f"Special key code: {key}")
        
        # Check for exit keys first
        if key == 27 or key == ord('q'):  # ESC או Q
            self.game.game_over = True  # סמן שהמשחק נגמר
            return True  # Signal to exit
        
        # Convert to character for easier handling
        char = None
        if 32 <= key <= 126:
            char = chr(key).lower()
        
        # Enhanced WASD detection for Player 2 (שחקן 2 שולט בכלים שחורים)
        wasd_detected = False
        
        # תמיכה מלאה במקלדת עברית! זיהוי מתקדם של מקשים עבריים
        hebrew_keys = {
            ord('\''): 'w',
            ord('ש'): 'a',
            ord('ד'): 's',
            ord('ג'): 'd'
        }
        # Check Hebrew keys
        detected_hebrew = hebrew_keys.get(key)
        if detected_hebrew:
            print(f"🔥 Hebrew key detected: {key} -> {detected_hebrew}")
            char = detected_hebrew
        
        # W key (UP) - English W או עברית ו
        if (key in [119, 87] or char == 'w' or 
            key in [1493, 215, 246, 1500] or  # Hebrew ו (vav)
            detected_hebrew == 'w'):
            print("🔥 Player 2: Moving UP (W/vav) - WASD WORKING!")
            self.game.player_manager.move_cursor_player2(0, -1)
            wasd_detected = True
        # S key (DOWN) - English S או עברית ד
        elif (key in [115, 83] or char == 's' or 
              key in [1491, 212, 213, 1504] or  # Hebrew ד (dalet)
              detected_hebrew == 's'):
            print("🔥 Player 2: Moving DOWN (S/dalet) - WASD WORKING!")
            self.game.player_manager.move_cursor_player2(0, 1)
            wasd_detected = True
        # A key (LEFT) - English A או עברית ש
        elif (key in [97, 65] or char == 'a' or 
              key in [1513, 249, 251, 1506] or  # Hebrew ש (shin)
              detected_hebrew == 'a'):
            print("🔥 Player 2: Moving LEFT (A/shin) - WASD WORKING!")
            self.game.player_manager.move_cursor_player2(-1, 0)
            wasd_detected = True
        # D key (RIGHT) - English D או עברית כ
        elif (key in [100, 68] or char == 'd' or 
              key in [1499, 235, 237, 1507] or  # Hebrew כ (kaf)
              detected_hebrew == 'd'):
            print("🔥 Player 2: Moving RIGHT (D/kaf) - WASD WORKING!")
            self.game.player_manager.move_cursor_player2(1, 0)
            wasd_detected = True
        elif key == 32 or char == ' ':  # Space
            print("🔥 Player 2: Selecting piece (SPACE) - SPACE WORKING!")
            self.game.player_manager.select_piece_player2()
            wasd_detected = True
        
        # מקשי חירום נוספים לשחקן 2 (אם WASD לא עובד)
        elif key in [255, 254, 253, 252]:  # מקשים מיוחדים כחלופה
            emergency_map = {255: 'w', 254: 's', 253: 'a', 252: 'd'}
            direction = emergency_map.get(key)
            if direction:
                print(f"🚨 Player 2: Emergency key {key} -> {direction}")
                if direction == 'w':
                    self.game.player_manager.move_cursor_player2(0, -1)
                elif direction == 's':
                    self.game.player_manager.move_cursor_player2(0, 1)
                elif direction == 'a':
                    self.game.player_manager.move_cursor_player2(-1, 0)
                elif direction == 'd':
                    self.game.player_manager.move_cursor_player2(1, 0)
                wasd_detected = True
        
        # Player 1 controls - מקשי מספרים - שחקן 1 שולט בכלים לבנים
        elif key == 56 or char == '8':  # 8 key
            print("⚡ Player 1: Moving UP (8) - NUMBERS WORKING!")
            self.game.player_manager.move_cursor_player1(0, -1)
        elif key == 50 or char == '2':  # 2 key
            print("⚡ Player 1: Moving DOWN (2) - NUMBERS WORKING!")
            self.game.player_manager.move_cursor_player1(0, 1)
        elif key == 52 or char == '4':  # 4 key
            print("⚡ Player 1: Moving LEFT (4) - NUMBERS WORKING!")
            self.game.player_manager.move_cursor_player1(-1, 0)
        elif key == 54 or char == '6':  # 6 key
            print("⚡ Player 1: Moving RIGHT (6) - NUMBERS WORKING!")
            self.game.player_manager.move_cursor_player1(1, 0)
        elif key == 53 or key == 48 or char == '5' or char == '0':  # 5 or 0 key
            print("⚡ Player 1: Selecting piece (5 or 0) - NUMBERS WORKING!")
            self.game.player_manager.select_piece_player1()
        elif key in [13, 10, 39, 226, 249]:  # Enter - multiple codes for different systems
            print(f"⚡ Player 1: Selecting piece (Enter code: {key}) - ENTER WORKING!")
            self.game.player_manager.select_piece_player1()
        
        else:
            if not wasd_detected:
                print(f"❓ Unknown key: {key}")
                if 32 <= key <= 126:
                    print(f"   Character: '{chr(key)}'")
                # Add ASCII codes for common keys
                key_map = {
                    119: 'w', 115: 's', 97: 'a', 100: 'd',
                    87: 'W', 83: 'S', 65: 'A', 68: 'D',
                    56: '8', 50: '2', 52: '4', 54: '6'
                }
                if key in key_map:
                    print(f"   Mapped character: '{key_map[key]}'")
        
        print("=== KEY PROCESSING COMPLETE ===\n")
        return False  # Don't exit

    def show_frame(self) -> bool:
        """Show the current frame and handle window events with automatic focus."""
        # ודא פוקוס אוטומטי בכל פריים (רק אם צריך)
        if self.focus_attempts < self.max_focus_attempts:
            self._force_window_focus()
        
        # קלט ללא חסימה - רק 30ms המתנה מקסימום
        key = cv2.waitKey(30) & 0xFF
        
        # עבד קלט אם נלחץ מקש
        if key != 255 and key != -1:
            # איפוס ספירת פוקוס כי קלט עובד
            self.focus_attempts = self.max_focus_attempts
            
            if self.handle_keyboard_input(key):
                return False  # Exit if ESC was pressed
        
        return True
