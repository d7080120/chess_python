from typing import Tuple, Optional
from src.core.game_logic.Command import Command
from src.core.game_logic.Board import Board


class Physics:
    """
    בסיס לפיזיקה של כלי: מיקום, מהירות, האם אפשר לתפוס/להיתפס, עדכון מצב.
    """

    def __init__(self, start_cell: Tuple[int, int], board: Board, speed_m_s: float = 1.0, piece_id: str = None):
        self.board = board
        self.cell = start_cell
        self.start_cell = start_cell  # המיקום ההתחלתי לאינטרפולציה
        self.speed = speed_m_s
        self.pixel_pos = self.board.cell_to_pixel(start_cell)
        self._can_capture = True
        self._can_be_captured = True
        self.target_cell = start_cell
        self.moving = False
        self.start_time = 0
        self.end_time = 0
        self.mode = "idle"  # מצב פיזי נוכחי: idle/move/jump
        self.piece_id = piece_id  # שמירת ה-ID של הכלי

    def reset(self, cmd: Command):
        """
        אתחול פיזיקה לפי פקודה חדשה (למשל התחלת תנועה, קפיצה, עמידה).
        """
        # print(f"🔧 Physics.reset: Received command {cmd.type} from {self.cell} to {getattr(cmd, 'target', 'N/A')}")
        self.mode = cmd.type
        if cmd.type == "move":
            self.start_cell = self.cell  # שמירת המיקום ההתחלתי לאינטרפולציה
            self.target_cell = cmd.target
            self.moving = True
            self.start_time = getattr(cmd, "time_ms", getattr(cmd, "timestamp", 0))
            
            # מהירות תנועה - נוודא שתמיד יש מהירות חיובית
            move_speed = 2.0  # תאים לשנייה - מהירות תנועה מהירה יותר
            dist = self._cell_distance(self.cell, self.target_cell)
            # print(f"🔧 Physics: Distance from {self.cell} to {self.target_cell} = {dist}, speed = {move_speed}")
            if dist == 0:
                self.end_time = self.start_time + 100  # 100ms מינימום
            else:
                self.end_time = self.start_time + int(dist / move_speed * 1000)
        elif cmd.type == "jump":
            self.target_cell = cmd.target if hasattr(cmd, 'target') and cmd.target else self.cell
            self.cell = self.target_cell  # קפיצה מיידית למיקום החדש
            self.pixel_pos = self.board.cell_to_pixel(self.cell)  # עדכון pixel_pos
            self.moving = False           # אין תנועה בפועל
            # שמירת זמן לפקודת arrived
            self.start_time = getattr(cmd, "time_ms", getattr(cmd, "timestamp", 0))
            self.end_time = self.start_time + 1  # יצירת arrived מיד במעדכון הבא
        elif cmd.type == "idle":
            self.target_cell = self.cell
            self.pixel_pos = self.board.cell_to_pixel(self.cell)  # וודא שpixel_pos מעודכן
            self.moving = False
        else:
            self.moving = False
            self.pixel_pos = self.board.cell_to_pixel(self.cell)  # וודא עדכון במצבים אחרים

    def update(self, now_ms: int) -> Optional[Command]:
        """
        עדכון מצב פיזי לפי הזמן הנוכחי. מחזיר פקודה אם הסתיימה תנועה/קפיצה.
        """
        if self.moving:
            if now_ms >= self.end_time:
                # תנועה הסתיימה - הגיעה למיקום הסופי
                self.cell = self.target_cell
                self.pixel_pos = self.board.cell_to_pixel(self.cell)
                self.moving = False
                print(f"🏁 Physics: Piece at {self.cell} reached target")
                return Command(timestamp=now_ms, piece_id=self.piece_id, type="arrived", target=self.cell, params=None)
            else:
                # תנועה בתהליך - אינטרפולציה חלקה
                total_duration = self.end_time - self.start_time
                elapsed = now_ms - self.start_time
                progress = elapsed / total_duration  # אחוז התקדמות (0.0 - 1.0)
                
                # חישוב מיקום ביניים
                start_pixel = self.board.cell_to_pixel(self.start_cell)
                target_pixel = self.board.cell_to_pixel(self.target_cell)
                
                # אינטרפולציה לינארית
                x = start_pixel[0] + (target_pixel[0] - start_pixel[0]) * progress
                y = start_pixel[1] + (target_pixel[1] - start_pixel[1]) * progress
                
                self.pixel_pos = (int(x), int(y))
        elif self.mode == "jump" and now_ms >= self.end_time:
            # קפיצה הסתיימה - צריך ליצור פקודת arrived
            print(f"🏁 Physics: Piece jumped to {self.cell}")
            self.mode = "idle"  # סיום הקפיצה
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
    pass  # אפשר להרחיב אם תרצה התנהגות מיוחדת

