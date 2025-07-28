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
        
        print("🔍 בודק תנאי נצחון...")
        for piece in self.game.pieces:
            print(f"   כלי קיים: {piece.piece_id}")
            if piece.piece_id == "KW0":  # מלך לבן
                white_king_alive = True
                print("   👑 מלך לבן עדיין חי!")
            elif piece.piece_id == "KB0":  # מלך שחור
                black_king_alive = True
                print("   👑 מלך שחור עדיין חי!")
        
        print(f"מלך לבן חי: {white_king_alive}, מלך שחור חי: {black_king_alive}")
        
        # אם אחד המלכים נהרג - המשחק נגמר
        if not white_king_alive or not black_king_alive:
            print("🏆 תנאי נצחון התקיים!")
            return True
            
        print("✅ המשחק ממשיך...")
        return False

    def announce_win(self):
        """Announce the winner."""
        print("🎺 מכריז על הנצחון!")
        # בדיקה מי ניצח
        white_king_alive = False
        black_king_alive = False
        
        for piece in self.game.pieces:
            if piece.piece_id == "KW0":  # מלך לבן
                white_king_alive = True
            elif piece.piece_id == "KB0":  # מלך שחור
                black_king_alive = True
        
        if not white_king_alive:
            print("🏆 שחקן 2 (שחור) ניצח! המלך הלבן נהרג!")
            print("🏆 PLAYER 2 (BLACK) WINS! White King was captured!")
            print("🏆 THE WINNER IS PLAYER 2 (BLACK)!")
        elif not black_king_alive:
            print("🏆 שחקן 1 (לבן) ניצח! המלך השחור נהרג!")
            print("🏆 PLAYER 1 (WHITE) WINS! Black King was captured!")
            print("🏆 THE WINNER IS PLAYER 1 (WHITE)!")
        else:
            print("🎮 המשחק נגמר!")
            print("🎮 Game Over!")
