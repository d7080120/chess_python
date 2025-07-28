"""
CaptureHandler - מחלקה לטיפול בתפיסות וביטול כלים
"""
import pathlib
from Command import Command


class CaptureHandler:
    def __init__(self, game_ref):
        """Initialize the capture handler with reference to game."""
        self.game = game_ref

    def handle_arrival(self, cmd: Command):
        """Handle piece arrival and check for captures."""
        print(f"🏁 כלי הגיע ליעד: {cmd.piece_id}")
        
        # מצא את הכלי שהגיע ליעד
        arriving_piece = None
        for piece in self.game.pieces:
            if piece.piece_id == cmd.piece_id:
                arriving_piece = piece
                break
        
        if not arriving_piece:
            print(f"❌ לא נמצא כלי שהגיע: {cmd.piece_id}")
            return
        
        # קבל את המיקום של הכלי שהגיע
        target_pos = arriving_piece._state._physics.cell
        
        # נניח שהכלי הגיע ממיקום קודם - נשתמש במיקום הנוכחי כמיקום מוצא
        from_pos = target_pos  # זה לא מדויק אבל יעבוד לעכשיו
        
        # בדוק הכתרת חיילים לפני בדיקת תפיסה
        self._check_pawn_promotion(arriving_piece, target_pos)
        
        print(f"🎯 בודק תפיסה במיקום {target_pos}")
        print(f"🔍 רשימת כל הכלים והמיקומים שלהם:")
        
        # הצג את כל הכלים והמיקומים שלהם
        for piece in self.game.pieces:
            piece_pos = piece._state._physics.cell
            print(f"   {piece.piece_id} במיקום {piece_pos}")
        
        # חפש כלי יריב באותו מיקום
        pieces_to_remove = []
        for piece in self.game.pieces:
            if piece != arriving_piece:  # לא אותו כלי
                piece_pos = piece._state._physics.cell
                print(f"🔍 בודק {piece.piece_id} במיקום {piece_pos} מול {target_pos}")
                if piece_pos == target_pos:
                    # בדוק אם זה כלי יריב
                    arriving_is_white = 'W' in arriving_piece.piece_id
                    piece_is_white = 'W' in piece.piece_id
                    
                    print(f"🎯 מצאתי כלי באותו מיקום! {piece.piece_id} (לבן: {piece_is_white}) vs {arriving_piece.piece_id} (לבן: {arriving_is_white})")
                    
                    if arriving_is_white != piece_is_white:  # צבעים שונים = יריבים
                        print(f"⚔️ {arriving_piece.piece_id} תפס את {piece.piece_id} במיקום {target_pos}!")
                        pieces_to_remove.append(piece)
                        
                        # עדכן את מנהל הניקוד
                        if hasattr(self.game, 'score_manager'):
                            self.game.score_manager.record_move(
                                arriving_piece.piece_id, 
                                from_pos, 
                                target_pos, 
                                "capture", 
                                piece.piece_id
                            )
                        
                        # בדיקה מיוחדת למלכים
                        if piece.piece_id in ["KW0", "KB0"]:
                            print(f"🚨🚨 CRITICAL: KING CAPTURED! {piece.piece_id} was taken! 🚨🚨🚨")
                            print(f"💀 מלך נהרג: {piece.piece_id}")
                            print(f"🔥 זה יגרום לסיום המשחק!")
                    else:
                        print(f"🛡️ אותו צבע - לא תוקף: {piece.piece_id} ו-{arriving_piece.piece_id}")
        
        print(f"📋 כלים לתפיסה: {[p.piece_id for p in pieces_to_remove]}")
        
        # הסר את הכלים הנתפסים
        for piece in pieces_to_remove:
            if piece in self.game.pieces:
                self.game.pieces.remove(piece)
                print(f"🗑️ הסרתי {piece.piece_id} מרשימת הכלים")
                
                # DEBUG נוסף - ספירת מלכים אחרי הסרה
                if piece.piece_id in ["KW0", "KB0"]:
                    remaining_kings = [p.piece_id for p in self.game.pieces if p.piece_id in ["KW0", "KB0"]]
                    print(f"👑 מלכים שנותרו אחרי הסרת {piece.piece_id}: {remaining_kings}")
                    print(f"📊 סה'כ כלים נותרים: {len(self.game.pieces)}")
                    
                    # בדיקה מיידית של תנאי נצחון
                    white_kings = [p for p in self.game.pieces if p.piece_id == "KW0"]
                    black_kings = [p for p in self.game.pieces if p.piece_id == "KB0"]
                    print(f"🔍 מלכים לבנים: {len(white_kings)}, מלכים שחורים: {len(black_kings)}")
                    
                    if len(white_kings) == 0:
                        print("🏆 אין מלך לבן - שחקן 2 אמור לנצח!")
                    if len(black_kings) == 0:
                        print("🏆 אין מלך שחור - שחקן 1 אמור לנצח!")
        
        # בדוק תנאי נצחון אחרי תפיסה
        if pieces_to_remove:
            if self.game.win_checker.is_win():
                self.game.win_checker.announce_win()
                self.game.game_over = True  # סמן שהמשחק נגמר מיד אחרי נצחון

    def _check_pawn_promotion(self, piece, target_pos):
        """Check if a pawn should be promoted to queen."""
        # בדוק אם זה חייל
        if not piece.piece_id.startswith('P'):
            return  # לא חייל - אין הכתרה
            
        col, row = target_pos  # target_pos הוא (x, y) = (col, row)
        is_white_pawn = 'W' in piece.piece_id
        is_black_pawn = 'B' in piece.piece_id
        
        # בדוק אם החייל הגיע לשורה המתאימה להכתרה
        should_promote = False
        new_piece_type = None
        
        if is_white_pawn and row == 0:  # חייל לבן הגיע לשורה 0
            should_promote = True
            new_piece_type = "QW"
            print(f"👑 חייל לבן {piece.piece_id} הגיע לשורה 0 - הכתרה למלכה!")
        elif is_black_pawn and row == 7:  # חייל שחור הגיע לשורה 7
            should_promote = True
            new_piece_type = "QB"
            print(f"👑 חייל שחור {piece.piece_id} הגיע לשורה 7 - הכתרה למלכה!")
            
        if should_promote:
            self._promote_pawn_to_queen(piece, new_piece_type, target_pos)

    def _promote_pawn_to_queen(self, pawn, queen_type, position):
        """Replace a pawn with a queen at the given position."""
        print(f"🎆 מבצע הכתרה: {pawn.piece_id} -> {queen_type} במיקום {position}")
        pieces_root = pathlib.Path(__file__).parent.parent / "pieces"
        
        # צור מלכה חדשה
        from PieceFactory import PieceFactory
        factory = PieceFactory(self.game.board, pieces_root)
        
        # יצירת ID ייחודי למלכה החדשה
        existing_queens = [p for p in self.game.pieces if p.piece_id.startswith(queen_type)]
        queen_id = f"{queen_type}{len(existing_queens)}"
        
        # צור מלכה חדשה במיקום הנדרש
        new_queen = factory.create_piece(queen_type, position, self.game.user_input_queue)
        new_queen.piece_id = queen_id
        new_queen._state._physics.piece_id = queen_id
        
        # הסר את החייל הישן והוסף את המלכה החדשה
        if pawn in self.game.pieces:
            self.game.pieces.remove(pawn)
            print(f"🗑️ הסרתי חייל: {pawn.piece_id}")
            
        self.game.pieces.append(new_queen)
        print(f"👑 הוספתי מלכה חדשה: {queen_id} במיקום {position}")
        print(f"🎉 הכתרה הושלמה בהצלחה! {pawn.piece_id} -> {queen_id}")
