

import pathlib
from .Graphics import Graphics
from .Board import Board
from .mock_img import MockImg  # לשימוש בטסטים בלבד

class GraphicsFactory:
    def load(self,
             sprites_dir: pathlib.Path,
             cfg: dict,
             cell_size: tuple[int, int]) -> Graphics:
        """
        Load graphics object given path to sprites and configuration.
        cfg צפוי להכיל פרטים כגון: { "loop": True, "fps": 8.0 }
        """
        board = Board(
            cell_H_pix=cell_size[1],
            cell_W_pix=cell_size[0],
            cell_H_m=1,
            cell_W_m=1,
            W_cells=8,
            H_cells=8,
            img=cfg.get("img", None) or MockImg()  # אם לא סופק – נטען MockImg
        )

        return Graphics(
            sprites_folder=sprites_dir,
            board=board,
            loop=cfg.get("loop", True),
            fps=cfg.get("fps", 6.0)
        )
