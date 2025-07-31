"""
Test script for the refactored Game classes
"""
import sys
import pathlib

# הוסף את הנתיב לתיקיית המחלקות
current_dir = pathlib.Path(__file__).parent
sys.path.append(str(current_dir))

from src.core.game_setup.Game import Game
from src.core.game_logic.Board import Board
from src.core.game_setup.PieceFactory import PieceFactory


def test_refactored_game():
    """Test the refactored game implementation."""
    print("🧪 בודק את המחלקות החדשות...")
    
    try:
        # צור לוח
        board_path = current_dir.parent / "pieces" / "board.csv"
        board = Board(board_path)
        print("✅ לוח נוצר בהצלחה")
        
        # צור מפעל כלים
        pieces_root = current_dir.parent / "pieces"
        factory = PieceFactory(board, pieces_root)
        print("✅ מפעל כלים נוצר בהצלחה")
        
        # צור כמה כלים לבדיקה
        pieces = []
        
        # הוסף מלכים
        king_white = factory.create_piece("KW", (4, 7), None)
        king_black = factory.create_piece("KB", (4, 0), None)
        pieces.extend([king_white, king_black])
        print("✅ מלכים נוצרו בהצלחה")
        
        # צור משחק מחודש
        game = Game(pieces, board)
        print("✅ משחק מחודש נוצר בהצלחה")
        
        # בדוק שכל המחלקות המסייעות קיימות
        assert hasattr(game, 'input_handler'), "InputHandler חסר"
        assert hasattr(game, 'player_manager'), "PlayerManager חסר"
        assert hasattr(game, 'draw_manager'), "DrawManager חסר"
        assert hasattr(game, 'capture_handler'), "CaptureHandler חסר"
        assert hasattr(game, 'win_checker'), "WinChecker חסר"
        assert hasattr(game, 'move_validator'), "MoveValidator חסר"
        print("✅ כל המחלקות המסייעות קיימות")
        
        # בדוק פונקציות בסיסיות
        assert callable(game.game_time_ms), "game_time_ms לא פונקציה"
        assert callable(game.clone_board), "clone_board לא פונקציה"
        print("✅ פונקציות בסיסיות עובדות")
        
        # בדוק שהמחלקות המסייעות מחוברות נכון למשחק
        assert game.input_handler.game == game, "InputHandler לא מחובר למשחק"
        assert game.player_manager.game == game, "PlayerManager לא מחובר למשחק"
        assert game.draw_manager.game == game, "DrawManager לא מחובר למשחק"
        assert game.capture_handler.game == game, "CaptureHandler לא מחובר למשחק"
        assert game.win_checker.game == game, "WinChecker לא מחובר למשחק"
        assert game.move_validator.game == game, "MoveValidator לא מחובר למשחק"
        print("✅ כל המחלקות מחוברות נכון למשחק")
        
        print("🎉 כל הבדיקות עברו בהצלחה!")
        print("🎉 הקוד המחודש עובד כמו שצריך!")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בבדיקה: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_refactored_game()
    if success:
        print("\n✅ המחלקות החדשות מוכנות לשימוש!")
        print("📝 כדי להשתמש בגרסה החדשה, החלף את Game ב-GameRefactored")
    else:
        print("\n❌ יש בעיות שצריך לתקן לפני השימוש")
