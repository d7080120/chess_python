
import pathlib
import copy
from .img import Img
from .Command import Command
from .Board import Board

class Graphics:
    def __init__(self,
                 sprites_folder: pathlib.Path,
                 board: Board,
                 loop: bool = True,
                 fps: float = 6.0):
        self.sprites_folder = sprites_folder
        self.board = board
        self.loop = loop
        self.fps = fps

        self.sprites = []
        self.load_sprites()

        self.current_frame = Img()
        self.current_frame.read(sprites_folder / "1.png")

    def load_sprites(self):
        files = sorted(self.sprites_folder.glob("*.png"))
        cell_size = (self.board.cell_W_pix, self.board.cell_H_pix)
        for file in files:
            img = Img().read(file, size=cell_size)
            if img.img.shape[1] > cell_size[0] or img.img.shape[0] > cell_size[1]:
                raise ValueError(f"Sprite {file.name} size {img.img.shape[1]}x{img.img.shape[0]} too big for cell {cell_size}")
            self.sprites.append(img)
        self.total_frames = len(self.sprites)
        if self.total_frames == 0:
            raise ValueError(f"No sprites found in: {self.sprites_folder}")
            
    def copy(self):
        copied_graphics = Graphics(self.sprites_folder, self.board, self.loop, self.fps)
        copied_graphics.sprites = copy.deepcopy(self.sprites)
        return copied_graphics

    def reset(self, cmd: Command):
        self._start_time = 0
        if cmd.type == "move":
            # מתוך params נשלוף את הכלי (נניח שהוא במיקום 2 ברשימה)
            if len(cmd.params) >= 3:
                piece = cmd.params[2]  # מצופה להיות אובייקט עם שדה `type`
                if hasattr(piece, 'type') and isinstance(piece.type, str):
                    index = int(piece.type) if piece.type.isdigit() else 0
                    if 0 <= index < len(self.sprites):
                        self.current_frame = self.sprites[index]
                    else:
                        self.current_frame = Img()
                else:
                    self.current_frame = Img()
            else:
                self.current_frame = Img()

    def update(self, now_ms: int):
        """Advance animation frame based on game-loop time, not wall time."""
        if self.total_frames == 0:
            return

        # כמה זמן עבר בכל פריים אחד, במילישניות
        frame_duration = 1000 / self.fps

        # שמירה מתי התחלנו אם זו הפעם הראשונה
        if not hasattr(self, "_start_time"):
            self._start_time = now_ms

        elapsed = now_ms - self._start_time

        # אינדקס הפריים הנוכחי לפי זמן שעבר
        frame_index = int(elapsed // frame_duration)

        if self.loop:
            frame_index %= self.total_frames
        else:
            frame_index = min(frame_index, self.total_frames - 1)

        self.current_frame = self.sprites[frame_index]

    def get_img(self) -> Img:
        return self.current_frame

    # def copy(self):
    #     copied_graphics = Graphics(self.sprites_folder, self.board, self.loop, self.fps)
    #     copied_graphics.sprites = [sprite.copy() for sprite in self.sprites]
    #     copied_graphics.total_frames = self.total_frames
    #     copied_graphics.current_frame = self.current_frame.copy()
    #     copied_graphics._start_time = getattr(self, "_start_time", 0)
    #     return copied_graphics
