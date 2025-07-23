

# from typing import Tuple, Optional
# from .Command import Command
# from .Board import Board

# class Physics:

#     def __init__(self, start_cell: Tuple[int, int],
#                  board: Board, speed_m_s: float = 1.0):
#         self.cell = start_cell
#         self.board = board
#         self.speed_m_s = speed_m_s
#         self.cmd: Optional[Command] = None
#         self.start_time: Optional[int] = None
#         self.pos_m = (start_cell[0] * board.cell_W_m, start_cell[1] * board.cell_H_m)
#         self.target_cell = start_cell

#     def reset(self, cmd: Command):
#         self.cmd = cmd
#         self.start_time = None
#         self.cell = cmd.from_pos
#         self.target_cell = cmd.to_pos

#     def update(self, now_ms: int) -> Command:
#         if self.start_time is None:
#             self.start_time = now_ms
#         elapsed_sec = (now_ms - self.start_time) / 1000.0

#         dx = self.target_cell[0] - self.cell[0]
#         dy = self.target_cell[1] - self.cell[1]
#         dist_cells = (dx, dy)

#         dist_m = (dist_cells[0] * self.board.cell_W_m, dist_cells[1] * self.board.cell_H_m)
#         total_dist = (dist_m[0]**2 + dist_m[1]**2)**0.5

#         traveled = min(1.0, (elapsed_sec * self.speed_m_s) / total_dist) if total_dist > 0 else 1.0

#         self.pos_m = (
#             (1 - traveled) * self.cell[0] * self.board.cell_W_m + traveled * self.target_cell[0] * self.board.cell_W_m,
#             (1 - traveled) * self.cell[1] * self.board.cell_H_m + traveled * self.target_cell[1] * self.board.cell_H_m
#         )

#         return self.cmd if traveled >= 1.0 else None

#     def can_be_captured(self) -> bool:
#         return True

#     def can_capture(self) -> bool:
#         return True

#     def get_pos(self) -> Tuple[int, int]:
#         return self.pos_m

# class IdlePhysics(Physics):
#     def update(self, now_ms: int) -> Command:
#         return None

#     def can_be_captured(self) -> bool:
#         return True

#     def can_capture(self) -> bool:
#         return False




from typing import Tuple, Optional
from .Command import Command
from .Board import Board

class Physics:

    def __init__(self, start_cell: Tuple[int, int],
                 board: Board, speed_m_s: float = 1.0):
        self.cell = start_cell
        self.board = board
        self.speed_m_s = speed_m_s
        self.cmd: Optional[Command] = None
        self.start_time: Optional[int] = None
        self.pos_m = (int(start_cell[0] * board.cell_W_m),int(start_cell[1] * board.cell_H_m))
        self.target_cell = start_cell


    def reset(self, cmd: Command):
        self.cmd = cmd
        self.start_time = None
        self.cell = cmd.params[0]
        self.target_cell = cmd.params[1] if len(cmd.params) > 1 else self.cell


    def update(self, now_ms: int) -> Optional[Command]:
        if self.start_time is None:
            self.start_time = now_ms
        elapsed_sec = (now_ms - self.start_time) / 1000.0

        dx = self.target_cell[0] - self.cell[0]
        dy = self.target_cell[1] - self.cell[1]
        dist_cells = (dx, dy)

        dist_m = (dist_cells[0] * self.board.cell_W_m, dist_cells[1] * self.board.cell_H_m)
        total_dist = (dist_m[0]**2 + dist_m[1]**2)**0.5

        traveled = min(1.0, (elapsed_sec * self.speed_m_s) / total_dist) if total_dist > 0 else 1.0

        self.pos_m = (
            int((1 - traveled) * self.cell[0] * self.board.cell_W_m + traveled * self.target_cell[0] * self.board.cell_W_m),
            int((1 - traveled) * self.cell[1] * self.board.cell_H_m + traveled * self.target_cell[1] * self.board.cell_H_m)
        )

        return self.cmd if traveled >= 1.0 else None

    def can_be_captured(self) -> bool:
        return True

    def can_capture(self) -> bool:
        return True

    def get_pos(self) -> Tuple[int, int]:
        return self.pos_m
    
    def get_pos_inpixels(self) -> Tuple[int, int]:
        return (int(self.pos_m[0] / self.board.cell_W_m * self.board.cell_W_pix),
                int(self.pos_m[1] / self.board.cell_H_m * self.board.cell_H_pix))
    def copy(self) -> "Physics":
            copied = Physics(start_cell=self.cell, board=self.board, speed_m_s=self.speed_m_s)
            copied.cmd = self.cmd
            copied.start_time = self.start_time
            copied.pos_m = self.pos_m
            copied.target_cell = self.target_cell
            return copied
    
    
class IdlePhysics(Physics):
    def update(self, now_ms: int) -> Optional[Command]:
        return None

    def can_be_captured(self) -> bool:
        return True

    def can_capture(self) -> bool:
        return False
    
    
