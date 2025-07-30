#!/usr/bin/env python3
"""
בדיקת תנועת חיילים - האם הם יכולים לזוז רק קדימה ולאכול רק באלכסון
"""

import time
import pathlib
from Board import Board
from GameRefactored import GameRefactored
from PieceFactory import PieceFactory
from Command import Command
from img import Img

def test_pawn_movement():
    """בדיקת כללי תנועת חיילים"""
    print("♟️ בדיקת תנועת חיילים...")
    
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
    
    # חייל לבן במיקום (4,6) - מיקום התחלה רגיל
    white_pawn = factory.create_piece("PW", (4, 6), None)
    white_pawn.piece_id = "PW_test"
    if hasattr(white_pawn, '_state') and hasattr(white_pawn._state, '_physics'):
        white_pawn._state._physics.piece_id = "PW_test"
    pieces.append(white_pawn)
    
    # חייל שחור במיקום (5,5) - כדי לבדוק אכילה באלכסון  
    black_pawn = factory.create_piece("PB", (5, 5), None)
    black_pawn.piece_id = "PB_test"
    if hasattr(black_pawn, '_state') and hasattr(black_pawn._state, '_physics'):
        black_pawn._state._physics.piece_id = "PB_test"
    pieces.append(black_pawn)
    
    # חייל שחור נוסף במיקום (4,5) - כדי לחסום תנועה קדימה
    black_pawn2 = factory.create_piece("PB", (4, 5), None)
    black_pawn2.piece_id = "PB_blocker"
    if hasattr(black_pawn2, '_state') and hasattr(black_pawn2._state, '_physics'):
        black_pawn2._state._physics.piece_id = "PB_blocker"
    pieces.append(black_pawn2)
    
    # צור משחק
    game = GameRefactored(pieces, board)
    
    # עדכן את הכלים עם התורים של המשחק
    for piece in pieces:
        if hasattr(piece, '_state') and hasattr(piece._state, '_physics'):
            piece._state._physics.user_input_queue = game.user_input_queue
            piece._state._game_queue = game.game_queue
    
    print(f"🔵 חייל לבן נוצר במיקום: {white_pawn._state._physics.cell}")
    print(f"🔴 חייל שחור נוצר במיקום: {black_pawn._state._physics.cell}")
    print(f"🔴 חייל חוסם נוצר במיקום: {black_pawn2._state._physics.cell}")
    
    # בדיקות שונות
    tests = [
        # (piece, target_x, target_y, should_succeed, test_name)
        (white_pawn, 4, 5, False, "חייל לבן - תנועה קדימה חסומה"),
        (white_pawn, 5, 5, True, "חייל לבן - אכילה באלכסון (יש כלי ב-5,5)"),  # תיקון המיקום
        (white_pawn, 3, 5, False, "חייל לבן - תנועה באלכסון ללא אכילה"),
        (white_pawn, 5, 6, False, "חייל לבן - תנועה צידית"),
        (white_pawn, 4, 7, False, "חייל לבן - תנועה אחורה"),
    ]
    
    results = []
    
    for piece, target_x, target_y, should_succeed, test_name in tests:
        print(f"\n🧪 בדיקה: {test_name}")
        print(f"   ניסיון להזיז {piece.piece_id} מ-{piece._state._physics.cell} ל-({target_x}, {target_y})")
        
        # נסה לזוז
        move_result = game.move_validator._is_valid_move(piece, target_x, target_y, 1)
        
        if move_result == should_succeed:
            print(f"   ✅ תוצאה נכונה: {'הצליח' if move_result else 'נכשל'}")
            results.append(True)
        else:
            print(f"   ❌ תוצאה שגויה: צפוי {'הצלחה' if should_succeed else 'כישלון'}, קיבלנו {'הצלחה' if move_result else 'כישלון'}")
            results.append(False)
    
    # סיכום
    success_count = sum(results)
    total_count = len(results)
    
    print(f"\n📊 תוצאות: {success_count}/{total_count} בדיקות עברו")
    
    if success_count == total_count:
        print("🎉 כל הבדיקות עברו בהצלחה! כללי החיילים עובדים נכון.")
        return True
    else:
        print("❌ חלק מהבדיקות נכשלו. יש צורך בתיקון נוסף.")
        return False

if __name__ == "__main__":
    success = test_pawn_movement()
    print("🏁 סיום בדיקת תנועת חיילים")
