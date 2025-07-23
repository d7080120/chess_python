


from .Board import Board
from .Command import Command
from .State import State
import cv2

class Piece:
    def __init__(self, piece_id: str, init_state: State):
        """Initialize a piece with ID and initial state."""
        self._piece_id = piece_id
        self._state = init_state

    # def is_command_possible(self, cmd: Command) -> bool:
    #     """Check if this command is intended for this piece."""
    #     return cmd.piece_id == self._piece_id

    def is_command_possible(self, cmd: Command) -> bool:
        """Check if this command is intended for this piece and if the move is legal."""
        if cmd.piece_id != self._piece_id:
            return False

        # קבלת המיקום הנוכחי של הכלי
        current_pos = self._state._physics.cell
        target_pos = tuple(cmd.params)  # נניח שהפרמטרים הם (row, col)

        # קבלת התנועות החוקיות מהמיקום הנוכחי
        legal_moves = self._state.moves.get_moves(*current_pos)

    # בדוק אם היעד נמצא בין התנועות החוקיות
        return target_pos in legal_moves

    def on_command(self, cmd: Command, now_ms: int):
        """Handle a command for this piece."""
        if self.is_command_possible(cmd):
            self._state = self._state.process_command(cmd)
            self._state.update(now_ms)
            return True
        return False

    def reset(self, start_ms: int):
        """Reset the piece to idle state."""
        pos = self._state._physics.cell  # מיקום נוכחי

        cmd = Command(piece_id=self._piece_id, type="idle", params=[pos,pos], timestamp=start_ms)
        self._state.reset(cmd)

    def update(self, now_ms: int):
        """Update the piece state based on current time."""
        self._state = self._state.update(now_ms)

    def draw_on_board(self, board: Board, now_ms: int):
        """Draw the piece on the board with its current image."""
        img = self._state._graphics.get_img()
        x, y = self._state._physics.get_pos_inpixels()
        img.draw_on(board.img, x,y)
        self._state = self._state.update(now_ms)
    
    
