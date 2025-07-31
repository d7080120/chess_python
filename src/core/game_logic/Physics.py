from typing import Tuple, Optional
from src.core.game_logic.Command import Command
from src.core.game_logic.Board import Board


class Physics:
    """
    Base class for piece physics: position, speed, capture ability, state updates.
    """

    def __init__(self, start_cell: Tuple[int, int], board: Board, speed_m_s: float = 1.0, piece_id: str = None):
        self.board = board
        self.cell = start_cell
        self.start_cell = start_cell
        self.speed = speed_m_s
        self.pixel_pos = self.board.cell_to_pixel(start_cell)
        self._can_capture = True
        self._can_be_captured = True
        self.target_cell = start_cell
        self.moving = False
        self.start_time = 0
        self.end_time = 0
        self.mode = "idle"
        self.piece_id = piece_id

    def reset(self, cmd: Command):
        """
        Initialize physics based on new command (movement, jump, etc.).
        """
        # print(f"🔧 Physics.reset: Received command {cmd.type} from {self.cell} to {getattr(cmd, 'target', 'N/A')}")
        self.mode = cmd.type
        if cmd.type == "move":
            self.start_cell = self.cell
            self.target_cell = cmd.target
            self.moving = True
            self.start_time = getattr(cmd, "time_ms", getattr(cmd, "timestamp", 0))
            
            move_speed = 2.0
            dist = self._cell_distance(self.cell, self.target_cell)
            if dist == 0:
                self.end_time = self.start_time + 100
            else:
                self.end_time = self.start_time + int(dist / move_speed * 1000)
        elif cmd.type == "jump":
            self.target_cell = cmd.target if hasattr(cmd, 'target') and cmd.target else self.cell
            self.cell = self.target_cell
            self.pixel_pos = self.board.cell_to_pixel(self.cell)
            self.moving = False
            self.start_time = getattr(cmd, "time_ms", getattr(cmd, "timestamp", 0))
            self.end_time = self.start_time + 1
        elif cmd.type == "idle":
            self.target_cell = self.cell
            self.pixel_pos = self.board.cell_to_pixel(self.cell)
            self.moving = False
        else:
            self.moving = False
            self.pixel_pos = self.board.cell_to_pixel(self.cell)

    def update(self, now_ms: int) -> Optional[Command]:
        """
        Update physics state based on current time. Returns command if movement/jump is completed.
        """
        if self.moving:
            if now_ms >= self.end_time:
                # Movement completed - reached final position
                self.cell = self.target_cell
                self.pixel_pos = self.board.cell_to_pixel(self.cell)
                self.moving = False
                return Command(timestamp=now_ms, piece_id=self.piece_id, type="arrived", target=self.cell, params=None)
            else:
                # Movement in progress - smooth interpolation
                total_duration = self.end_time - self.start_time
                elapsed = now_ms - self.start_time
                progress = elapsed / total_duration
                
                # Calculate intermediate position
                start_pixel = self.board.cell_to_pixel(self.start_cell)
                target_pixel = self.board.cell_to_pixel(self.target_cell)
                
                # Linear interpolation
                x = start_pixel[0] + (target_pixel[0] - start_pixel[0]) * progress
                y = start_pixel[1] + (target_pixel[1] - start_pixel[1]) * progress
                
                self.pixel_pos = (int(x), int(y))
        elif self.mode == "jump" and now_ms >= self.end_time:
            # Jump completed - need to create arrived command
            self.mode = "idle"
            return Command(timestamp=now_ms, piece_id=self.piece_id, type="arrived", target=self.cell, params=None)
        return None

    def can_be_captured(self) -> bool:
        return self._can_be_captured

    def can_capture(self) -> bool:
        return self._can_capture

    def get_pos(self) -> Tuple[int, int]:
        return self.pixel_pos

    def _cell_distance(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        dr = b[0] - a[0]
        dc = b[1] - a[1]
        return (dr ** 2 + dc ** 2) ** 0.5


class IdlePhysics(Physics):
    def reset(self, cmd: Command):
        self.moving = False
        self.mode = "idle"

    def update(self, now_ms: int) -> Optional[Command]:
        return None


class MovePhysics(Physics):
    pass

