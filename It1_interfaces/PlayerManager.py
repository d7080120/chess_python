"""
PlayerManager - מחלקה לניהול שני השחקנים והסמנים שלהם
"""
from Command import Command


class PlayerManager:
    def __init__(self, game_ref):
        """Initialize the player manager with reference to game."""
        self.game = game_ref
        
        # מערכת שני שחקנים - ללא תורות
        self.selected_piece_player1 = None  # הכלי הנבחר של שחקן 1 (מקשי מספרים)
        self.selected_piece_player2 = None  # הכלי הנבחר של שחקן 2 (WASD)
        self.cursor_pos_player1 = [0, 7]  # מיקום הסמן של שחקן 1 (כלים לבנים) - התחל ליד הכלים הלבנים בשורה 7
        self.cursor_pos_player2 = [0, 0]  # מיקום הסמן של שחקן 2 (כלים שחורים) - התחל ליד הכלים השחורים בשורה 0

    def move_cursor_player1(self, dx, dy):
        """Move player 1 cursor (numeric keys) - כלים לבנים."""
        old_pos = self.cursor_pos_player1.copy()
        new_x = max(0, min(7, self.cursor_pos_player1[0] + dx))
        new_y = max(0, min(7, self.cursor_pos_player1[1] + dy))
        self.cursor_pos_player1 = [new_x, new_y]
        print(f"⚡ שחקן 1 (מספרים): הזיז סמן מ-{old_pos} ל-{self.cursor_pos_player1}")

    def move_cursor_player2(self, dx, dy):
        """Move player 2 cursor (WASD) - כלים שחורים."""
        old_pos = self.cursor_pos_player2.copy()
        new_x = max(0, min(7, self.cursor_pos_player2[0] + dx))
        new_y = max(0, min(7, self.cursor_pos_player2[1] + dy))
        self.cursor_pos_player2 = [new_x, new_y]
        print(f"🔥 שחקן 2 (WASD): הזיז סמן מ-{old_pos} ל-{self.cursor_pos_player2}")

    def select_piece_player1(self):
        """Handle piece selection for player 1 (Enter key)."""
        x, y = self.cursor_pos_player1
        print(f"🎯 שחקן 1 מנסה לבחור כלי במיקום ({x}, {y})")
        print(f"PLAYER 1 SELECTION ATTEMPT AT POSITION ({x}, {y})")
        
        if self.selected_piece_player1 is None:
            # בחירת כלי חדש
            piece = self._find_piece_at_position(x, y)
            if piece and self._is_player_piece(piece, 1):
                self.selected_piece_player1 = piece
                print(f"✅ שחקן 1 בחר כלי: {piece.piece_id} במיקום ({x}, {y})")
                print(f"PLAYER 1 SELECTED PIECE: {piece.piece_id} AT ({x}, {y})")
            else:
                print(f"❌ שחקן 1: אין כלי לבן במיקום ({x}, {y})")
                print(f"PLAYER 1: NO WHITE PIECE AT ({x}, {y})")
                if piece:
                    is_white = self._is_player_piece(piece, 1)
                    print(f"כלי קיים: {piece.piece_id}, כלי לבן: {is_white}")
                    print(f"PIECE EXISTS: {piece.piece_id}, IS WHITE: {is_white}")
        else:
            # בדיקה אם מנסים להזיז לאותו מיקום (אנימציית קפיצה במקום)
            current_pos = self._get_piece_position(self.selected_piece_player1)
            if current_pos == (x, y):
                print(f"🦘 שחקן 1 מבצע קפיצה במקום לכלי: {self.selected_piece_player1.piece_id}")
                print(f"PLAYER 1 JUMP IN PLACE FOR PIECE: {self.selected_piece_player1.piece_id}")
                # בצע אנימציית קפיצה לאותו מיקום
                jump_cmd = Command(
                    timestamp=self.game.game_time_ms(),
                    piece_id=self.selected_piece_player1.piece_id,
                    type="jump",
                    target=current_pos,  # קפיצה לאותו מיקום
                    params=None
                )
                self.game.user_input_queue.put(jump_cmd)
                self.selected_piece_player1 = None
                return
            
            # הזזת הכלי הנבחר למיקום חדש
            print(f"🎯 שחקן 1 מזיז כלי {self.selected_piece_player1.piece_id} ל-({x}, {y})")
            print(f"PLAYER 1 MOVING PIECE {self.selected_piece_player1.piece_id} TO ({x}, {y})")
            self.game.move_validator.move_piece(self.selected_piece_player1, x, y, 1)
            self.selected_piece_player1 = None

    def select_piece_player2(self):
        """Handle piece selection for player 2 (Space key)."""
        x, y = self.cursor_pos_player2
        print(f"🎯 שחקן 2 מנסה לבחור כלי במיקום ({x}, {y})")
        
        if self.selected_piece_player2 is None:
            # בחירת כלי חדש
            piece = self._find_piece_at_position(x, y)
            if piece and self._is_player_piece(piece, 2):
                self.selected_piece_player2 = piece
                print(f"✅ שחקן 2 בחר כלי: {piece.piece_id} במיקום ({x}, {y})")
            else:
                print(f"❌ שחקן 2: אין כלי שחור במיקום ({x}, {y})")
                if piece:
                    is_black = self._is_player_piece(piece, 2)
                    print(f"כלי קיים: {piece.piece_id}, כלי שחור: {is_black}")
        else:
            # בדיקה אם מנסים להזיז לאותו מיקום (אנימציית קפיצה במקום)
            current_pos = self._get_piece_position(self.selected_piece_player2)
            if current_pos == (x, y):
                print(f"🦘 שחקן 2 מבצע קפיצה במקום לכלי: {self.selected_piece_player2.piece_id}")
                print(f"PLAYER 2 JUMP IN PLACE FOR PIECE: {self.selected_piece_player2.piece_id}")
                # בצע אנימציית קפיצה לאותו מיקום
                jump_cmd = Command(
                    timestamp=self.game.game_time_ms(),
                    piece_id=self.selected_piece_player2.piece_id,
                    type="jump",
                    target=current_pos,  # קפיצה לאותו מיקום
                    params=None
                )
                self.game.user_input_queue.put(jump_cmd)
                self.selected_piece_player2 = None
                return
            
            # הזזת הכלי הנבחר למיקום חדש
            print(f"🎯 שחקן 2 מזיז כלי {self.selected_piece_player2.piece_id} ל-({x}, {y})")
            self.game.move_validator.move_piece(self.selected_piece_player2, x, y, 2)
            self.selected_piece_player2 = None

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

    def _find_piece_at_position(self, x, y):
        """Find piece at given board position."""
        print(f"מחפש כלי במיקום ({x}, {y})")
        
        for piece in self.game.pieces:
            piece_found = False
            piece_pos = None
            
            # בדיקה אם לכלי יש _state עם _physics עם cell
            if hasattr(piece, '_state') and hasattr(piece._state, '_physics'):
                physics = piece._state._physics
                if hasattr(physics, 'cell'):
                    piece_pos = physics.cell
                    if physics.cell == (x, y):
                        piece_found = True
                        print(f"מצא כלי {piece.piece_id} במיקום {piece_pos} via _state._physics.cell")
            
            # פלטות נוספות - בדיקת מיקום ישיר
            elif hasattr(piece, 'x') and hasattr(piece, 'y'):
                piece_pos = (piece.x, piece.y)
                if piece.x == x and piece.y == y:
                    piece_found = True
                    print(f"מצא כלי {piece.piece_id} במיקום {piece_pos} via x,y")
            
            elif hasattr(piece, 'board_position'):
                piece_pos = piece.board_position
                if piece.board_position == (x, y):
                    piece_found = True
                    print(f"מצא כלי {piece.piece_id} במיקום {piece_pos} via board_position")
            
            # Debug - הצג את מיקום כל כלי
            if piece_pos:
                print(f"כלי {piece.piece_id} נמצא במיקום {piece_pos}")
            else:
                print(f"כלי {piece.piece_id} - לא נמצא מיקום!")
            
            if piece_found:
                return piece
        
        print(f"לא נמצא כלי במיקום ({x}, {y})")
        return None

    def _is_player_piece(self, piece, player_num):
        """Check if piece belongs to specified player."""
        # שחקן 1 = כלים לבנים (W), שחקן 2 = כלים שחורים (B)
        # הכלים עכשיו מזוהים כ-PW0, PW1, PB0, PB1, etc.
        if player_num == 1:
            return 'W' in piece.piece_id  # כלים לבנים
        else:
            return 'B' in piece.piece_id  # כלים שחורים
