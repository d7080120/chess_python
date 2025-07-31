"""
CaptureHandler - מחלקה לטיפול בתפיסות וביטול כלים
"""
import pathlib
from src.core.game_logic.Command import Command


class CaptureHandler:
    def __init__(self, game_ref):
        """Initialize the capture handler with reference to game."""
        self.game = game_ref

    def handle_arrival(self, cmd: Command):
        """Handle piece arrival and check for captures."""
        
        # Find the piece that arrived at the destination
        arriving_piece = None
        for piece in self.game.pieces:
            if piece.piece_id == cmd.piece_id:
                arriving_piece = piece
                break
        
        if not arriving_piece:
            return
        
        # Get the position of the arriving piece
        target_pos = arriving_piece._state._physics.cell
        
        # Assume the piece came from a previous position - we'll use current position as source for now
        from_pos = target_pos  # This is not accurate but will work for now
        
        # Check pawn promotion before checking capture
        self._check_pawn_promotion(arriving_piece, target_pos)
        
        # Search for enemy piece at the same position
        pieces_to_remove = []
        for piece in self.game.pieces:
            if piece != arriving_piece:  # Not the same piece
                piece_pos = piece._state._physics.cell
                if piece_pos == target_pos:
                    # Check if it's an enemy piece
                    arriving_is_white = 'W' in arriving_piece.piece_id
                    piece_is_white = 'W' in piece.piece_id
                    
                    if arriving_is_white != piece_is_white:  # Different colors = enemies
                        pieces_to_remove.append(piece)
                        
                        # Special check for kings
                        if piece.piece_id in ["KW0", "KB0"]:
                            print(f"KING CAPTURED! {piece.piece_id} was taken!")
        
        # Remove captured pieces
        for piece in pieces_to_remove:
            if piece in self.game.pieces:
                self.game.pieces.remove(piece)
                
                # Additional victory check for kings
                if piece.piece_id in ["KW0", "KB0"]:
                    # Immediate check for victory conditions
                    white_kings = [p for p in self.game.pieces if p.piece_id == "KW0"]
                    black_kings = [p for p in self.game.pieces if p.piece_id == "KB0"]
                    
                    if len(white_kings) == 0:
                        print("Player 2 Wins!")
                    if len(black_kings) == 0:
                        print("Player 1 Wins!")
        
        # Check victory conditions after capture
        if pieces_to_remove:
            if self.game.win_checker.is_win():
                self.game.win_checker.announce_win()
                self.game.game_over = True  # Mark game as over immediately after victory
        
        # DEBUG: Print attacking piece position after capture
        final_pos = arriving_piece._state._physics.cell

    def _check_pawn_promotion(self, piece, target_pos):
        """Check if a pawn should be promoted to queen."""
        # Check if it's a pawn
        if not piece.piece_id.startswith('P'):
            return  # Not a pawn - no promotion
            
        col, row = target_pos  # target_pos is (x, y) = (col, row)
        is_white_pawn = 'W' in piece.piece_id
        is_black_pawn = 'B' in piece.piece_id
        
        # Check if the pawn reached the appropriate promotion row
        should_promote = False
        new_piece_type = None
        
        if is_white_pawn and row == 0:  # White pawn reached row 0
            should_promote = True
            new_piece_type = "QW"
            print(f"White pawn promoted to Queen!")
        elif is_black_pawn and row == 7:  # Black pawn reached row 7
            should_promote = True
            new_piece_type = "QB"
            print(f"Black pawn promoted to Queen!")
            
        if should_promote:
            self._promote_pawn_to_queen(piece, new_piece_type, target_pos)

    def _promote_pawn_to_queen(self, pawn, queen_type, position):
        """Replace a pawn with a queen at the given position."""
        pieces_root = pathlib.Path(__file__).parent.parent / "pieces"
        
        # Create new queen
        from src.core.game_setup.PieceFactory import PieceFactory
        factory = PieceFactory(self.game.board, pieces_root)
        
        # Create unique ID for the new queen
        existing_queens = [p for p in self.game.pieces if p.piece_id.startswith(queen_type)]
        queen_id = f"{queen_type}{len(existing_queens)}"
        
        # Create new queen at required position
        new_queen = factory.create_piece(queen_type, position, self.game.user_input_queue)
        new_queen.piece_id = queen_id
        new_queen._state._physics.piece_id = queen_id
        
        # Connect the new queen to the game's queue system properly
        new_queen._state._game_queue = self.game.game_queue
        
        # Set the new queen to rest_long state (as if it just moved) using proper command
        from src.core.game_logic.Command import Command
        import time
        now_ms = self.game.game_time_ms()  # Use the game's time method instead of time.time()
        
        # Process the arrived command to properly enter rest_long state
        # This will trigger the normal state machine transition: move -> arrived -> rest_long
        new_queen._state.state = "move"  # Set to move first
        new_queen._state._transition("arrived", now_ms)  # Then transition to rest_long
        
        # Remove old pawn and add new queen
        if pawn in self.game.pieces:
            self.game.pieces.remove(pawn)
            
        self.game.pieces.append(new_queen)
