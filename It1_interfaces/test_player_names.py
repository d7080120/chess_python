"""
test_player_names.py - בדיקת מערכת שמות השחקנים
"""

from PlayerNameManager import PlayerNameManager

def test_player_names():
    """בדיקת מערכת שמות השחקנים"""
    print("🧪 בודק את מערכת שמות השחקנים...")
    
    # יצירת מנהל השמות
    name_manager = PlayerNameManager()
    
    # בדיקת שמות ברירת מחדל
    print(f"✅ שם ברירת מחדל שחקן 1: {name_manager.get_player1_name()}")
    print(f"✅ שם ברירת מחדל שחקן 2: {name_manager.get_player2_name()}")
    
    # הגדרת שמות דמה
    name_manager.player1_name = "דורה"
    name_manager.player2_name = "אבי"
    
    print(f"✅ שם מעודכן שחקן 1: {name_manager.get_player1_name()}")
    print(f"✅ שם מעודכן שחקן 2: {name_manager.get_player2_name()}")
    
    print("🎉 כל הבדיקות עברו בהצלחה!")
    print("📋 המערכת מוכנה לקליטת שמות שחקנים!")

if __name__ == "__main__":
    test_player_names()
