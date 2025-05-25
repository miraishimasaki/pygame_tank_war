import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.image = pygame.image.load('image/螢幕擷取畫面 2023-11-17 230834.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.image.get_width()
        self.rect.y = self.image.get_height()
        self.x = float(self.rect.x)
        self.speed = ai_game.settings.alien_speed




    def _check_edges(self):
        if self.rect.right >= self.screen_rect.right:
            return True
        if self.rect.left < 0:
            return True

    def update(self):
        self.x += (self.speed * self.settings.speed_direction)
        self.rect.x = self.x




