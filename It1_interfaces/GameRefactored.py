"""
GameRefactored - גרסה מחודשת של מחלקת Game עם הפרדה למחלקות
"""
import inspect
import pathlib
import queue, threading, time, cv2, math
from typing import List, Dict, Tuple, Optional
from img import Img
from Board import Board
from Command import Command
from Piece import Piece
from integration_setup import setup_observers
from sound_player import SoundPlayer

# ייבוא המחלקות החדשות
from InputHandler import InputHandler
from PlayerManager import PlayerManager
from DrawManager import DrawManager
from CaptureHandler import CaptureHandler
from WinChecker import WinChecker
from MoveValidator import MoveValidator
from ScoreManager import ScoreManager
from PlayerNameManager import PlayerNameManager


class InvalidBoard(Exception): 
    pass


class GameRefactored:
    def __init__(self, pieces: List[Piece], board: Board):
        """Initialize the game with pieces and board."""
        self.pieces = pieces  # שמור כרשימה במקום כמילון
        self.board = board
        self.user_input_queue = queue.Queue()
        self.command_subject, self.logger, self.scorer, self.sound_player = setup_observers()

        # דגל סיום המשחק
        self.game_over = False

        # יצירת המחלקות המסייעות
        self.player_name_manager = PlayerNameManager()
        self.input_handler = InputHandler(self)
        self.player_manager = PlayerManager(self)
        self.draw_manager = DrawManager(self)
        self.capture_handler = CaptureHandler(self)
        self.win_checker = WinChecker(self)
        self.move_validator = MoveValidator(self)
        self.score_manager = ScoreManager(self)

    # ─── helpers ─────────────────────────────────────────────────────────────
    def game_time_ms(self) -> int:
        """Return the current game time in milliseconds."""
        return int(time.monotonic() * 1000)

    def clone_board(self) -> Board:
        """
        Return a **brand-new** Board wrapping a copy of the background pixels
        so we can paint sprites without touching the pristine board.
        """
        return self.board.clone()

    def start_user_input_thread(self):
        """Start the user input thread for mouse handling."""
        # התור כבר נוצר בקונסטרקטור - אל תדרוס אותו!
        # אפשר להפעיל thread אמיתי בעתיד
        pass

    # ─── main public entrypoint ──────────────────────────────────────────────
    def run(self):
        """Main game loop."""
        
        self.start_user_input_thread() # QWe2e5
        
        start_ms = self.game_time_ms()
        for p in self.pieces:
            p.reset(start_ms)
        
        # ─────── main loop ──────────────────────────────────────────────────
        while not self.game_over:
            now = self.game_time_ms() # monotonic time ! not computer time.

            # (1) update physics & animations
            for p in self.pieces:
                p.update(now)

            # (2) handle queued Commands from mouse thread
            while not self.user_input_queue.empty():
                cmd: Command = self.user_input_queue.get()
                self._process_input(cmd)
                
                # בדוק אם המשחק נגמר
                if self.game_over:
                    break

            # (3) draw current position
            self.draw_manager.draw_game()
            if not self.input_handler.show_frame():           # returns False if user closed window
                break

            # (4) detect captures
            self._resolve_collisions()
            
            # (5) שליטה בקצב פריימים - 60 FPS
            import time
            time.sleep(1/60.0)  # ~16.7ms המתנה

        # אם המשחק נגמר בגלל נצחון ולא בגלל סגירת החלון
        if self.game_over:
            print("🎮 המשחק הסתיים עקב נצחון!")
            print("🎮 Game ended due to victory!")
            
            # בדוק אם יש קומנדים שלא עובדו בתור
            remaining_count = 0
            print(f"🔍 בודק קומנדים שנותרו בתור...")
            while not self.user_input_queue.empty():
                cmd = self.user_input_queue.get()
                remaining_count += 1
                print(f"🔍 קומנד שלא עובד: type='{cmd.type}', piece_id='{cmd.piece_id}', target={cmd.target}")
            print(f"🔍 סה\"כ קומנדים שלא עובדו: {remaining_count}")
        else:
            print("🎮 המשחק נגמר!")
            print("🎮 Game Over!")
        cv2.destroyAllWindows()

    # ─── drawing helpers ────────────────────────────────────────────────────
    def _process_input(self, cmd: Command):
        """Process input commands and delegate to appropriate handlers."""
        if cmd.type == "arrived":
            self.capture_handler.handle_arrival(cmd)
            return
        
        for piece in self.pieces:
            if piece.piece_id == cmd.piece_id:
                if piece.on_command(cmd, self.game_time_ms()):
                    self.command_subject.notify(cmd)  # נוטיפיקציה לכל המאזינים

                # 🏆 בדיקת תנאי נצחון אחרי כל תנועה!
                if self.win_checker.is_win():
                    self.win_checker.announce_win()
                    self.game_over = True  # סמן שהמשחק נגמר
                    return  # עצור את המשחק
                break
        else:
            print(f"❌ לא נמצא כלי עם ID: {cmd.piece_id}")

    # ─── capture resolution ────────────────────────────────────────────────
    def _resolve_collisions(self):
        """Resolve piece collisions and captures."""
        pass  # לממש לוגיקת תפיסות בהמשך
