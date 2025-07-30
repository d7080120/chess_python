"""
CaptureHandler - מחלקה לטיפול בתפיסות וביטול כלים
"""
import pathlib
from Command import Command


class CaptureHandler:
    def __init__(self, game_ref):
        """Initialize the capture handler with reference to game."""
        self.game = game_ref

    def handle_arrival(self, cmd: Command):
        """Handle piece arrival and check for captures."""
        print(f"🏁 Piece arrived at destination: {cmd.piece_id}")
        
        # Find the piece that arrived at the destination
        arriving_piece = None
        for piece in self.game.pieces:
            if piece.piece_id == cmd.piece_id:
                arriving_piece = piece
                break
        
        if not arriving_piece:
            print(f"❌ Arriving piece not found: {cmd.piece_id}")
            return
        
        # Get the position of the arriving piece
        target_pos = arriving_piece._state._physics.cell
        
        # Assume the piece came from a previous position - we'll use current position as source for now
        from_pos = target_pos  # This is not accurate but will work for now
        
        # Check pawn promotion before checking capture
        self._check_pawn_promotion(arriving_piece, target_pos)
        
        print(f"🎯 Checking capture at position {target_pos}")
        print(f"🔍 List of all pieces and their positions:")
        
        # Display all pieces and their positions
        for piece in self.game.pieces:
            piece_pos = piece._state._physics.cell
            print(f"   {piece.piece_id} at position {piece_pos}")
        
        # Search for enemy piece at the same position
        pieces_to_remove = []
        for piece in self.game.pieces:
            if piece != arriving_piece:  # Not the same piece
                piece_pos = piece._state._physics.cell
                print(f"🔍 Checking {piece.piece_id} at position {piece_pos} vs {target_pos}")
                if piece_pos == target_pos:
                    # Check if it's an enemy piece
                    arriving_is_white = 'W' in arriving_piece.piece_id
                    piece_is_white = 'W' in piece.piece_id
                    
                    print(f"🎯 Found piece at same position! {piece.piece_id} (white: {piece_is_white}) vs {arriving_piece.piece_id} (white: {arriving_is_white})")
                    
                    if arriving_is_white != piece_is_white:  # Different colors = enemies
                        print(f"⚔️ {arriving_piece.piece_id} captured {piece.piece_id} at position {target_pos}!")
                        pieces_to_remove.append(piece)
                        
                        # Move logging will be handled via Observer pattern
                        
                        # Special check for kings
                        if piece.piece_id in ["KW0", "KB0"]:
                            print(f"🚨🚨 CRITICAL: KING CAPTURED! {piece.piece_id} was taken! 🚨🚨🚨")
                            print(f"💀 King killed: {piece.piece_id}")
                            print(f"🔥 This will cause game over!")
                    else:
                        print(f"🛡️ Same color - no attack: {piece.piece_id} and {arriving_piece.piece_id}")
        
        print(f"📋 Pieces to capture: {[p.piece_id for p in pieces_to_remove]}")
        
        # Remove captured pieces
        for piece in pieces_to_remove:
            if piece in self.game.pieces:
                self.game.pieces.remove(piece)
                print(f"🗑️ Removed {piece.piece_id} from pieces list")
                
                # Additional DEBUG - count kings after removal
                if piece.piece_id in ["KW0", "KB0"]:
                    remaining_kings = [p.piece_id for p in self.game.pieces if p.piece_id in ["KW0", "KB0"]]
                    print(f"👑 Kings remaining after removing {piece.piece_id}: {remaining_kings}")
                    print(f"📊 Total pieces remaining: {len(self.game.pieces)}")
                    
                    # Immediate check for victory conditions
                    white_kings = [p for p in self.game.pieces if p.piece_id == "KW0"]
                    black_kings = [p for p in self.game.pieces if p.piece_id == "KB0"]
                    print(f"🔍 White kings: {len(white_kings)}, Black kings: {len(black_kings)}")
                    
                    if len(white_kings) == 0:
                        print("🏆 No white king - Player 2 should win!")
                    if len(black_kings) == 0:
                        print("🏆 No black king - Player 1 should win!")
        
        # Check victory conditions after capture
        if pieces_to_remove:
            if self.game.win_checker.is_win():
                self.game.win_checker.announce_win()
                self.game.game_over = True  # Mark game as over immediately after victory
        
        # DEBUG: Print attacking piece position after capture
        final_pos = arriving_piece._state._physics.cell
        print(f"🔍 DEBUG: After capture - {arriving_piece.piece_id} at position {final_pos}")
        print(f"🔍 DEBUG: This means the piece should be selectable at position {final_pos}")

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
            print(f"👑 White pawn {piece.piece_id} reached row 0 - promoting to queen!")
        elif is_black_pawn and row == 7:  # Black pawn reached row 7
            should_promote = True
            new_piece_type = "QB"
            print(f"👑 Black pawn {piece.piece_id} reached row 7 - promoting to queen!")
            
        if should_promote:
            self._promote_pawn_to_queen(piece, new_piece_type, target_pos)

    def _promote_pawn_to_queen(self, pawn, queen_type, position):
        """Replace a pawn with a queen at the given position."""
        print(f"🎆 Performing promotion: {pawn.piece_id} -> {queen_type} at position {position}")
        pieces_root = pathlib.Path(__file__).parent.parent / "pieces"
        
        # Create new queen
        from PieceFactory import PieceFactory
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
        from Command import Command
        import time
        now_ms = self.game.game_time_ms()  # Use the game's time method instead of time.time()
        
        # Process the arrived command to properly enter rest_long state
        # This will trigger the normal state machine transition: move -> arrived -> rest_long
        new_queen._state.state = "move"  # Set to move first
        new_queen._state._transition("arrived", now_ms)  # Then transition to rest_long
        print(f"💤 New queen {queen_id} properly set to rest_long state after promotion")
        print(f"🔍 DEBUG: Queen state: {new_queen._state.state}, rest_start: {new_queen._state.rest_start}")
        print(f"🔍 DEBUG: Required rest time: {new_queen._state.rest_time.get('rest_long', 0)}ms")
        print(f"🔍 DEBUG: Game queue connected: {new_queen._state._game_queue is not None}")
        print(f"🔍 DEBUG: Using game time: {now_ms} (monotonic-based)")
        
        # Remove old pawn and add new queen
        if pawn in self.game.pieces:
            self.game.pieces.remove(pawn)
            print(f"🗑️ Removed pawn: {pawn.piece_id}")
            
        self.game.pieces.append(new_queen)
        print(f"👑 Added new queen: {queen_id} at position {position}")
        print(f"🔍 DEBUG: Total pieces in game: {len(self.game.pieces)}")
        print(f"🔍 DEBUG: Queen added to pieces list successfully")
        print(f"🔍 DEBUG: Queen has update method: {hasattr(new_queen, 'update')}")
        print(f"🎉 Promotion completed successfully! {pawn.piece_id} -> {queen_id}")
