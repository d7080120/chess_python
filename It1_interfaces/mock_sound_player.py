class MockSoundPlayer:
    def __init__(self):
        self.sounds = []

    def play(self, sound_name):
        self.sounds.append(sound_name)
