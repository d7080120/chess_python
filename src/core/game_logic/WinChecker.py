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
        
        for piece in self.game.pieces:
            if piece.piece_id == "KW0":  # מלך לבן
                white_king_alive = True
            elif piece.piece_id == "KB0":  # מלך שחור
                black_king_alive = True
        
        # אם אחד המלכים נהרג - המשחק נגמר
        if not white_king_alive or not black_king_alive:
            return True
            
        return False

    def announce_win(self):
        """Announce the winner."""
        # בדיקה מי ניצח
        white_king_alive = False
        black_king_alive = False
        
        for piece in self.game.pieces:
            if piece.piece_id == "KW0":  # מלך לבן
                white_king_alive = True
            elif piece.piece_id == "KB0":  # מלך שחור
                black_king_alive = True
        
        if not white_king_alive:
            print("🏆 PLAYER 2 (BLACK) WINS! White King was captured!")
        elif not black_king_alive:
            print("🏆 PLAYER 1 (WHITE) WINS! Black King was captured!")
        else:
            print("🎮 Game Over!")
