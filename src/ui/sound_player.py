import pygame
import os

class SoundPlayer:
    def __init__(self):
        pygame.mixer.init()

    def play(self, sound_path):
        try:
            if not os.path.exists(sound_path):
                return
                
            sound = pygame.mixer.Sound(sound_path)
            sound.play()
        except Exception as e:
            pass
