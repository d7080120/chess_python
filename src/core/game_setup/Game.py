"""
Game - Main game class with separated classes
"""
import inspect
import pathlib
import queue, threading, time, cv2, math
from typing import List, Dict, Tuple, Optional
from src.graphics.img import Img
from src.core.game_logic.Board import Board
from src.core.game_logic.Command import Command
from src.core.game_logic.Piece import Piece
from src.core.game_setup.integration_setup import setup_observers
from src.ui.sound_player import SoundPlayer

from src.input.InputHandler import InputHandler
from src.ui.PlayerManager import PlayerManager
from src.ui.DrawManager import DrawManager
from src.core.game_logic.CaptureHandler import CaptureHandler
from src.core.game_logic.WinChecker import WinChecker
from src.core.game_logic.MoveValidator import MoveValidator
from src.core.observers.ScoreManager import ScoreManager
from src.ui.PlayerNameManager import PlayerNameManager


class InvalidBoard(Exception): 
    pass


class Game:
    def __init__(self, pieces: List[Piece], board: Board):
        """Initialize the game with pieces and board."""
        self.pieces = pieces
        self.board = board
        self.user_input_queue = queue.Queue()
        self.game_queue = queue.Queue()  # Queue for arrived commands from pieces
        
        # Setup observers - ScoreManager is created here
        self.command_subject, self.logger, self.scorer, self.sound_player, self.score_manager = setup_observers(self)

        # Game over flag
        self.game_over = False

        # Initialize helper classes
        self.player_name_manager = PlayerNameManager()
        self.input_handler = InputHandler(self)
        self.player_manager = PlayerManager(self)
        self.draw_manager = DrawManager(self)
        self.capture_handler = CaptureHandler(self)
        self.win_checker = WinChecker(self)
        self.move_validator = MoveValidator(self)

    # ─── helpers ─────────────────────────────────────────────────────────────
    def game_time_ms(self) -> int:
        """Return the current game time in milliseconds."""
        return int(time.monotonic() * 1000)

    def clone_board(self) -> Board:
        """
        Return a brand-new Board wrapping a copy of the background pixels
        so we can paint sprites without touching the pristine board.
        """
        return self.board.clone()

    def start_user_input_thread(self):
        """Start the user input thread for mouse handling."""
        # Queue already created in constructor - don't override it!
        # Can activate real thread in the future
        pass

    # ─── main public entrypoint ──────────────────────────────────────────────
    def run(self):
        """Main game loop."""
        
        self.start_user_input_thread()
        
        start_ms = self.game_time_ms()
        for p in self.pieces:
            p.reset(start_ms)
        
        # Main loop
        while not self.game_over:
            now = self.game_time_ms()

            # (1) update physics & animations
            for p in self.pieces:
                p.update(now)

            # (2) handle queued Commands from mouse thread
            while not self.user_input_queue.empty():
                cmd: Command = self.user_input_queue.get()
                self._process_input(cmd)
                
                if self.game_over:
                    return
                    
            # (3) handle arrived commands from pieces
            while not self.game_queue.empty():
                cmd: Command = self.game_queue.get()
                self._process_input(cmd)

            # (4) draw current position
            self.draw_manager.draw_game()
            if not self.input_handler.show_frame():
                break

            # (5) detect captures
            self._resolve_collisions()
            
            # (6) 60 FPS control
            import time
            time.sleep(1/60.0)

        # Game ended
        if self.game_over:
            print("Game ended due to victory!")
            
            # Check for remaining commands in queue
            remaining_count = 0
            while not self.user_input_queue.empty():
                cmd = self.user_input_queue.get()
                remaining_count += 1
            if remaining_count > 0:
                print(f"Remaining unprocessed commands: {remaining_count}")
        else:
            print("Game Over!")
        cv2.destroyAllWindows()

    def _process_input(self, cmd: Command):
        """Process input commands and delegate to appropriate handlers."""
        if cmd.type == "arrived":
            self.capture_handler.handle_arrival(cmd)
            return
        
        for piece in self.pieces:
            if piece.piece_id == cmd.piece_id:
                print(f"🎵 DEBUG: Processing command {cmd.type} for piece {piece.piece_id}")
                if piece.on_command(cmd, self.game_time_ms()):
                    print(f"🎵 DEBUG: Notifying observers for {cmd.type}")
                    self.command_subject.notify(cmd)
                else:
                    print(f"🎵 DEBUG: piece.on_command returned False for {cmd.type}")

                # Check win condition after each move
                if self.win_checker.is_win():
                    self.win_checker.announce_win()
                    self.game_over = True
                    return
                break
        else:
            print(f"Piece not found: {cmd.piece_id}")

    def _resolve_collisions(self):
        """Resolve piece collisions and captures."""
        pass
