"""
MoveValidator - Validates move legality and handles piece movement
"""
from src.core.game_logic.Command import Command


class MoveValidator:
    def __init__(self, game_ref):
        """Initialize the move validator with reference to game."""
        self.game = game_ref

    def move_piece(self, piece, new_x, new_y, player_num):
        """Move piece to new position using Command system."""
        if not self._is_valid_move(piece, new_x, new_y, player_num):
            return
        
        current_pos = self._get_piece_position(piece)
        if not current_pos:
            return
        
        current_x, current_y = current_pos
        
        blocking_position = self._check_path(current_x, current_y, new_x, new_y, piece.piece_id)
        
        final_x, final_y = new_x, new_y
        if blocking_position:
            final_x, final_y = blocking_position
        
        target_piece = self._get_piece_at_position(final_x, final_y)
        if target_piece:
            if self._is_player_piece(target_piece, player_num):
                return
            else:
                if target_piece.piece_id in ["KW0", "KB0"]:
                    print(f"KING CAPTURED! {target_piece.piece_id} was taken!")
                    
        is_capture = target_piece is not None
        captured_piece_id = target_piece.piece_id if target_piece else None
        
        command_type = "move"
        
        move_cmd = Command(
            timestamp=self.game.game_time_ms(),
            piece_id=piece.piece_id,
            type=command_type,
            target=(final_x, final_y),
            params=None
        )
        
        move_cmd.source = current_pos
        if is_capture and captured_piece_id:
            move_cmd.params = [captured_piece_id]
        
        self.game.user_input_queue.put(move_cmd)

    def _check_path(self, start_x, start_y, end_x, end_y, piece_type):
        """Check if path is clear and return first blocking piece position if any."""
        if piece_type.startswith('N'):
            return None
        
        dx = end_x - start_x
        dy = end_y - start_y
        
        if piece_type.startswith('K') and abs(dx) <= 1 and abs(dy) <= 1:
            return None
        
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
        
        current_x = start_x + step_x
        current_y = start_y + step_y
        
        while current_x != end_x or current_y != end_y:
            blocking_piece = self._get_piece_at_position(current_x, current_y)
            if blocking_piece:
                return (current_x, current_y)
            
            current_x += step_x
            current_y += step_y
        
        return None

    def _is_valid_move(self, piece, new_x, new_y, player_num):
        """Check if move is valid based on piece type and rules."""
        if not (0 <= new_x <= 7 and 0 <= new_y <= 7):
            return False
        
        current_pos = self._get_piece_position(piece)
        if not current_pos:
            return False
        
        current_x, current_y = current_pos
        
        dx = new_x - current_x
        dy = new_y - current_y
        
        target_piece = self._get_piece_at_position(new_x, new_y)
        is_capture = target_piece is not None
        
        if hasattr(piece._state, '_moves') and hasattr(piece._state._moves, 'valid_moves'):
            valid_moves = piece._state._moves.valid_moves
            
            move_is_valid = False
            
            for move_dx, move_dy, move_type in valid_moves:
                if piece.piece_id.startswith('P'):
                    actual_dx = move_dx
                    actual_dy = move_dy
                    
                    if abs(actual_dy) == 2:
                        if not self._is_pawn_first_move(piece):
                            continue
                    
                    if move_type == 'capture':
                        if not is_capture:
                            continue
                    elif move_type == 'non_capture' or move_type == '1st':
                        if is_capture:
                            continue
                else:
                    actual_dx = move_dx
                    actual_dy = move_dy
                
                if dx == actual_dx and dy == actual_dy:
                    move_is_valid = True
                    break
            
            if not move_is_valid:
                return False
            
            blocking_position = self._check_path(current_x, current_y, new_x, new_y, piece.piece_id)
            
            if blocking_position and blocking_position != (new_x, new_y):
                return False
            
            return True
        else:
            return False

    def _get_piece_position(self, piece):
        """Get the current position of a piece."""
        if not piece:
            return None
            
        if hasattr(piece, '_state') and hasattr(piece._state, '_physics'):
            physics = piece._state._physics
            if hasattr(physics, 'cell'):
                return physics.cell
        
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
        if player_num == 1:
            return 'W' in piece.piece_id
        else:
            return 'B' in piece.piece_id

    def _is_pawn_first_move(self, piece):
        """Check if this is the pawn's first move based on its current position."""
        if not piece.piece_id.startswith('P'):
            return False
        
        current_pos = self._get_piece_position(piece)
        if not current_pos:
            return False
        
        current_x, current_y = current_pos
        
        if 'W' in piece.piece_id:
            return current_y == 6
        else:
            return current_y == 1
