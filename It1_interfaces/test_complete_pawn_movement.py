#!/usr/bin/env python3
"""
בדיקה מקיפה של תנועת חיילים - כולל תנועה קדימה פנויה
""        # חייל לבן לא במיקום התחלה (3,4)  
        (white_pawn2, 3, 3, True, "חייל לבן מהאמצע - תנועה קדימה צעד אחד"),
        (white_pawn2, 3, 2, False, "חייל לבן מהאמצע - תנועה קדימה 2 צעדים (אסור)"),
        (white_pawn2, 4, 3, True, "חייל לבן מהאמצע - אכילה באלכסון"),
        (white_pawn2, 2, 3, False, "חייל לבן מהאמצע - תנועה באלכסון ללא אכילה"),import time
import pathlib
from Board import Board
from GameRefactored import GameRefactored
from PieceFactory import PieceFactory
from Command import Command
from img import Img

def test_complete_pawn_movement():
    """בדיקה מקיפה של כללי תנועת חיילים"""
    print("♟️ בדיקה מקיפה של תנועת חיילים...")
    
    # יצירת לוח ומפעל כלים
    img = Img()
    img_path = pathlib.Path(__file__).parent.parent / "board.png"
    img.read(str(img_path), size=(800, 800))
    
    board = Board(
        cell_W_pix=100,
        cell_H_pix=100,
        cell_H_m=1,
        cell_W_m=1,
        W_cells=8,
        H_cells=8,
        img=img
    )
    pieces_root = pathlib.Path(__file__).parent.parent / "pieces"
    factory = PieceFactory(board, pieces_root)
    
    # צור חיילים לבדיקה
    pieces = []
    
    # חייל לבן במיקום התחלה (4,6)
    white_pawn1 = factory.create_piece("PW", (4, 6), None)
    white_pawn1.piece_id = "PW_start"
    if hasattr(white_pawn1, '_state') and hasattr(white_pawn1._state, '_physics'):
        white_pawn1._state._physics.piece_id = "PW_start"
    pieces.append(white_pawn1)
    
    # חייל לבן במיקום לא התחלה (3,4) - לא חוסם את התנועה של הראשון
    white_pawn2 = factory.create_piece("PW", (3, 4), None)
    white_pawn2.piece_id = "PW_middle"
    if hasattr(white_pawn2, '_state') and hasattr(white_pawn2._state, '_physics'):
        white_pawn2._state._physics.piece_id = "PW_middle"
    pieces.append(white_pawn2)
    
    # חייל שחור לא במיקום התחלה (2,3)
    black_pawn1 = factory.create_piece("PB", (2, 3), None)
    black_pawn1.piece_id = "PB_middle"
    if hasattr(black_pawn1, '_state') and hasattr(black_pawn1._state, '_physics'):
        black_pawn1._state._physics.piece_id = "PB_middle"
    pieces.append(black_pawn1)
    
    # חייל שחור לאכילה (4,3) - ליד החייל הלבן השני
    black_pawn2 = factory.create_piece("PB", (4, 3), None)
    black_pawn2.piece_id = "PB_capture"
    if hasattr(black_pawn2, '_state') and hasattr(black_pawn2._state, '_physics'):
        black_pawn2._state._physics.piece_id = "PB_capture"
    pieces.append(black_pawn2)
    
    # צור משחק
    game = GameRefactored(pieces, board)
    
    # עדכן את הכלים עם התורים של המשחק
    for piece in pieces:
        if hasattr(piece, '_state') and hasattr(piece._state, '_physics'):
            piece._state._physics.user_input_queue = game.user_input_queue
            piece._state._game_queue = game.game_queue
    
    print(f"🔵 חייל לבן התחלה: {white_pawn1._state._physics.cell}")
    print(f"🔵 חייל לבן אמצע: {white_pawn2._state._physics.cell}")
    print(f"🔴 חייל שחור אמצע: {black_pawn1._state._physics.cell}")
    print(f"🔴 חייל שחור לאכילה: {black_pawn2._state._physics.cell}")
    
    # בדיקות מקיפות
    tests = [
        # חייל לבן במיקום התחלה (4,6)
        (white_pawn1, 4, 5, True, "חייל לבן מהתחלה - תנועה קדימה צעד אחד"),
        (white_pawn1, 4, 4, True, "חייל לבן מהתחלה - תנועה קדימה 2 צעדים"),
        
        # חייל לבן לא במיקום התחלה (4,4)  
        (white_pawn2, 4, 3, True, "חייל לבן מהאמצע - תנועה קدימה צעד אחד"),
        (white_pawn2, 4, 2, False, "חייל לבן מהאמצע - תנועה קדימה 2 צעדים (אסור)"),
        (white_pawn2, 5, 3, True, "חייל לבן מהאמצע - אכילה באלכסון"),
        (white_pawn2, 3, 3, False, "חייל לבן מהאמצע - תנועה באלכסון ללא אכילה"),
        
        # חייל שחור לא במיקום התחלה (2,3)
        (black_pawn1, 2, 4, True, "חייל שחור מהאמצע - תנועה קדימה צעד אחד"),
        (black_pawn1, 2, 5, False, "חייל שחור מהאמצע - תנועה קדימה 2 צעדים (אסור)"),
        (black_pawn1, 1, 4, False, "חייל שחור מהאמצע - תנועה באלכסון ללא אכילה"),
        
        # תנועות שגויות כלליות
        (white_pawn1, 5, 6, False, "חייל לבן - תנועה צידית"),
        (white_pawn1, 4, 7, False, "חייל לבן - תנועה אחורה"),
        (black_pawn1, 1, 3, False, "חייל שחור - תנועה צידית"), 
        (black_pawn1, 2, 2, False, "חייל שחור - תנועה אחורה"),
    ]
    
    results = []
    
    print("\n🧪 מתחיל בדיקות...")
    for i, (piece, target_x, target_y, should_succeed, test_name) in enumerate(tests, 1):
        print(f"\n{i}. {test_name}")
        print(f"   ניסיון: {piece.piece_id} מ-{piece._state._physics.cell} ל-({target_x}, {target_y})")
        
        # נסה לזוז (player 1 for white, player 2 for black)
        player_num = 1 if 'W' in piece.piece_id else 2
        move_result = game.move_validator._is_valid_move(piece, target_x, target_y, player_num)
        
        if move_result == should_succeed:
            print(f"   ✅ נכון: {'הצליח' if move_result else 'נכשל'}")
            results.append(True)
        else:
            print(f"   ❌ שגוי: צפוי {'הצלחה' if should_succeed else 'כישלון'}, קיבלנו {'הצלחה' if move_result else 'כישלון'}")
            results.append(False)
    
    # סיכום
    success_count = sum(results)
    total_count = len(results)
    
    print(f"\n📊 תוצאות סופיות: {success_count}/{total_count} בדיקות עברו")
    
    if success_count == total_count:
        print("🎉 כל הבדיקות עברו בהצלחה! כללי החיילים תקינים לחלוטין.")
        return True
    else:
        print("❌ יש בדיקות שנכשלו. יש צורך בבדיקה נוספת.")
        return False

if __name__ == "__main__":
    success = test_complete_pawn_movement()
    print("🏁 סיום בדיקה מקיפה")
