import os
import pathlib
from src.core.observers.observer import IObserver
from src.core.game_logic.Command import Command

class SoundEffectObserver(IObserver):
    def __init__(self, sound_player, base_path=None):
        if base_path is None:
            # Go up from src/core/observers to get to the root directory
            # __file__ is in src/core/observers, so we need to go up 4 levels to get to root
            current_file = pathlib.Path(__file__)
            root_dir = current_file.parent.parent.parent.parent  # up 4 levels from src/core/observers/file.py
            base_path = root_dir / "assets" / "pieces"
        self.sound_player = sound_player
        self.base_path = base_path

    def update(self, command: Command):
        piece_id = command.piece_id  # e.g., "BB0"
        piece_type = piece_id[:2]    # e.g., "BB"

        sound_file_mp3 = self.base_path / piece_type / "sounds" / f"{command.type}.mp3"
        sound_file_wav = self.base_path / piece_type / "sounds" / f"{command.type}.wav"
        
        if sound_file_mp3.exists():
            self.sound_player.play(str(sound_file_mp3))
        elif sound_file_wav.exists():
            self.sound_player.play(str(sound_file_wav))
