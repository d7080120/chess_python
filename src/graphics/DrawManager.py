"""
DrawManager - מחלקה לציור המשחק, הסמנים, הניקוד וההיסטוריה
"""
import cv2
import numpy as np
import pathlib


class DrawManager:
    def __init__(self, game_ref):
        """Initialize the draw manager with reference to game."""
        self.game = game_ref
        self.background_img = None
        
        # גדלי המסך והלוח
        self.screen_width = 1200  # רוחב כולל
        self.screen_height = 800  # גובה כולל
        self.board_size = 600     # גודל הלוח הפנימי
        self.board_x = (self.screen_width - self.board_size) // 2  # מרכז אופקי
        self.board_y = (self.screen_height - self.board_size) // 2  # מרכז אנכי
        
        # אזורי הטקסט
        self.left_panel_x = 50
        self.right_panel_x = self.board_x + self.board_size + 50
        self.panel_width = 150

    def draw_game(self):
        """Draw the current game state with score and move history."""
        # צור עותק נקי של הלוח לכל פריים
        display_board = self.game.clone_board()
        
        # ציור כל הכלים על העותק
        now = self.game.game_time_ms()
        for p in self.game.pieces:
            p.draw_on_board(display_board, now)
        
        # ציור סמנים של השחקנים
        self._draw_cursors(display_board)
        
        # יצירת canvas רחב יותר עם רקע לניקוד והיסטוריה
        enhanced_display = self._create_enhanced_display(display_board)
        
        # הצגה
        if enhanced_display is not None:
            cv2.imshow("Chess Game", enhanced_display)

    def _create_enhanced_display(self, board):
        """Create enhanced display with score and move history on sides"""
        if not hasattr(board, "img") or board.img is None or not hasattr(board.img, "img"):
            return None
            
        board_img = board.img.img
        board_height, board_width = board_img.shape[:2]
        
        # יצירת canvas רחב יותר (לוח + 2 פאנלים בצדדים)
        panel_width = 300  # רוחב הפאנל בכל צד
        total_width = board_width + (2 * panel_width)
        
        # יצירת רקע (נסה לטעון background.png או צור רקע אחיד)
        background = self._create_background(total_width, board_height)
        
        # מיקום הלוח במרכז
        board_x_offset = panel_width
        
        # המרת צבעים אם נחוץ (RGBA לRGB)
        if len(board_img.shape) == 3 and board_img.shape[2] == 4:
            # המרה מ-RGBA ל-RGB
            board_img = cv2.cvtColor(board_img, cv2.COLOR_RGBA2RGB)
        elif len(board_img.shape) == 3 and board_img.shape[2] == 3:
            # כבר RGB, אין צורך בהמרה
            pass
        
        background[0:board_height, board_x_offset:board_x_offset + board_width] = board_img
        
        # ציור הפאנלים
        self._draw_left_panel(background, 0, panel_width, board_height)  # Player 1 (White)
        self._draw_right_panel(background, board_x_offset + board_width, panel_width, board_height)  # Player 2 (Black)
        
        return background

    def _create_background(self, width, height):
        """Create or load background image"""
        try:
            # נסה לטעון background.png
            import pathlib
            bg_path = pathlib.Path(__file__).parent.parent.parent / "assets" / "images" / "background.png"
            if bg_path.exists():
                bg_img = cv2.imread(str(bg_path))
                if bg_img is not None:
                    return cv2.resize(bg_img, (width, height))
        except:
            pass
        
        # אם אין רקע, צור רקע כהה אלגנטי
        background = np.zeros((height, width, 3), dtype=np.uint8)
        background[:] = (40, 40, 40)  # רקע אפור כהה
        return background

    def _draw_left_panel(self, img, x_start, width, height):
        """Draw left panel for Player 1 (White)"""
        # קבל שם השחקן
        player_name = self.game.player_name_manager.get_player1_name()
        
        # כותרת עם שם השחקן
        cv2.rectangle(img, (x_start, 0), (x_start + width, 80), (200, 200, 255), -1)  # רקע כחול בהיר - יותר גבוה
        
        # שם השחקן - גופן מעוצב יותר
        cv2.putText(img, player_name, (x_start + 10, 30), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 2)
        cv2.putText(img, "(WHITE)", (x_start + 10, 60), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 2)
        
        # ניקוד - גופן מעוצב יותר
        if hasattr(self.game, 'score_manager'):
            score1, _ = self.game.score_manager.get_scores()
            cv2.putText(img, f"Score: {score1}", (x_start + 10, 110), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 2)  # Changed to black
        
        # היסטוריית מהלכים - כותרת מעוצבת יותר
        cv2.putText(img, "Recent Moves:", (x_start + 10, 150), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.7, (200, 200, 200), 2)
        
        if hasattr(self.game, 'score_manager'):
            moves_with_numbers = self.game.score_manager.get_player1_recent_moves_with_numbers(10)
            # רקע לבן קטן למהלכים (כמו דף נייר)
            if moves_with_numbers:
                moves_bg_height = min(len(moves_with_numbers) * 35 + 20, height - 200)
                cv2.rectangle(img, (x_start + 5, 175), (x_start + width - 5, 175 + moves_bg_height), 
                             (240, 240, 240), -1)  # רקע לבן
                cv2.rectangle(img, (x_start + 5, 175), (x_start + width - 5, 175 + moves_bg_height), 
                             (180, 180, 180), 2)   # גבול אפור
            
            for i, (move_number, move) in enumerate(moves_with_numbers):
                y = 195 + (i * 35)  # רווח גדול יותר בין המהלכים
                if y > height - 40:
                    break
                # מהלכים בגופן מעוצב וברור יותר - מספור אמיתי מתחילת המשחק - שחקן 1
                cv2.putText(img, f"{move_number}. {move}", (x_start + 15, y), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 2)  # טקסט שחור על רקע לבן

    def _draw_right_panel(self, img, x_start, width, height):
        """Draw right panel for Player 2 (Black)"""
        # קבל שם השחקן
        player_name = self.game.player_name_manager.get_player2_name()
        
        # כותרת עם שם השחקן
        cv2.rectangle(img, (x_start, 0), (x_start + width, 80), (100, 100, 100), -1)  # רקע אפור כהה - יותר גבוה
        
        # שם השחקן - גופן מעוצב יותר
        cv2.putText(img, player_name, (x_start + 10, 30), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
        cv2.putText(img, "(BLACK)", (x_start + 10, 60), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)
        
        # ניקוד - גופן מעוצב יותר
        if hasattr(self.game, 'score_manager'):
            _, score2 = self.game.score_manager.get_scores()
            cv2.putText(img, f"Score: {score2}", (x_start + 10, 110), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 0), 2)  # Changed to black
        
        # היסטוריית מהלכים - כותרת מעוצבת יותר
        cv2.putText(img, "Recent Moves:", (x_start + 10, 150), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.7, (200, 200, 200), 2)
        
        if hasattr(self.game, 'score_manager'):
            moves_with_numbers = self.game.score_manager.get_player2_recent_moves_with_numbers(10)
            # רקע לבן קטן למהלכים (כמו דף נייר)
            if moves_with_numbers:
                moves_bg_height = min(len(moves_with_numbers) * 35 + 20, height - 200)
                cv2.rectangle(img, (x_start + 5, 175), (x_start + width - 5, 175 + moves_bg_height), 
                             (240, 240, 240), -1)  # רקע לבן
                cv2.rectangle(img, (x_start + 5, 175), (x_start + width - 5, 175 + moves_bg_height), 
                             (180, 180, 180), 2)   # גבול אפור
            
            for i, (move_number, move) in enumerate(moves_with_numbers):
                y = 195 + (i * 35)  # רווח גדול יותר בין המהלכים
                if y > height - 40:
                    break
                # מהלכים בגופן מעוצב וברור יותר - מספור אמיתי מתחילת המשחק - שחקן 2
                cv2.putText(img, f"{move_number}. {move}", (x_start + 15, y), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 2)  # טקסט שחור על רקע לבן

    def _draw_cursors(self, board):
        """Draw player cursors on the board."""
        if hasattr(board, 'img') and hasattr(board.img, 'img'):
            img = board.img.img
            
            # חישוב גודל משבצת
            board_height, board_width = img.shape[:2]
            cell_width = board_width // 8
            cell_height = board_height // 8
            
            # ציור סמן שחקן 1 (כחול עבה - מסגרת חיצונית)
            x1, y1 = self.game.player_manager.cursor_pos_player1
            top_left_1 = (x1 * cell_width, y1 * cell_height)
            bottom_right_1 = ((x1 + 1) * cell_width - 1, (y1 + 1) * cell_height - 1)
            cv2.rectangle(img, top_left_1, bottom_right_1, (255, 0, 0), 8)  # כחול BGR עבה מאוד
            
            # ציור סמן שחקן 2 (אדום דק יותר - מסגרת חיצונית, יופיע מעל שחקן 1)
            x2, y2 = self.game.player_manager.cursor_pos_player2
            top_left_2 = (x2 * cell_width, y2 * cell_height)
            bottom_right_2 = ((x2 + 1) * cell_width - 1, (y2 + 1) * cell_height - 1)
            cv2.rectangle(img, top_left_2, bottom_right_2, (0, 0, 255), 5)  # אדום BGR דק יותר, יצויר מעל הכחול
            
            # סימון כלי נבחר - צריך להיות על הכלי עצמו, לא על הסמן
            if self.game.player_manager.selected_piece_player1:
                # מצא את מיקום הכלי הנבחר של שחקן 1
                piece_pos = self._get_piece_position(self.game.player_manager.selected_piece_player1)
                if piece_pos:
                    px, py = piece_pos
                    piece_top_left = (px * cell_width, py * cell_height)
                    piece_bottom_right = ((px + 1) * cell_width - 1, (py + 1) * cell_height - 1)
                    cv2.rectangle(img, piece_top_left, piece_bottom_right, (0, 255, 0), 4)  # ירוק עבה
            
            if self.game.player_manager.selected_piece_player2:
                # מצא את מיקום הכלי הנבחר של שחקן 2
                piece_pos = self._get_piece_position(self.game.player_manager.selected_piece_player2)
                if piece_pos:
                    px, py = piece_pos
                    piece_top_left = (px * cell_width, py * cell_height)
                    piece_bottom_right = ((px + 1) * cell_width - 1, (py + 1) * cell_height - 1)
                    cv2.rectangle(img, piece_top_left, piece_bottom_right, (0, 255, 255), 4)  # צהוב עבה

    def _get_piece_position(self, piece):
        """Get the current position of a piece."""
        if not piece:
            return None
            
        # בדיקה אם לכלי יש _state עם _physics עם cell
        if hasattr(piece, '_state') and hasattr(piece._state, '_physics'):
            physics = piece._state._physics
            if hasattr(physics, 'cell'):
                return physics.cell
        
        # פלטות נוספות
        if hasattr(piece, 'x') and hasattr(piece, 'y'):
            return (piece.x, piece.y)
        
        if hasattr(piece, 'board_position'):
            return piece.board_position
        
        return None
