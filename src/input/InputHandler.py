"""
InputHandler - מחלקה פשוטה לטיפול בקלט עם פוקוס אוטומטי
"""
import cv2
from src.ui.WindowFocusManager import WindowFocusManager
from src.ui.window_settings import GAME_WINDOW_POSITION


class InputHandler:
    def __init__(self, game_ref):
        """Initialize the input handler with game reference."""
        self.game = game_ref
        self.focus_manager = WindowFocusManager("Chess Game", GAME_WINDOW_POSITION)
        self.last_key = None
        self.window_created = False  # דגל שהחלון לא נוצר עדיין

    def ensure_window_created(self):
        """Create window only when needed"""
        if not self.window_created:
            self.focus_manager.create_focused_window()
            self.window_created = True

    def show_frame(self) -> bool:
        """Show the current frame and handle window events with auto-focus."""
        # יצירת חלון רק כשצריך
        self.ensure_window_created()
        
        # בדיקה חכמה של פוקוס - רק אם נדרש
        self.focus_manager.smart_focus_check()
        
        # קלט ללא חסימה
        key = cv2.waitKey(30) & 0xFF
        
        # עבד קלט אם נלחץ מקש
        if key != 255 and key != -1:
            self.last_key = key
            if self.handle_keyboard_input(key):
                return False  # Exit if ESC was pressed
        
        return True

    def handle_keyboard_input(self, key) -> bool:
        """Handle keyboard input. Returns True if should exit game."""
        
        # Convert key to character for debugging
        char = chr(key) if 32 <= key <= 126 else None
        
        # Exit keys
        if key == 27 or key == 113 or char == 'q':  # ESC or Q
            print("Exiting game...")
            return True
        
        wasd_detected = False
        
        # Player 2 controls - WASD - שחקן 2 שולט בכלים שחורים
        # W key (UP)
        if key in [119, 87] or char == 'w' or char == 'W':
            self.game.player_manager.move_cursor_player2(0, -1)
            wasd_detected = True
        # S key (DOWN)
        elif key in [115, 83] or char == 's' or char == 'S':
            self.game.player_manager.move_cursor_player2(0, 1)
            wasd_detected = True
        # A key (LEFT)
        elif key in [97, 65] or char == 'a' or char == 'A':
            self.game.player_manager.move_cursor_player2(-1, 0)
            wasd_detected = True
        # D key (RIGHT)
        elif key in [100, 68] or char == 'd' or char == 'D':
            self.game.player_manager.move_cursor_player2(1, 0)
            wasd_detected = True
        elif key == 32 or char == ' ':  # Space
            self.game.player_manager.select_piece_player2()
            wasd_detected = True
        
        # Player 1 controls - מקשי מספרים - שחקן 1 שולט בכלים לבנים
        elif key == 56 or char == '8':  # 8 key
            self.game.player_manager.move_cursor_player1(0, -1)
        elif key == 50 or char == '2':  # 2 key
            self.game.player_manager.move_cursor_player1(0, 1)
        elif key == 52 or char == '4':  # 4 key
            self.game.player_manager.move_cursor_player1(-1, 0)
        elif key == 54 or char == '6':  # 6 key
            self.game.player_manager.move_cursor_player1(1, 0)
        elif key == 53 or key == 48 or char == '5' or char == '0':  # 5 or 0 key
            self.game.player_manager.select_piece_player1()
        elif key in [13, 10]:  # Enter
            self.game.player_manager.select_piece_player1()
        
        return False  # Don't exit
