"""
ScoreManager - מחלקה לניהול ניקוד והיסטוריית מהלכים
"""
from typing import List, Tuple
import time


class MoveRecord:
    """Record of a single move"""
    def __init__(self, piece_id: str, from_pos: Tuple[int, int], to_pos: Tuple[int, int], 
                 move_type: str = "move", captured_piece: str = None, timestamp: float = None):
        self.piece_id = piece_id
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.move_type = move_type  # "move", "capture", "promotion", etc.
        self.captured_piece = captured_piece
        self.timestamp = timestamp or time.time()
        
    def __str__(self):
        """String representation for display"""
        from_str = f"{chr(65 + self.from_pos[0])}{8 - self.from_pos[1]}"
        to_str = f"{chr(65 + self.to_pos[0])}{8 - self.to_pos[1]}"
        
        if self.move_type == "capture" and self.captured_piece:
            return f"{self.piece_id}: {from_str}x{to_str}"
        else:
            return f"{self.piece_id}: {from_str}-{to_str}"


class ScoreManager:
    """Manages scoring and move history for both players"""
    
    def __init__(self, game_ref):
        """Initialize the score manager with reference to game."""
        self.game = game_ref
        
        # Move history - last 10 moves for each player
        self.player1_moves: List[MoveRecord] = []  # White pieces
        self.player2_moves: List[MoveRecord] = []  # Black pieces
        
        # Scoring system
        self.player1_score = 0  # White player score
        self.player2_score = 0  # Black player score
        
        # Piece values for scoring
        self.piece_values = {
            'P': 1,   # Pawn
            'N': 3,   # Knight
            'B': 3,   # Bishop
            'R': 5,   # Rook
            'Q': 9,   # Queen
            'K': 0    # King (invaluable)
        }
    
    def record_move(self, piece_id: str, from_pos: Tuple[int, int], to_pos: Tuple[int, int], 
                   move_type: str = "move", captured_piece: str = None):
        """Record a move for the appropriate player"""
        move = MoveRecord(piece_id, from_pos, to_pos, move_type, captured_piece)
        
        # Determine which player made the move
        is_white_piece = 'W' in piece_id
        if is_white_piece:
            self.player1_moves.append(move)
            # Keep only last 10 moves
            if len(self.player1_moves) > 10:
                self.player1_moves.pop(0)
        else:
            self.player2_moves.append(move)
            # Keep only last 10 moves
            if len(self.player2_moves) > 10:
                self.player2_moves.pop(0)
        
        # Update score if it's a capture
        if move_type == "capture" and captured_piece:
            self._update_score_for_capture(is_white_piece, captured_piece)
    
    def _update_score_for_capture(self, capturing_player_is_white: bool, captured_piece_id: str):
        """Update score when a piece is captured"""
        # Extract piece type (first character after color)
        piece_type = captured_piece_id[1] if len(captured_piece_id) > 1 else captured_piece_id[0]
        piece_value = self.piece_values.get(piece_type, 0)
        
        if capturing_player_is_white:
            self.player1_score += piece_value
            print(f"🏆 Player 1 (White) scored {piece_value} points! Total: {self.player1_score}")
        else:
            self.player2_score += piece_value
            print(f"🏆 Player 2 (Black) scored {piece_value} points! Total: {self.player2_score}")
    
    def get_player1_recent_moves(self, count: int = 10) -> List[str]:
        """Get recent moves for player 1 (white) as display strings - newest first"""
        recent_moves = [str(move) for move in self.player1_moves[-count:]]
        return list(reversed(recent_moves))  # הפוך את הסדר - החדש ביותר בראש
    
    def get_player2_recent_moves(self, count: int = 10) -> List[str]:
        """Get recent moves for player 2 (black) as display strings - newest first"""
        recent_moves = [str(move) for move in self.player2_moves[-count:]]
        return list(reversed(recent_moves))  # הפוך את הסדר - החדש ביותר בראש
    
    def get_scores(self) -> Tuple[int, int]:
        """Get current scores for both players"""
        return self.player1_score, self.player2_score
    
    def get_move_count(self) -> Tuple[int, int]:
        """Get total move count for both players"""
        return len(self.player1_moves), len(self.player2_moves)
    
    def reset_scores(self):
        """Reset all scores and move history"""
        self.player1_score = 0
        self.player2_score = 0
        self.player1_moves.clear()
        self.player2_moves.clear()
        print("🔄 Scores and move history reset!")
    
    def print_summary(self):
        """Print current game summary"""
        print("\n" + "="*50)
        print("📊 GAME SUMMARY")
        print("="*50)
        print(f"🏆 Player 1 (White): {self.player1_score} points | {len(self.player1_moves)} moves")
        print(f"🏆 Player 2 (Black): {self.player2_score} points | {len(self.player2_moves)} moves")
        
        print(f"\n📝 Recent moves Player 1:")
        for i, move in enumerate(self.get_player1_recent_moves(5), 1):
            print(f"   {i}. {move}")
            
        print(f"\n📝 Recent moves Player 2:")
        for i, move in enumerate(self.get_player2_recent_moves(5), 1):
            print(f"   {i}. {move}")
        print("="*50)
