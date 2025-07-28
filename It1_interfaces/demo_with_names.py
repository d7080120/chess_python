"""
demo_with_names.py - דמו קטן של המשחק עם שמות שחקנים
"""

from PlayerNameManager import PlayerNameManager
from ScoreManager import ScoreManager

def demo_enhanced_game():
    """הדגמה של התכונות החדשות"""
    
    print("🎮 הדגמת המשחק המשופר עם שמות שחקנים")
    print("=" * 55)
    
    # יצירת מנהלי המשחק
    name_manager = PlayerNameManager()
    score_manager = ScoreManager(None)  # None במקום game_ref
    
    # הגדרת שמות דמה
    name_manager.player1_name = "דורה"
    name_manager.player2_name = "אבי"
    
    print(f"👤 שחקן 1: {name_manager.get_player1_name()} (כלים לבנים)")
    print(f"👤 שחקן 2: {name_manager.get_player2_name()} (כלים שחורים)")
    print()
    
    # הדמיית כמה מהלכים
    print("🎯 הדמיית מהלכים:")
    score_manager.record_move("PW0", (0, 6), (0, 5))  # רגלי לבן
    score_manager.record_move("PB0", (0, 1), (0, 2))  # רגלי שחור
    score_manager.record_move("NW0", (1, 7), (2, 5))  # סוס לבן
    score_manager.record_move("NB0", (1, 0), (2, 2))  # סוס שחור
    score_manager.record_move("PW1", (1, 6), (1, 4), "capture", "PB1")  # תפיסה
    
    # הצגת ניקוד
    score1, score2 = score_manager.get_scores()
    print(f"🏆 {name_manager.get_player1_name()}: {score1} נקודות")
    print(f"🏆 {name_manager.get_player2_name()}: {score2} נקודות")
    print()
    
    # הצגת מהלכים אחרונים
    print(f"📋 המהלכים האחרונים של {name_manager.get_player1_name()}:")
    moves1 = score_manager.get_player1_recent_moves(5)
    for i, move in enumerate(moves1):
        print(f"   {len(moves1)-i}. {move}")
    
    print(f"\n📋 המהלכים האחרונים של {name_manager.get_player2_name()}:")
    moves2 = score_manager.get_player2_recent_moves(5)
    for i, move in enumerate(moves2):
        print(f"   {len(moves2)-i}. {move}")
    
    print("\n" + "=" * 55)
    print("🎉 התכונות החדשות עובדות מצוין!")
    print("✨ המשחק עכשיו אישי ומותאם לשחקנים!")
    print("🚀 נסו את המשחק המלא: python main_refactored.py")

if __name__ == "__main__":
    demo_enhanced_game()
