from src.core.game_logic.Command import Command
from src.core.game_logic.Moves import Moves
from src.graphics.Graphics import Graphics
from src.core.game_logic.Physics import Physics
from typing import Dict, Optional


class State:
    def __init__(self, moves: Moves, graphics: Graphics, physics: Physics, game_queue=None):
        """Initialize state machine with moves, graphics, physics and optional game queue."""
        self._moves = moves
        self._graphics = graphics
        self._physics = physics
        self._game_queue = game_queue
        self.state = "idle"  # Current state: idle, move, jump, rest_short, rest_long
        self.transitions = {
            "idle": {"move": "move", "jump": "jump"},
            "move": {"arrived": "rest_long"},
            "jump": {"arrived": "rest_short"},
            "rest_short": {"rest_done": "idle"},
            "rest_long": {"rest_done": "idle"},
        }
        self.rest_start = None
        self.rest_time = {"rest_short": 2000, "rest_long": 5000}
        self._last_cmd: Optional[Command] = None

    def reset(self, cmd: Command):
        """Reset state machine with a new command."""
        self._last_cmd = cmd
        self._physics.reset(cmd)
        if cmd.type in ("rest_short", "rest_long"):
            self.rest_start = cmd.timestamp if hasattr(cmd, "timestamp") else 0
        elif cmd.type in ("move", "jump"):
            self._transition(cmd.type, getattr(cmd, "timestamp", 0))
        
        self._graphics.reset(cmd)

    def update(self, now_ms: int) -> "State":
        """Update state machine and handle transitions."""
        self._graphics.update(now_ms)
        
        # Handle rest states
        if self.state in ("rest_short", "rest_long"):
            if self.rest_start is not None and now_ms - self.rest_start >= self.rest_time[self.state]:
                self._last_cmd = Command(timestamp=now_ms, piece_id=None, type="rest_done", params=None)
                self._transition("rest_done", now_ms)
        else:
            cmd = self._physics.update(now_ms)
            if cmd is not None:
                self._last_cmd = cmd
                # If it's an arrived command, add it to game queue
                if cmd.type == "arrived":
                    if self._game_queue is not None:
                        self._game_queue.put(cmd)
                self._transition(cmd.type, now_ms)
        return self

    def _transition(self, event: str, now_ms: int):
        next_state = self.transitions.get(self.state, {}).get(event)
        if next_state:
            old_state = self.state
            self.state = next_state
            
            state_cmd = Command(timestamp=now_ms, piece_id=None, type="state_change", 
                              params={"target_state": self.state})
            self._graphics.reset(state_cmd)
            
            if self.state in ("rest_short", "rest_long"):
                self.rest_start = now_ms
                rest_duration = self.rest_time[self.state] / 1000
            elif self.state == "idle":
                self.rest_start = None

    def can_transition(self, now_ms: int) -> bool:
        return True

    def get_command(self) -> Optional[Command]:
        return self._last_cmd

    def process_command(self, cmd: Command) -> "State":
        """Process an incoming command and return the next state."""
        # print(f"🔧 State.process_command: processing command {cmd.type} for {cmd.piece_id}")
        
        if self.state in ("rest_short", "rest_long") and cmd.type in ("move", "jump"):
            if self.rest_start is not None:
                now_ms = cmd.timestamp if hasattr(cmd, 'timestamp') else 0
                elapsed_ms = now_ms - self.rest_start
                required_ms = self.rest_time[self.state]
                
                if elapsed_ms < required_ms:
                    remaining_sec = (required_ms - elapsed_ms) / 1000
                    return None
        
        if cmd.type == "move":
            self._physics.reset(cmd)
            
            self.state = "move"
            self._last_cmd = cmd
            
        elif cmd.type == "jump":
            self._physics.reset(cmd)
            
            self.state = "jump"
            self._last_cmd = cmd
            self._transition("arrived", cmd.timestamp if hasattr(cmd, 'timestamp') else 0)
            
        elif cmd.type == "reset":
            self.reset(cmd)
        
        else:
            pass
        
        return self
