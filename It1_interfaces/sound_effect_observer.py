import os
import pathlib
from observer import IObserver
from Command import Command

class SoundEffectObserver(IObserver):
    BASE_PATH = pathlib.Path(__file__).parent.parent.resolve()

    def __init__(self, sound_player, base_path=BASE_PATH / "pieces"):
        self.sound_player = sound_player
        self.base_path = base_path

    def update(self, command: Command):
        piece_id = command.piece_id  # e.g., "BB0"
        piece_type = piece_id[:2]    # e.g., "BB"

        # move_sound = BASE_PATH / "pieces/PW/sounds/move.mp3"
        sound_file_mp3 = f"{self.base_path}/{piece_type}/sounds/{command.type}.mp3"
        sound_file_wav = f"{self.base_path}/{piece_type}/sounds/{command.type}.wav"
        if os.path.exists(sound_file_mp3):
            self.sound_player.play(sound_file_mp3)
        elif os.path.exists(sound_file_wav):
            self.sound_player.play(sound_file_wav)
