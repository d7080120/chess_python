"""
WinChecker - מחלקה לבדיקת תנאי נצחון
"""


class WinChecker:
    def __init__(self, game_ref):
        """Initialize the win checker with reference to game."""
        self.game = game_ref

    def is_win(self) -> bool:
        """Check if the game has ended."""
        # בדיקה אם אחד המלכים נהרג
        white_king_alive = False
        black_king_alive = False
        
        print("🔍 Checking victory conditions...")
        for piece in self.game.pieces:
            print(f"   Piece exists: {piece.piece_id}")
            if piece.piece_id == "KW0":  # מלך לבן
                white_king_alive = True
                print("   👑 White king is still alive!")
            elif piece.piece_id == "KB0":  # מלך שחור
                black_king_alive = True
                print("   👑 Black king is still alive!")
        
        print(f"White king alive: {white_king_alive}, Black king alive: {black_king_alive}")
        
        # אם אחד המלכים נהרג - המשחק נגמר
        if not white_king_alive or not black_king_alive:
            print("🏆 Victory condition met!")
            return True
            
        print("✅ Game continues...")
        return False

    def announce_win(self):
        """Announce the winner."""
        print("🎺 Announcing victory!")
        # בדיקה מי ניצח
        white_king_alive = False
        black_king_alive = False
        
        for piece in self.game.pieces:
            if piece.piece_id == "KW0":  # מלך לבן
                white_king_alive = True
            elif piece.piece_id == "KB0":  # מלך שחור
                black_king_alive = True
        
        if not white_king_alive:
            print("🏆 Player 2 (BLACK) wins! White King was captured!")
            print("🏆 PLAYER 2 (BLACK) WINS! White King was captured!")
            print("🏆 THE WINNER IS PLAYER 2 (BLACK)!")
        elif not black_king_alive:
            print("🏆 Player 1 (WHITE) wins! Black King was captured!")
            print("🏆 PLAYER 1 (WHITE) WINS! Black King was captured!")
            print("🏆 THE WINNER IS PLAYER 1 (WHITE)!")
        else:
            print("🎮 Game over!")
            print("🎮 Game Over!")
