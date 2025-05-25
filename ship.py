import pygame

class Ship():
    def __init__(self,ai_game):

        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('image/阿布.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.height = self.image.get_height()
    def blitme(self):
        self.screen.blit(self.image,self.rect)
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
        if self.moving_up and self.rect.y > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        self.rect.y = self.y

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom #只复原x值
        self.x = float(self.rect.x)
        self.rect.y = self.settings.screen_height - self.height
        self.y = float(self.rect.y)
    #如果center_ship函数中只有前两行代码，飞船在碰撞后只会在x方向上复原到屏幕中间
    #如果是飞船跑到上面碰撞，上述情况中飞船和外星人将一直碰撞，从而导致程序卡死