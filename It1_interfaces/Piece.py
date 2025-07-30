from Board import Board
from Command import Command
from State import State
import cv2


class Piece:
    def __init__(self, piece_id: str, init_state: State):
        """Initialize a piece with ID and initial state."""
        self.piece_id = piece_id
        self._state = init_state

    def on_command(self, cmd: Command, now_ms: int):
        """Handle a command for this piece."""
        
        if hasattr(self._state, "process_command"):
            new_state = self._state.process_command(cmd)
            if new_state and new_state != self._state:
                self._state = new_state  # Update to new state!
                if hasattr(self._state, "update"):
                    self._state.update(now_ms)
                return True  # Command was accepted and executed
            elif not new_state:
                # Command was rejected (invalid move) - no state change, no notify
                if hasattr(self._state, "update"):
                    self._state.update(now_ms)
                return False  # Command was rejected
            else:
                # Same state but command was processed successfully
                if hasattr(self._state, "update"):
                    self._state.update(now_ms)
                return True  # Command was accepted
        
        if hasattr(self._state, "update"):
            self._state.update(now_ms)
            
        return True  # Default to success if no process_command method 


    def reset(self, start_ms: int = 0):
        """Reset the piece to idle state."""
        if hasattr(self._state, "reset"):
            self._state.reset(Command(timestamp=start_ms, piece_id=self.piece_id, type="reset", params=None))

    def update(self, now_ms: int):
        """Update the piece state based on current time."""
        if hasattr(self._state, "update"):
            self._state.update(now_ms)

    def draw_on_board(self, board: Board, now_ms: int):
        """
        Draw the piece on the board using its graphics and physics position.
        Uses pixel_pos for smooth animation instead of cell
        """
        graphics = getattr(self._state, "_graphics", None)
        physics = getattr(self._state, "_physics", None)
        if graphics is not None and physics is not None:
            img = graphics.get_img()
            # Use smooth pixel position instead of cell
            pixel_pos = getattr(physics, "pixel_pos", None)
            if pixel_pos is not None:
                x, y = pixel_pos
                img.draw_on(board.img, x, y)
                # debug: show both cell position and pixel position
                cell = getattr(physics, "cell", None)
                # if physics.moving:
                #     print(f"🏃 Drawing {self.piece_id}: cell {cell} -> pixel ({x}, {y})")
                # else:
                #     print(f"🧘 Drawing {self.piece_id} at rest in {cell} -> pixel ({x}, {y})")
