
import pathlib
from typing import List, Tuple


class Moves:
    def __init__(self, txt_path: pathlib.Path, dims: Tuple[int, int]):
        """Initialize moves with rules from text file and board dimensions."""
        self.rows, self.cols = dims
        self.deltas = self._load_deltas(txt_path)

    def _load_deltas(self, txt_path: pathlib.Path) -> List[Tuple[int, int]]:
        deltas = []
        with open(txt_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                # ננקה תגיות כמו :non_capture אם קיימות
                dr = int(parts[0].split(":")[0])
                dc = int(parts[1].split(":")[0])
                deltas.append((dr, dc))
        return deltas


    def get_moves(self, r: int, c: int) -> List[Tuple[int, int]]:
        """Get all legal moves from position (r, c) based on deltas and board bounds."""
        moves = []
        for dr, dc in self.deltas:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                moves.append((nr, nc))
        return moves
