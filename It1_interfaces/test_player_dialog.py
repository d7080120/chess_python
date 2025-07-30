"""
טסט פשוט לדיאלוג שמות השחקנים
"""
from PlayerNameDialog import PlayerNameDialog

if __name__ == "__main__":
    print("🧪 Testing PlayerNameDialog...")
    
    try:
        dialog = PlayerNameDialog()
        player1, player2 = dialog.get_player_names()
        
        print(f"✅ Test completed successfully!")
        print(f"   Player 1: {player1}")
        print(f"   Player 2: {player2}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("🎮 Test finished!")
