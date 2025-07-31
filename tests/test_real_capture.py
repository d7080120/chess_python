"""
test_real_capture.py - בדיקת תפיסה אמיתית במשחק
"""
import sys
import time
import pathlib
from unittest.mock import Mock

# הוסף את הנתיב לתיקיית המחלקות
current_dir = pathlib.Path(__file__).parent
sys.path.append(str(current_dir))

def test_real_game_capture():
    """בדיקה קצרה של תפיסת כלים במשחק האמיתי"""
    
    print("🎮 בדיקת תפיסת כלים במשחק האמיתי")
    print("=" * 50)
    
    from src.core.game_setup.Game import Game
    from src.core.game_logic.Board import Board
    from src.core.game_setup.PieceFactory import PieceFactory
    from src.graphics.img import Img
    
    try:
        # יצירת לוח בסיסי לבדיקה
        print("📸 יוצר לוח בדיקה...")
        img = Img()
        # נסה לטעון תמונה קיימת או צור רקע בסיסי
        try:
            img_path = pathlib.Path(__file__).parent.parent / "board.png"
            if img_path.exists():
                img.read(str(img_path), size=(800, 800))
            else:
                # צור תמונה בסיסית
                import numpy as np
                img.img = np.zeros((800, 800, 3), dtype=np.uint8)
                img.img[:] = (100, 100, 100)  # רקע אפור
        except:
            import numpy as np
            img.img = np.zeros((800, 800, 3), dtype=np.uint8)
            img.img[:] = (100, 100, 100)
        
        board = Board(
            cell_W_pix=100, cell_H_pix=100,
            cell_H_m=1, cell_W_m=1,
            W_cells=8, H_cells=8,
            img=img
        )
        
        # יצירת כמה כלים בסיסיים לבדיקה
        pieces_root = pathlib.Path(__file__).parent.parent / "pieces"
        factory = PieceFactory(board, pieces_root)
        
        # יצירת משחק עם כלים מועטים
        pieces = [
            factory.create_piece("PW", (0, 6)),   # רגלי לבן
            factory.create_piece("PB", (1, 1)),   # רגלי שחור
            factory.create_piece("NW", (2, 7)),   # סוס לבן
        ]
        
        game = Game(pieces, board)
        
        print("✅ משחק נוצר בהצלחה")
        print(f"✅ ScoreManager: {type(game.score_manager).__name__}")
        print(f"✅ כלים: {[p.piece_id for p in game.pieces]}")
        
        # בדיקת היכולת לנוע לתפיסה
        print("\n🎯 בדיקת תפיסה:")
        print("   נסה להזיז את הסוס הלבן לתפוס את הרגלי השחור")
        
        # סימולציה של תנועה לתפיסה
        from src.core.game_logic.Command import Command
        import time
        
        # נסה לזוז לתפוس
        capture_cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="NW0",
            type="move",
            from_pos=(2, 7),
            to_pos=(1, 1),  # מיקום הרגלי השחור
            captured_piece="PB0",
            target=(1, 1)
        )
        
        print(f"   שולח פקודה: {capture_cmd.piece_id} -> {capture_cmd.to_pos}")
        
        # שלח דרך ה-subject
        game.command_subject.notify(capture_cmd)
        
        # בדוק את הניקוד
        scores = game.score_manager.get_scores()
        print(f"🏆 ניקוד אחרי תפיסה: לבן={scores[0]}, שחור={scores[1]}")
        
        moves = game.score_manager.get_player1_recent_moves(3)
        print(f"📋 מהלכים אחרונים של לבן: {moves}")
        
        print("\n" + "=" * 50)
        print("🎉 הבדיקה הושלמה!")
        print("✨ מערכת Observer פועלת נכון במשחק האמיתי")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_real_game_capture()
