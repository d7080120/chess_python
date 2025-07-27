import pygame
import os

class SoundPlayer:
    def __init__(self):
        pygame.mixer.init()

    def play(self, sound_path):
        try:
            sound = pygame.mixer.Sound(sound_path)
            sound.play()
            print(f"Playing sound: {sound_path}")
        except Exception as e:
            print(f"Error playing {sound_path}: {e}")
