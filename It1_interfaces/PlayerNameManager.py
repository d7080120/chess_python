"""
PlayerNameManager - מחלקה לניהול שמות השחקנים
"""

class PlayerNameManager:
    def __init__(self):
        """Initialize the player name manager."""
        self.player1_name = ""
        self.player2_name = ""
        
    def get_player_names(self):
        """Get player names from user input."""
        print("🎮 הגדרת שמות השחקנים")
        print("=" * 40)
        
        # קבלת שם שחקן 1
        while True:
            name1 = input("👤 הכנס שם שחקן 1 (כלים לבנים): ").strip()
            if name1:
                self.player1_name = name1
                break
            print("❌ אנא הכנס שם תקין!")
        
        # קבלת שם שחקן 2  
        while True:
            name2 = input("👤 הכנס שם שחקן 2 (כלים שחורים): ").strip()
            if name2:
                self.player2_name = name2
                break
            print("❌ אנא הכנס שם תקין!")
        
        print(f"✅ שחקן 1: {self.player1_name} (לבן)")
        print(f"✅ שחקן 2: {self.player2_name} (שחור)")
        print("🎯 בהצלחה במשחק!")
        print()
        
        return self.player1_name, self.player2_name
    
    def get_player1_name(self):
        """Get player 1 name."""
        return self.player1_name if self.player1_name else "Player 1"
    
    def get_player2_name(self):
        """Get player 2 name."""
        return self.player2_name if self.player2_name else "Player 2"
