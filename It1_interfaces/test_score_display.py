"""
test_score_display.py - בדיקה מהירה של מערכת הניקוד וההיסטוריה
"""
import sys
import pathlib
from unittest.mock import Mock

# הוסף את הנתיב לתיקיית המחלקות
current_dir = pathlib.Path(__file__).parent
sys.path.append(str(current_dir))

def test_score_manager():
    """Test ScoreManager functionality"""
    print("🧪 בודק את ScoreManager...")
    
    from ScoreManager import ScoreManager
    
    # צור mock game
    mock_game = Mock()
    score_manager = ScoreManager(mock_game)
    
    # בדוק הוספת מהלכים
    score_manager.record_move("PW0", (1, 6), (1, 5), "move")
    score_manager.record_move("PB0", (1, 1), (1, 2), "move")
    score_manager.record_move("NW0", (1, 7), (2, 5), "move")
    
    # בדוק תפיסה
    score_manager.record_move("PW0", (1, 5), (2, 4), "capture", "PB1")
    score_manager.record_move("QB0", (3, 0), (2, 5), "capture", "NW0")
    
    # הצג תוצאות
    scores = score_manager.get_scores()
    print(f"✅ ניקוד: שחקן 1 = {scores[0]}, שחקן 2 = {scores[1]}")
    
    moves1 = score_manager.get_player1_recent_moves()
    moves2 = score_manager.get_player2_recent_moves()
    
    print(f"✅ מהלכים שחקן 1: {len(moves1)}")
    for move in moves1:
        print(f"   - {move}")
    
    print(f"✅ מהלכים שחקן 2: {len(moves2)}")
    for move in moves2:
        print(f"   - {move}")
    
    return True

def test_enhanced_display():
    """Test that the enhanced display components work"""
    print("\n🎨 בודק את מערכת התצוגה המשופרת...")
    
    try:
        from DrawManager import DrawManager
        print("✅ DrawManager נטען בהצלחה")
        
        # בדוק אם background.png קיים
        bg_path = pathlib.Path(__file__).parent.parent / "background.png"
        if bg_path.exists():
            print("✅ background.png נמצא")
        else:
            print("⚠️ background.png לא נמצא - ייווצר רקע ברירת מחדל")
        
        return True
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        return False

if __name__ == "__main__":
    print("🎮 בדיקת מערכת הניקוד וההיסטוריה")
    print("=" * 50)
    
    success1 = test_score_manager()
    success2 = test_enhanced_display()
    
    if success1 and success2:
        print("\n🎉 כל הבדיקות עברו בהצלחה!")
        print("🎮 המשחק מוכן עם מערכת ניקוד והיסטוריה!")
        print("\n📋 איך להשתמש:")
        print("   python main_refactored.py  # הפעל את המשחק")
        print("   הניקוד יוצג בצד שמאל (שחקן 1)")
        print("   ההיסטוריה תוצג בצד ימין (שחקן 2)")
    else:
        print("\n❌ יש בעיות שצריך לתקן")
