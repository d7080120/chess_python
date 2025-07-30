"""
MoveValidator - מחלקה לבדיקת חוקיות מהלכים והזזת כלים
"""
from Command import Command


class MoveValidator:
    def __init__(self, game_ref):
        """Initialize the move validator with reference to game."""
        self.game = game_ref

    def move_piece(self, piece, new_x, new_y, player_num):
        """Move piece to new position using Command system."""
        # Check if move is valid
        if not self._is_valid_move(piece, new_x, new_y, player_num):
            print(f"❌ Invalid move for {piece.piece_id} to ({new_x}, {new_y})")
            return
        
        # Current position of the piece
        current_pos = self._get_piece_position(piece)
        if not current_pos:
            print(f"❌ Cannot find current position of {piece.piece_id}")
            return
        
        current_x, current_y = current_pos
        
        # Path checking - are there pieces in the way (only after movement is valid!)
        blocking_position = self._check_path(current_x, current_y, new_x, new_y, piece.piece_id)
        
        # If there's a blocking piece in the way, update target position to the blocking piece position
        final_x, final_y = new_x, new_y
        if blocking_position:
            final_x, final_y = blocking_position
            print(f"🎯 Updating target due to blocking piece: from ({new_x}, {new_y}) to ({final_x}, {final_y})")
        
        # Check if there's a piece at the final target position
        target_piece = self._get_piece_at_position(final_x, final_y)
        if target_piece:
            # Check if it's an enemy piece (can capture)
            if self._is_player_piece(target_piece, player_num):
                print(f"❌ Cannot capture piece of same player: {target_piece.piece_id}")
                return
            else:
                print(f"⚔️ {piece.piece_id} captures {target_piece.piece_id}!")
                # Special check for kings - Extended DEBUG!
                if target_piece.piece_id in ["KW0", "KB0"]:
                    print(f"🚨🚨 CRITICAL: KING CAPTURED! {target_piece.piece_id} was taken! 🚨🚨🚨")
                    print(f"💀 King killed: {target_piece.piece_id}")
                    print(f"🔥 This should cause immediate game over!")
                    
                # Don't delete the piece here - this will happen in _handle_arrival when the piece arrives!
        
        # Create movement command - determine type based on whether there's a capture
        is_capture = target_piece is not None
        captured_piece_id = target_piece.piece_id if target_piece else None
        
        # All movement commands are type "move" - ScoreManager will check params for captured piece
        command_type = "move"
        print(f"🎯 Creating command type: {command_type} (capture: {is_capture})")
        
        # Move logging will be done via Observer pattern after command is successfully executed
        
        move_cmd = Command(
            timestamp=self.game.game_time_ms(),
            piece_id=piece.piece_id,
            type=command_type,
            target=(final_x, final_y),  # Use updated position
            params=None
        )
        
        # Add source position information for ScoreManager
        move_cmd.source = current_pos
        if is_capture and captured_piece_id:
            move_cmd.params = [captured_piece_id]
            print(f"🎯 Added captured piece to params: {captured_piece_id}")
        else:
            print(f"🎯 No capture, params remain None")
        
        # Add command to queue - State.process_command will handle state machine
        self.game.user_input_queue.put(move_cmd)
        
        print(f"🎯 Player {player_num}: sent {command_type} command for {piece.piece_id} to ({final_x}, {final_y})")
        print(f"PLAYER {player_num}: Sent {command_type} command for {piece.piece_id} to ({final_x}, {final_y})")
        # No turn switching - each player can move whenever they want

    def _check_path(self, start_x, start_y, end_x, end_y, piece_type):
        """Check if path is clear and return first blocking piece position if any."""
        # Knights can jump over pieces
        if piece_type.startswith('N'):  # Knight - no path checking
            return None
        
        dx = end_x - start_x
        dy = end_y - start_y
        
        # Kings can move one square in any direction - no path checking needed
        if piece_type.startswith('K') and abs(dx) <= 1 and abs(dy) <= 1:
            return None
        
        # Calculate movement direction
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
        
        # Path checking - excluding start and end points
        current_x = start_x + step_x
        current_y = start_y + step_y
        
        while current_x != end_x or current_y != end_y:
            # Check if there's a piece at current square
            blocking_piece = self._get_piece_at_position(current_x, current_y)
            if blocking_piece:
                print(f"🚫 Path blocked! Piece {blocking_piece.piece_id} at position ({current_x}, {current_y})")
                return (current_x, current_y)  # Return blocking piece position
            
            # Move to next square
            current_x += step_x
            current_y += step_y
        
        print(f"✅ Path clear from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        return None  # Path is clear

    def _is_valid_move(self, piece, new_x, new_y, player_num):
        """Check if move is valid based on piece type and rules."""
        # Basic check - within board boundaries
        if not (0 <= new_x <= 7 and 0 <= new_y <= 7):
            return False
        
        # Current position of the piece
        current_pos = self._get_piece_position(piece)
        if not current_pos:
            return False
        
        current_x, current_y = current_pos
        
        # Calculate difference
        dx = new_x - current_x
        dy = new_y - current_y
        
        # Check if there's a piece at target position
        target_piece = self._get_piece_at_position(new_x, new_y)
        is_capture = target_piece is not None
        
        # Read data from piece's move file - first check if move is valid
        if hasattr(piece._state, '_moves') and hasattr(piece._state._moves, 'valid_moves'):
            valid_moves = piece._state._moves.valid_moves
            print(f"🔍 Checking move: {piece.piece_id} from ({current_x},{current_y}) to ({new_x},{new_y}), difference: ({dx},{dy})")
            print(f"🔍 Possible moves: {valid_moves}")
            
            move_is_valid = False
            
            # Check each possible move - coordinates only, no move types
            for move_dx, move_dy, move_type in valid_moves:
                # Pawn move files: need to reverse direction
                # White and black pawns are reversed in coordinate system
                if piece.piece_id.startswith('P'):  # Pawns - reverse direction
                    # File says (0,-1) and this should remain (0,-1)
                    actual_dx = move_dx  # Keep as is
                    actual_dy = move_dy  # Keep as is
                    
                    # Special check for pawns: 2-step move only allowed on first move
                    if abs(actual_dy) == 2:  # This is a 2-step move
                        if not self._is_pawn_first_move(piece):
                            print(f"❌ Pawn 2-step move only allowed on first move")
                            continue  # Skip this move option
                else:  # All other pieces - use as is
                    actual_dx = move_dx
                    actual_dy = move_dy
                
                print(f"🔍 Checking move ({move_dx},{move_dy},{move_type}) -> translated: ({actual_dx},{actual_dy})")
                
                # Check if move matches - coordinates only!
                if dx == actual_dx and dy == actual_dy:
                    print(f"✅ Move matches! Difference ({dx},{dy}) = coordinates ({actual_dx},{actual_dy})")
                    move_is_valid = True
                    break
            
            if not move_is_valid:
                print(f"❌ No matching move found")
                return False
            
            # Now, after we know the move is valid according to files, check path
            blocking_position = self._check_path(current_x, current_y, new_x, new_y, piece.piece_id)
            
            # If there's a blocking piece in the way and we're not trying to move to its position
            if blocking_position and blocking_position != (new_x, new_y):
                print(f"🚫 Invalid move: path blocked by piece at position {blocking_position}")
                return False
            
            print(f"✅ Valid move!")
            return True
        else:
            print(f"❌ No move data for piece {piece.piece_id}")
            return False

    def _get_piece_position(self, piece):
        """Get the current position of a piece."""
        if not piece:
            return None
            
        # Check if piece has _state with _physics with cell
        if hasattr(piece, '_state') and hasattr(piece._state, '_physics'):
            physics = piece._state._physics
            if hasattr(physics, 'cell'):
                return physics.cell
        
        # Additional fallbacks
        if hasattr(piece, 'x') and hasattr(piece, 'y'):
            return (piece.x, piece.y)
        
        if hasattr(piece, 'board_position'):
            return piece.board_position
        
        return None

    def _get_piece_at_position(self, x, y):
        """Get piece at specific position, if any."""
        for piece in self.game.pieces:
            piece_pos = self._get_piece_position(piece)
            if piece_pos and piece_pos == (x, y):
                return piece
        return None

    def _is_player_piece(self, piece, player_num):
        """Check if piece belongs to specified player."""
        # Player 1 = white pieces (W), Player 2 = black pieces (B)
        # Pieces are now identified as PW0, PW1, PB0, PB1, etc.
        if player_num == 1:
            return 'W' in piece.piece_id  # White pieces
        else:
            return 'B' in piece.piece_id  # Black pieces

    def _is_pawn_first_move(self, piece):
        """Check if this is the pawn's first move based on its current position."""
        if not piece.piece_id.startswith('P'):
            return False
        
        current_pos = self._get_piece_position(piece)
        if not current_pos:
            return False
        
        current_x, current_y = current_pos
        
        # White pawns start at row 6, black pawns start at row 1
        if 'W' in piece.piece_id:
            return current_y == 6  # White pawn still at starting position
        else:
            return current_y == 1  # Black pawn still at starting position
