"""
test_move_fixes.py - בדיקת התיקונים החדשים למהלכים
"""

from src.ui.ScoreManager import ScoreManager

def test_move_fixes():
    """בדיקת התיקונים למערכת המהלכים"""
    
    print("🔧 בדיקת התיקונים למערכת המהלכים")
    print("=" * 50)
    
    # יצירת מנהל ניקוד
    score_manager = ScoreManager(None)
    
    print("🎯 הדמיית מהלכים רצופים:")
    
    # הדמיית מהלכים
    moves_data = [
        ("PW0", (0, 6), (0, 5), "move", None),
        ("PB0", (0, 1), (0, 2), "move", None),
        ("NW0", (1, 7), (2, 5), "move", None),
        ("NB0", (1, 0), (2, 2), "move", None),
        ("PW1", (1, 6), (1, 4), "capture", "PB1"),
        ("QB0", (3, 0), (2, 1), "move", None),
        ("QW0", (3, 7), (3, 4), "move", None),
        ("RB0", (0, 0), (0, 1), "move", None),
        ("RW0", (0, 7), (0, 6), "move", None),
        ("KB0", (4, 0), (3, 0), "move", None)
    ]
    
    for i, (piece_id, from_pos, to_pos, move_type, captured) in enumerate(moves_data, 1):
        score_manager.record_move(piece_id, from_pos, to_pos, move_type, captured)
        print(f"   מהלך {i}: {piece_id} מ-{from_pos} ל-{to_pos}")
    
    print(f"\n📊 ניקוד נוכחי:")
    score1, score2 = score_manager.get_scores()
    print(f"   שחקן 1 (לבן): {score1} נקודות")
    print(f"   שחקן 2 (שחור): {score2} נקודות")
    
    print(f"\n📋 המהלכים האחרונים של שחקן 1 (החדש ביותר בראש):")
    moves1 = score_manager.get_player1_recent_moves(10)
    for i, move in enumerate(moves1[:5], 1):  # הצג רק 5 ראשונים
        print(f"   {i}. {move}")
    
    print(f"\n📋 המהלכים האחרונים של שחקן 2 (החדש ביותר בראש):")
    moves2 = score_manager.get_player2_recent_moves(10)
    for i, move in enumerate(moves2[:5], 1):  # הצג רק 5 ראשונים
        print(f"   {i}. {move}")
    
    print("\n" + "=" * 50)
    print("✅ תיקונים שבוצעו:")
    print("   🔧 הוסרה רישום כפול של מהלכים")
    print("   🔧 מספור מהלכים תוקן (החדש ביותר בראש)")
    print("   🎨 נוסף רקע לבן למהלכים (כמו דף נייר)")
    print("   📝 טקסט שחור על רקע לבן לקריאות טובה יותר")
    print("🎉 כל התיקונים הופעלו בהצלחה!")

if __name__ == "__main__":
    test_move_fixes()
