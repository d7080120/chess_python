"""
PlayerNameManager - מחלקה לניהול שמות השחקנים עם GUI
"""
from src.ui.PlayerNameDialog import PlayerNameDialog


class PlayerNameManager:
    def __init__(self):
        """Initialize the player name manager."""
        self.player1_name = ""
        self.player2_name = ""
        
    def get_player_names(self, window_position="top-left"):
        """Get player names using GUI dialog.
        
        Args:
            window_position: "center" for screen center, "top-left" for top-left corner
        """
        print("🎮 Opening player name dialog...")
        
        # יצירת דיאלוג GUI לקבלת השמות
        dialog = PlayerNameDialog(window_position=window_position)
        
        try:
            # קבלת השמות דרך הדיאלוג
            self.player1_name, self.player2_name = dialog.get_player_names()
            
            print("✅ Player names set successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error getting player names: {e}")
            print("🔄 Using default names...")
            self.player1_name = "Player 1"
            self.player2_name = "Player 2"
            return False
    
    def get_player1_name(self):
        """Get player 1 name."""
        return self.player1_name if self.player1_name else "Player 1"
    
    def get_player2_name(self):
        """Get player 2 name."""
        return self.player2_name if self.player2_name else "Player 2"
