import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.image = pygame.image.load('image/螢幕擷取畫面 2023-11-07 223920.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = ai_game.ship.rect.midtop
        self.speed = ai_game.settings.bullet_speed
        self.y = float(self.rect.y)


    def update(self):
        self.y -= self.speed #直接在此处调用ai_game.settings.bullet_speed会报错，因为ai_game没有定义
        self.rect.y = self.y


    def DrawBullet(self):
        self.screen.blit(self.image,self.rect)