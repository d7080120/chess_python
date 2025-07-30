"""
🎮 מדריך מיקום חלונות למשחק השחמט
=======================================

כדי לשנות את מיקום החלונות במשחק:

📝 עריכת קובץ ההגדרות:
1. פתח את הקובץ: window_settings.py
2. שנה את הערכים הבאים:

📍 אפשרויות מיקום:
   "top-left" = פינה שמאלית עליונה (0, 0)
   "center"   = מרכז המסך

🔧 דוגמאות:

לפתיחה בפינה השמאלית העליונה:
    PLAYER_DIALOG_POSITION = "top-left"
    GAME_WINDOW_POSITION = "top-left"

לפתיחה במרכז המסך:
    PLAYER_DIALOG_POSITION = "center"
    GAME_WINDOW_POSITION = "center"

לשילוב (דיאלוג בפינה, משחק במרכז):
    PLAYER_DIALOG_POSITION = "top-left"
    GAME_WINDOW_POSITION = "center"

💡 עצות:
- "top-left" טוב למסכים קטנים או כשאתה רוצה לראות חלונות אחרים
- "center" טוב למסכים גדולים ולמיקוד במשחק
- השינויים יכנסו לתוקף בהפעלה הבאה של המשחק

🚀 הפעלת המשחק:
python main.py
"""

if __name__ == "__main__":
    print("📖 להצגת המדריך המלא, קרא את הקובץ window_positioning_guide.py")
    
    # הצגת ההגדרות הנוכחיות
    try:
        from window_settings import PLAYER_DIALOG_POSITION, GAME_WINDOW_POSITION
        print("\n⚙️ הגדרות נוכחיות:")
        print(f"   🎯 חלון השמות: {PLAYER_DIALOG_POSITION}")
        print(f"   🎮 חלון המשחק: {GAME_WINDOW_POSITION}")
    except ImportError:
        print("❌ שגיאה בטעינת ההגדרות")
    
    print("\n🔧 לשינוי ההגדרות, ערוך את הקובץ: window_settings.py")
