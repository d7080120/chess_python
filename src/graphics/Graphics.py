import pathlib
from typing import List, Dict, Optional
import copy
from src.graphics.img import Img
from src.core.game_logic.Command import Command
from src.core.game_logic.Board import Board


class Graphics:
    def __init__(self,
                 sprites_folder: pathlib.Path,
                 board: Board,
                 loop: bool = True,
                 fps: float = 6.0):
        """
        Initialize graphics with sprites folder, cell size, loop setting, and FPS.
        טוען את כל התמונות מהתיקייה (לפי סדר שמות הקבצים).
        """
        self.sprites_folder = sprites_folder
        self.board = board
        self.loop = loop
        self.fps = fps
        self.frame_time_ms = int(1000 / fps)
        
        # שמור את תיקיית המצבים לשינוי sprites
        self.piece_states_dir = sprites_folder.parent.parent  # מ-idle/sprites ל-states
        
        self.frames: List[Img] = self._load_frames()
        self.current_frame = 0
        self.last_update = 0
        self.running = True

    def _load_frames(self) -> List[Img]:
        frames = []
        cell_size = (self.board.cell_W_pix, self.board.cell_H_pix)
        for img_path in sorted(self.sprites_folder.glob("*.png")):
            img = Img()
            img.read(str(img_path), size=cell_size)  # ודא שזה תואם לגודל התא שלך
            frames.append(img)
        return frames if frames else [Img()]  # לפחות פריים ריק

    def copy(self):
        """Create a shallow copy of the graphics object."""
        new_gfx = Graphics(self.sprites_folder, self.board, self.loop, self.fps)
        new_gfx.current_frame = self.current_frame
        new_gfx.last_update = self.last_update
        new_gfx.running = self.running
        return new_gfx

    def reset(self, cmd: Command = None):
        """Reset the animation with a new command."""
        self.current_frame = 0
        self.last_update = 0
        self.running = True
        
        # אם יש פקודה עם state, החלף sprites בהתאם
        if cmd and hasattr(cmd, 'params') and cmd.params and 'target_state' in cmd.params:
            state_name = cmd.params['target_state']
            self._switch_sprites_for_state(state_name)

    def _switch_sprites_for_state(self, state_name: str):
        """החלף sprites לפי שם המצב"""
        folder_map = {
            "idle": "idle",
            "move": "move", 
            "jump": "jump",
            "rest_short": "short_rest",
            "rest_long": "long_rest"
        }
        
        folder_name = folder_map.get(state_name, "idle")
        new_sprites_dir = self.piece_states_dir / folder_name / "sprites"
        
        if new_sprites_dir.exists():
            self.sprites_folder = new_sprites_dir
            self.frames = self._load_frames()
            self.current_frame = 0

    def update(self, now_ms: int):
        """Advance animation frame based on game-loop time, not wall time."""
        if not self.running or len(self.frames) == 1:
            return
        if self.last_update == 0:
            self.last_update = now_ms
            return
        if now_ms - self.last_update >= self.frame_time_ms:
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.running = False
            self.last_update = now_ms

    def get_img(self) -> Img:
        """Get the current frame image."""
        return self.frames[self.current_frame]
