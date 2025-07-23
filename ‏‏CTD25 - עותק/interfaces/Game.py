
# import inspect
# import pathlib
# import queue, threading, time, cv2, math
# import numpy as np
# from typing import List, Dict, Tuple, Optional
# from .Board   import Board
# from .Command import Command
# from .Piece   import Piece
# from .img     import Img


# class InvalidBoard(Exception): ...

# class Game:
#     def __init__(self, pieces: List[Piece], board: Board):
#         self.pieces = pieces
#         self.board = board
#         self.user_input_queue = queue.Queue()
#         self._start_time = time.monotonic()
#         self._input_thread = None

#     def game_time_ms(self) -> int:
#         return int((time.monotonic() - self._start_time) * 1000)

#     def clone_board(self) -> Board:
#         return self.board.clone()

#     def start_user_input_thread(self):
#         def run():
#             while True:
#                 # MOCK INPUT LOOP (in real scenario use mouse or file input)
#                 time.sleep(1)
#         self._input_thread = threading.Thread(target=run, daemon=True)
#         self._input_thread.start()

#     def run(self):
#         """Main game loop."""
#         self.start_user_input_thread()  # QWe2e5

#         start_ms = self.game_time_ms()
#         for p in self.pieces:
#             p.reset(start_ms)

#         # ─────── main loop ──────────────────────────────────────────────────
#         while not self._is_win():
#             now = self.game_time_ms()  # monotonic time ! not computer time.

#             # (1) update physics & animations
#             for p in self.pieces:
#                 p.update(now)

#             # (2) handle queued Commands from mouse thread
#             while not self.user_input_queue.empty():  # QWe2e5
#                 cmd: Command = self.user_input_queue.get()
#                 self._process_input(cmd)

#             # (3) draw current position
#             self._draw()
#             if not self._show():  # returns False if user closed window
#                 break

#             # (4) detect captures
#             self._resolve_collisions()

#         self._announce_win()
#         cv2.destroyAllWindows()

#     def _process_input(self, cmd: Command):
#         for p in self.pieces:
#             if p.piece_id == cmd.piece_id:
#                 p.on_command(cmd)

#     def _draw(self):
#         frame: Board = self.board.clone()  # עותק מלא של הלוח
#         now = self.game_time_ms()
#         for p in self.pieces:
#             p.draw_on_board(frame, now)
#         self._last_frame = frame


#     def _show(self) -> bool:
#         img = self._last_frame.img.img  # assuming board holds `get_img`
#         filtered_values = img[(img != 0) & (img != 255)]
#         sh = img.shape
#         # print(np.min(img), np.max(img))  # הדפסת הערכים המינימליים והמקסימליים

#         cv2.imshow("Game", img)
#         # self._last_frame.img.show()
#         key = cv2.waitKey(1)
#         return key != 27  # ESC

#     def _resolve_collisions(self):
#         pass  # to be implemented

#     def _is_win(self) -> bool:
#         return False  # for now no win condition

#     def _announce_win(self):
#         print("Game over! Player X wins")


import inspect
import pathlib
import queue, threading, time, cv2, math
import numpy as np
from typing import List, Dict, Tuple, Optional
from .Board   import Board
from .Command import Command
from .Piece   import Piece
from .img     import Img

class InvalidBoard(Exception): ...

class Game:
    def __init__(self, pieces: List[Piece], board: Board):
        self.pieces = pieces
        self.board = board
        self.user_input_queue = queue.Queue()
        self._start_time = time.monotonic()
        self._input_thread = None
        self.board_state = [[None for _ in range(8)] for _ in range(8)]  # לוח 8x8 מאוחסן ב-None

        # אתחול הלוח עם הכלים
        self.initialize_board()

    def initialize_board(self):
        for piece in self.pieces:
            x, y = piece._state._physics.get_pos()  # נניח שיש למלך מיקום (x, y)
            print(x, y )
            self.board_state[y][x] = piece  # שמירה של הכלי במיקום המתאים בלוח

    def game_time_ms(self) -> int:
        return int((time.monotonic() - self._start_time) * 1000)

    def clone_board(self) -> Board:
        return self.board.clone()

    def start_user_input_thread(self):
        def run():
            while True:
                # MOCK INPUT LOOP (in real scenario use mouse or file input)
                time.sleep(1)
        self._input_thread = threading.Thread(target=run, daemon=True)
        self._input_thread.start()

    def run(self):
        """Main game loop."""
        self.start_user_input_thread()  # QWe2e5

        start_ms = self.game_time_ms()
        for p in self.pieces:
            p.reset(start_ms)

        # ─────── main loop ──────────────────────────────────────────────────
        while not self._is_win():
            now = self.game_time_ms()  # monotonic time ! not computer time.

            # (1) update physics & animations
            for p in self.pieces:
                p.update(now)

            # (2) handle queued Commands from mouse thread
            while not self.user_input_queue.empty():  # QWe2e5
                cmd: Command = self.user_input_queue.get()
                self._process_input(cmd)

            # (3) draw current position
            self._draw()
            if not self._show():  # returns False if user closed window
                break

            # (4) detect captures
            self._resolve_collisions()

        self._announce_win()
        cv2.destroyAllWindows()

    def _process_input(self, cmd: Command):
        for p in self.pieces:
            if p.piece_id == cmd.piece_id:
                b=p.on_command(cmd)
                if b==True:# עדכון הלוח לאחר ביצוע הפקודה
                    self.update_board_state(p, cmd)

    def update_board_state(self, piece: Piece, cmd: Command):
        # עדכון הלוח לאחר ביצוע פקודה
        start_x, start_y = piece._state._physics.get_pos()
        end_x = cmd.params[0] 
        end_y = cmd.params[1] # נניח שיש לך את המיקום הסופי בפקודה

        # עדכון הלוח
        self.board_state[start_y][start_x] = None  # המיקום ההתחלתי מתעדכן ל-None
        self.board_state[end_y][end_x] = piece  # המיקום הסופי מתעדכן לכלי

    def _draw(self):
        frame: Board = self.board.clone()  # עותק מלא של הלוח
        now = self.game_time_ms()
        for p in self.pieces:
            p.draw_on_board(frame, now)
        self._last_frame = frame

    def _show(self) -> bool:
        img = self._last_frame.img.img  # assuming board holds `get_img`
        cv2.imshow("Game", img)
        key = cv2.waitKey(1)
        return key != 27  # ESC

    def _resolve_collisions(self):
        pass  # to be implemented

    def _is_win(self) -> bool:
        return False  # for now no win condition

    def _announce_win(self):
        print("Game over! Player X wins")