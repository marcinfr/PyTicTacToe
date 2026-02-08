import pygame
import sys
import os

class Assets:
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    
    def play(file):
        sound = pygame.mixer.Sound(Assets.resource_path("assets/" + file))
        sound.play()