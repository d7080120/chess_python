
from .Board import Board
from .Physics import Physics

class PhysicsFactory:
    def __init__(self, board: Board): 
        """Initialize physics factory with board."""
        self.board = board

    def create(self, start_cell, cfg: dict) -> Physics:
        """Create a physics object with the given configuration.

        cfg must contain: 'speed'
        """
        speed = cfg.get("speed", 1.0)  # ברירת מחדל למהירות
        return Physics(start_cell=start_cell, board=self.board, speed_m_s=speed)
