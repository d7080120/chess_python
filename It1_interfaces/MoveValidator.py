"""
MoveValidator - מחלקה לבדיקת חוקיות מהלכים והזזת כלים
"""
from Command import Command


class MoveValidator:
    def __init__(self, game_ref):
        """Initialize the move validator with reference to game."""
        self.game = game_ref

    def move_piece(self, piece, new_x, new_y, player_num):
        """Move piece to new position using Command system."""
        # בדיקה שהמהלך חוקי
        if not self._is_valid_move(piece, new_x, new_y, player_num):
            print(f"❌ מהלך לא חוקי ל-{piece.piece_id} ל-({new_x}, {new_y})")
            return
        
        # מיקום נוכחי של הכלי
        current_pos = self._get_piece_position(piece)
        if not current_pos:
            print(f"❌ לא ניתן למצוא מיקום נוכחי של {piece.piece_id}")
            return
        
        current_x, current_y = current_pos
        
        # בדיקת נתיב - האם יש כלים בדרך (רק אחרי שהתנועה תקינה!)
        blocking_position = self._check_path(current_x, current_y, new_x, new_y, piece.piece_id)
        
        # אם יש כלי חוסם בדרך, עדכן את מיקום היעד למיקום של הכלי החוסם
        final_x, final_y = new_x, new_y
        if blocking_position:
            final_x, final_y = blocking_position
            print(f"🎯 מעדכן יעד בגלל כלי חוסם: מ-({new_x}, {new_y}) ל-({final_x}, {final_y})")
        
        # בדיקה אם יש כלי במיקום המטרה הסופי
        target_piece = self._get_piece_at_position(final_x, final_y)
        if target_piece:
            # בדוק אם זה כלי של האויב (אפשר לתפוס)
            if self._is_player_piece(target_piece, player_num):
                print(f"❌ לא ניתן לתפוס כלי של אותו שחקן: {target_piece.piece_id}")
                return
            else:
                print(f"⚔️ {piece.piece_id} תופס את {target_piece.piece_id}!")
                # בדיקה מיוחדת למלכים - DEBUG מורחב!
                if target_piece.piece_id in ["KW0", "KB0"]:
                    print(f"🚨🚨 CRITICAL: KING CAPTURED! {target_piece.piece_id} was taken! 🚨🚨🚨")
                    print(f"💀 מלך נהרג: {target_piece.piece_id}")
                    print(f"🔥 זה אמור לגרום לסיום המשחק מיד!")
                    
                # לא מוחקים את הכלי כאן - זה יקרה ב-_handle_arrival כשהכלי יגיע!
        
        # יצירת פקודת תנועה - כל הכלים יכולים לזוז בתנועה חלקה
        command_type = "move"
        
        # תיעוד המהלך במערכת הניקוד
        is_capture = target_piece is not None
        captured_piece_id = target_piece.piece_id if target_piece else None
        
        if hasattr(self.game, 'score_manager'):
            move_type = "capture" if is_capture else "move"
            self.game.score_manager.record_move(
                piece.piece_id, current_pos, (final_x, final_y), 
                move_type, captured_piece_id
            )
        
        move_cmd = Command(
            timestamp=self.game.game_time_ms(),
            piece_id=piece.piece_id,
            type=command_type,
            target=(final_x, final_y),  # שימוש במיקום המעודכן
            params=None
        )
        
        # הוספת הפקודה לתור - State.process_command יטפל במכונת המצבים
        self.game.user_input_queue.put(move_cmd)
        
        print(f"🎯 שחקן {player_num}: שלח פקודת {command_type} ל-{piece.piece_id} ל-({final_x}, {final_y})")
        print(f"PLAYER {player_num}: Sent {command_type} command for {piece.piece_id} to ({final_x}, {final_y})")
        # ללא החלפת תור - כל שחקן יכול לזוז מתי שהוא רוצה

    def _check_path(self, start_x, start_y, end_x, end_y, piece_type):
        """Check if path is clear and return first blocking piece position if any."""
        # סוסים יכולים לקפוץ מעל כלים
        if piece_type.startswith('N'):  # Knight - no path checking
            return None
        
        dx = end_x - start_x
        dy = end_y - start_y
        
        # מלכים יכולים לזוז משבצת אחת בכל כיוון - אין צורך בבדיקת נתיב
        if piece_type.startswith('K') and abs(dx) <= 1 and abs(dy) <= 1:
            return None
        
        # חישוב כיוון התנועה
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
        
        # בדיקת נתיב - בלי לכלול את נקודות ההתחלה והסיום
        current_x = start_x + step_x
        current_y = start_y + step_y
        
        while current_x != end_x or current_y != end_y:
            # בדיקה אם יש כלי במשבצת הנוכחית
            blocking_piece = self._get_piece_at_position(current_x, current_y)
            if blocking_piece:
                print(f"🚫 נתיב חסום! כלי {blocking_piece.piece_id} במיקום ({current_x}, {current_y})")
                return (current_x, current_y)  # מחזיר את מיקום הכלי החוסם
            
            # מעבר למשבצת הבאה
            current_x += step_x
            current_y += step_y
        
        print(f"✅ נתיב פנוי מ-({start_x}, {start_y}) ל-({end_x}, {end_y})")
        return None  # נתיב פנוי

    def _is_valid_move(self, piece, new_x, new_y, player_num):
        """Check if move is valid based on piece type and rules."""
        # בדיקה בסיסית - בגבולות הלוח
        if not (0 <= new_x <= 7 and 0 <= new_y <= 7):
            return False
        
        # מיקום נוכחי של הכלי
        current_pos = self._get_piece_position(piece)
        if not current_pos:
            return False
        
        current_x, current_y = current_pos
        
        # חישוב ההפרש
        dx = new_x - current_x
        dy = new_y - current_y
        
        # בדיקה אם יש כלי במיקום המטרה
        target_piece = self._get_piece_at_position(new_x, new_y)
        is_capture = target_piece is not None
        
        # קריאת הנתונים מקובץ התנועות של הכלי - קודם נבדוק אם התנועה חוקית
        if hasattr(piece._state, '_moves') and hasattr(piece._state._moves, 'valid_moves'):
            valid_moves = piece._state._moves.valid_moves
            print(f"🔍 בודק תנועה: {piece.piece_id} מ-({current_x},{current_y}) ל-({new_x},{new_y}), הפרש: ({dx},{dy})")
            print(f"🔍 תנועות אפשריות: {valid_moves}")
            
            move_is_valid = False
            
            # בדיקה לכל תנועה אפשרית - רק קואורדינטות, בלי סוגי תנועה
            for move_dx, move_dy, move_type in valid_moves:
                # קבצי התנועות של חילים: צריך להפוך את הכיוון
                # החילים הלבנים והשחורים הפוכים במערכת הקואורדינטות
                if piece.piece_id.startswith('P'):  # חילים - הפך כיוון
                    # הקובץ אומר (0,-1) וזה צריך להישאר (0,-1)
                    actual_dx = move_dx  # השאר כמו שזה
                    actual_dy = move_dy  # השאר כמו שזה
                else:  # כל שאר הכלים - use as is
                    actual_dx = move_dx
                    actual_dy = move_dy
                
                print(f"🔍 בודק תנועה ({move_dx},{move_dy},{move_type}) -> מתורגם: ({actual_dx},{actual_dy})")
                
                # בדיקה אם התנועה תואמת - רק קואורדינטות!
                if dx == actual_dx and dy == actual_dy:
                    print(f"✅ תנועה תואמת! הפרש ({dx},{dy}) = קואורדינטות ({actual_dx},{actual_dy})")
                    move_is_valid = True
                    break
            
            if not move_is_valid:
                print(f"❌ לא נמצאה תנועה תואמת")
                return False
            
            # כעת, אחרי שאנחנו יודעים שהתנועה חוקית לפי הקבצים, נבדוק נתיב
            blocking_position = self._check_path(current_x, current_y, new_x, new_y, piece.piece_id)
            
            # אם יש כלי חוסם בדרך ואנחנו לא מנסים לזוז למיקום שלו
            if blocking_position and blocking_position != (new_x, new_y):
                print(f"🚫 תנועה לא חוקית: נתיב חסום על ידי כלי במיקום {blocking_position}")
                return False
            
            print(f"✅ תנועה חוקית!")
            return True
        else:
            print(f"❌ אין נתוני תנועות לכלי {piece.piece_id}")
            return False

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

    def _get_piece_at_position(self, x, y):
        """Get piece at specific position, if any."""
        for piece in self.game.pieces:
            piece_pos = self._get_piece_position(piece)
            if piece_pos and piece_pos == (x, y):
                return piece
        return None

    def _is_player_piece(self, piece, player_num):
        """Check if piece belongs to specified player."""
        # שחקן 1 = כלים לבנים (W), שחקן 2 = כלים שחורים (B)
        # הכלים עכשיו מזוהים כ-PW0, PW1, PB0, PB1, etc.
        if player_num == 1:
            return 'W' in piece.piece_id  # כלים לבנים
        else:
            return 'B' in piece.piece_id  # כלים שחורים
